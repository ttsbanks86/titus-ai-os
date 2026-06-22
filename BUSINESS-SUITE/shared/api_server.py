#!/usr/bin/env python3
"""Open Business Suite — Shared Integration API Server
Connects: Pipeline CRM, Content Engine, Academy Platform, Command Center
"""
import sys, json, os, sqlite3, datetime, uuid, threading, ctypes
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import ctypes.wintypes

ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)

PORT = int(os.environ.get("OS_PORT", "19200"))
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "business_suite.db")

# ─── Database Schema ────────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Shared contacts (used by CRM + Content Engine + Academy)
    c.execute("""CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, email TEXT, phone TEXT, company TEXT,
        source TEXT DEFAULT 'manual',
        stage TEXT DEFAULT 'lead',
        value REAL DEFAULT 0,
        tags TEXT DEFAULT '',
        notes TEXT DEFAULT '',
        created_at TEXT, updated_at TEXT
    )""")
    
    # Deals / pipeline (CRM)
    c.execute("""CREATE TABLE IF NOT EXISTS deals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        contact_id INTEGER, title TEXT, value REAL,
        stage TEXT DEFAULT 'lead',
        probability INTEGER DEFAULT 10,
        expected_close TEXT,
        notes TEXT DEFAULT '',
        created_at TEXT, updated_at TEXT
    )""")
    
    # Content calendar (Content Engine)
    c.execute("""CREATE TABLE IF NOT EXISTS content (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT, platform TEXT, content_type TEXT,
        status TEXT DEFAULT 'draft',
        scheduled_date TEXT, published_date TEXT,
        body TEXT DEFAULT '',
        engagement_data TEXT DEFAULT '{}',
        created_at TEXT, updated_at TEXT
    )""")
    
    # Courses / memberships (Academy Platform)
    c.execute("""CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT, description TEXT, price REAL,
        module_count INTEGER DEFAULT 0,
        student_count INTEGER DEFAULT 0,
        status TEXT DEFAULT 'draft',
        created_at TEXT, updated_at TEXT
    )""")
    
    # Activities (shared logging across all systems)
    c.execute("""CREATE TABLE IF NOT EXISTS activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entity_type TEXT, entity_id INTEGER,
        action TEXT, detail TEXT,
        created_at TEXT
    )""")
    
    # Metrics (Command Center)
    c.execute("""CREATE TABLE IF NOT EXISTS metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        metric_key TEXT, metric_value REAL,
        label TEXT, category TEXT,
        recorded_at TEXT
    )""")
    
    conn.commit()
    return conn

db_lock = threading.Lock()

def query(sql, params=None):
    with db_lock:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        if params:
            result = conn.execute(sql, params).fetchall()
        else:
            result = conn.execute(sql).fetchall()
        conn.commit()
        conn.close()
    return [dict(r) for r in result]

def execute(sql, params=None):
    with db_lock:
        conn = sqlite3.connect(DB_PATH)
        if params:
            conn.execute(sql, params)
        else:
            conn.execute(sql)
        conn.commit()
        conn.close()

def log_activity(entity_type, entity_id, action, detail=""):
    execute(
        "INSERT INTO activities (entity_type, entity_id, action, detail, created_at) VALUES (?,?,?,?,?)",
        (entity_type, entity_id, action, detail, datetime.datetime.now().isoformat())
    )

# ─── HTTP Handler ────────────────────────────────────────────────────────
class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip('/')
        qs = {k: v[0] for k, v in (p.split('=') for p in parsed.query.split('&') if '=' in p)} if parsed.query else {}
        
        try:
            if path == "/status":
                self.json({"status": "ok", "db": os.path.exists(DB_PATH), "port": PORT})
            
            elif path == "/contacts":
                self.json(query("SELECT * FROM contacts ORDER BY updated_at DESC"))
            elif path.startswith("/contacts/"):
                cid = int(path.split("/")[-1])
                self.json(query("SELECT * FROM contacts WHERE id=?", (cid,)))
            
            elif path == "/deals":
                stage = qs.get("stage", "")
                sql = "SELECT d.*, c.name as contact_name FROM deals d LEFT JOIN contacts c ON d.contact_id=c.id"
                if stage: sql += " WHERE d.stage=?"
                sql += " ORDER BY d.updated_at DESC"
                self.json(query(sql, (stage,)) if stage else query(sql))
            elif path.startswith("/deals/"):
                did = int(path.split("/")[-1])
                self.json(query("SELECT d.*, c.name as contact_name FROM deals d LEFT JOIN contacts c ON d.contact_id=c.id WHERE d.id=?", (did,)))
            
            elif path == "/content":
                self.json(query("SELECT * FROM content ORDER BY scheduled_date DESC"))
            
            elif path == "/courses":
                self.json(query("SELECT * FROM courses ORDER BY updated_at DESC"))
            
            elif path == "/activities":
                limit = int(qs.get("limit", 20))
                self.json(query("SELECT * FROM activities ORDER BY created_at DESC LIMIT ?", (limit,)))
            
            elif path == "/metrics":
                category = qs.get("category", "")
                if category:
                    self.json(query("SELECT * FROM metrics WHERE category=? ORDER BY recorded_at DESC", (category,)))
                else:
                    self.json(query("SELECT * FROM metrics ORDER BY recorded_at DESC LIMIT 50"))
            
            elif path == "/dashboard":
                # Unified dashboard data
                contacts_count = query("SELECT COUNT(*) as c FROM contacts")[0]["c"]
                deals_total = query("SELECT COALESCE(SUM(value),0) as t FROM deals WHERE stage NOT IN ('closed_lost')")[0]["t"]
                content_scheduled = query("SELECT COUNT(*) as c FROM content WHERE status='scheduled'")[0]["c"]
                courses_active = query("SELECT COUNT(*) as c FROM courses WHERE status='published'")[0]["c"]
                recent_activities = query("SELECT * FROM activities ORDER BY created_at DESC LIMIT 10")
                pipeline = query("SELECT stage, COUNT(*) as count, COALESCE(SUM(value),0) as value FROM deals GROUP BY stage ORDER BY stage")
                
                self.json({
                    "contacts": contacts_count,
                    "pipeline_value": deals_total,
                    "scheduled_content": content_scheduled,
                    "active_courses": courses_active,
                    "recent_activities": recent_activities,
                    "pipeline_breakdown": pipeline
                })
            
            else:
                self.json({"error": "not found"}, 404)
        except Exception as e:
            self.json({"error": str(e)}, 500)
    
    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip('/')
        content_len = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(content_len)) if content_len else {}
        
        try:
            if path == "/contacts":
                now = datetime.datetime.now().isoformat()
                execute("INSERT INTO contacts (name,email,phone,company,source,stage,value,tags,notes,created_at,updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    (body.get("name",""), body.get("email",""), body.get("phone",""), body.get("company",""),
                     body.get("source","manual"), body.get("stage","lead"), body.get("value",0),
                     body.get("tags",""), body.get("notes",""), now, now))
                cid = query("SELECT last_insert_rowid() as id")[0]["id"]
                log_activity("contact", cid, "created", f"Contact {body.get('name','')} added")
                self.json({"id": cid, "status": "created"})
            
            elif path.startswith("/contacts/") and path.endswith("/update"):
                cid = int(path.split("/")[-2])
                now = datetime.datetime.now().isoformat()
                fields = ["name","email","phone","company","stage","value","tags","notes"]
                sets = ", ".join([f"{f}=?" for f in fields if f in body])
                vals = [body[f] for f in fields if f in body]
                if sets:
                    execute(f"UPDATE contacts SET {sets}, updated_at=? WHERE id=?", (*vals, now, cid))
                    log_activity("contact", cid, "updated", "Contact updated")
                self.json({"status": "updated"})
            
            elif path == "/deals":
                now = datetime.datetime.now().isoformat()
                execute("INSERT INTO deals (contact_id,title,value,stage,probability,expected_close,notes,created_at,updated_at) VALUES (?,?,?,?,?,?,?,?,?)",
                    (body.get("contact_id"), body.get("title",""), body.get("value",0),
                     body.get("stage","lead"), body.get("probability",10), body.get("expected_close",""),
                     body.get("notes",""), now, now))
                did = query("SELECT last_insert_rowid() as id")[0]["id"]
                log_activity("deal", did, "created", f"Deal: {body.get('title','')}")
                self.json({"id": did, "status": "created"})
            
            elif path == "/content":
                now = datetime.datetime.now().isoformat()
                execute("INSERT INTO content (title,platform,content_type,status,scheduled_date,body,created_at,updated_at) VALUES (?,?,?,?,?,?,?,?)",
                    (body.get("title",""), body.get("platform",""), body.get("content_type",""),
                     body.get("status","draft"), body.get("scheduled_date",""), body.get("body",""), now, now))
                cnid = query("SELECT last_insert_rowid() as id")[0]["id"]
                log_activity("content", cnid, "created", f"Content: {body.get('title','')}")
                self.json({"id": cnid, "status": "created"})
            
            elif path == "/metrics":
                now = datetime.datetime.now().isoformat()
                execute("INSERT INTO metrics (metric_key,metric_value,label,category,recorded_at) VALUES (?,?,?,?,?)",
                    (body.get("key",""), body.get("value",0), body.get("label",""), body.get("category","general"), now))
                self.json({"status": "recorded"})
            
            elif path == "/seed":
                # Seed sample data for demo
                now = datetime.datetime.now().isoformat()
                sample_contacts = [
                    ("Acme Corp", "contact@acme.com", "555-0100", "Acme Corp", "lead", 50000),
                    ("TechStart Inc", "hello@techstart.io", "555-0101", "TechStart", "qualified", 120000),
                    ("GreenLeaf Co", "info@greenleaf.com", "555-0102", "GreenLeaf", "proposal", 75000),
                ]
                for name, email, phone, company, stage, value in sample_contacts:
                    execute("INSERT INTO contacts (name,email,phone,company,stage,value,created_at,updated_at) VALUES (?,?,?,?,?,?,?,?)",
                        (name, email, phone, company, stage, value, now, now))
                sample_content = [
                    ("Business Analysis Best Practices", "LinkedIn", "article", "scheduled", "2026-06-20"),
                    ("Why Custom Software Beats SaaS", "Medium", "blog", "scheduled", "2026-06-22"),
                    ("ROI of Process Automation", "Twitter/X", "thread", "draft", "2026-06-25"),
                ]
                for title, platform, ctype, status, date in sample_content:
                    execute("INSERT INTO content (title,platform,content_type,status,scheduled_date,created_at,updated_at) VALUES (?,?,?,?,?,?,?)",
                        (title, platform, ctype, status, date, now, now))
                self.json({"status": "seeded", "contacts": 3, "content": 3})
            
            else:
                self.json({"error": "not found"}, 404)
        except Exception as e:
            self.json({"error": str(e)}, 500)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    
    def json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def log_message(self, *args): pass

if __name__ == "__main__":
    init_db()
    server = HTTPServer(("127.0.0.1", PORT), APIHandler)
    print(f"[Open Business Suite] API Server on port {PORT}")
    server.serve_forever()
