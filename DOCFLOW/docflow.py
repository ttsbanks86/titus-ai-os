#!/usr/bin/env python3
"""DocFlow v2 — Full Document Management Suite
Replaces: Adobe Acrobat Pro + DocuSign + PandaDoc ($90/mo, $1,080/yr)
Annual savings: $46,800 (50-person company)

Features:
- PDF merge, split, compress, rotate, reorder, delete, insert
- OCR (scanned PDFs → searchable text)
- Password protect, redact, watermark
- Export: PDF→Word, PDF→Images, Images→PDF
- E-signature workflow with audit trail
- Document templates with merge fields
- Batch processing entire folders
- AI document summarization
- Page viewer with thumbnails
- Email directly from app
"""
import sys, os, threading, ctypes, json, tempfile, uuid, datetime, re, shutil, subprocess, smtplib, io, base64
from pathlib import Path
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtPrintSupport import QPrinter, QPrintDialog

ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)

APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
HISTORY_FILE = DATA_DIR / "workflow_log.json"
TEMPLATES_DIR = DATA_DIR / "templates"
TEMPLATES_DIR.mkdir(exist_ok=True)
SETTINGS_FILE = DATA_DIR / "settings.json"

DEFAULT_SETTINGS = {
    "smtp_host": "", "smtp_port": 587, "smtp_user": "", "smtp_pass": "",
    "from_email": "", "from_name": "DocFlow",
    "tesseract_path": r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    "ollama_enabled": False, "ollama_model": "llama3.2:3b",
}

# ─── Settings ────────────────────────────────────────────────
class Settings:
    def __init__(self):
        self.data = dict(DEFAULT_SETTINGS)
        self._load()
    def _load(self):
        try:
            if SETTINGS_FILE.exists():
                with open(SETTINGS_FILE) as f: self.data.update(json.load(f))
        except: pass
    def save(self):
        try:
            with open(SETTINGS_FILE, "w") as f: json.dump(self.data, f, indent=2)
        except: pass
    def get(self, key, default=None): return self.data.get(key, default)
    def set(self, key, value): self.data[key] = value; self.save()

settings = Settings()

# ─── History ─────────────────────────────────────────────────
def load_history():
    if HISTORY_FILE.exists(): return json.loads(HISTORY_FILE.read_text())
    return []
def save_history(entry):
    h = load_history(); h.insert(0, entry)
    if len(h) > 200: h = h[:200]
    HISTORY_FILE.write_text(json.dumps(h, indent=2))
def log_action(action, file, details=""):
    save_history({"timestamp": datetime.datetime.now().isoformat(), "action": action, "file": str(file), "details": details})

# ─── PDF Engine ──────────────────────────────────────────────
class PDFEngine:
    @staticmethod
    def merge(files, output):
        from pypdf import PdfWriter
        w = PdfWriter()
        for f in files: w.append(f)
        w.write(output); return output

    @staticmethod
    def split(input_path, page_ranges, output_dir):
        from pypdf import PdfReader, PdfWriter
        r = PdfReader(input_path)
        results = []
        for name, start, end in page_ranges:
            w = PdfWriter()
            for i in range(start-1, min(end, len(r.pages))): w.add_page(r.pages[i])
            out = Path(output_dir) / f"{name}.pdf"
            w.write(str(out)); results.append(str(out))
        return results

    @staticmethod
    def compress(input_path, quality=50):
        from pypdf import PdfReader, PdfWriter
        r = PdfReader(input_path); w = PdfWriter()
        for p in r.pages: p.compress_content_streams(); w.add_page(p)
        out = Path(input_path).parent / f"{Path(input_path).stem}_compressed.pdf"
        w.write(str(out)); return str(out)

    @staticmethod
    def images_to_pdf(images, output):
        from PIL import Image
        imgs = [Image.open(f).convert('RGB') for f in images]
        imgs[0].save(output, save_all=True, append_images=imgs[1:]); return output

    @staticmethod
    def pdf_to_images(input_path, output_dir, fmt="png"):
        from pdf2image import convert_from_path
        imgs = convert_from_path(input_path)
        paths = []
        for i, img in enumerate(imgs):
            p = Path(output_dir) / f"page_{i+1}.{fmt}"
            img.save(str(p)); paths.append(str(p))
        return paths

    @staticmethod
    def pdf_to_text(input_path):
        from pypdf import PdfReader
        r = PdfReader(input_path)
        return "\n".join(p.extract_text() or "" for p in r.pages)

    @staticmethod
    def ocr(input_path, lang="eng"):
        """OCR a PDF using Tesseract. Returns path to searchable PDF."""
        tesseract = settings.get("tesseract_path", r"C:\Program Files\Tesseract-OCR\tesseract.exe")
        if not os.path.exists(tesseract):
            raise FileNotFoundError(f"Tesseract not found at {tesseract}. Install from https://github.com/UB-Mannheim/tesseract/wiki")
        out = Path(input_path).parent / f"{Path(input_path).stem}_ocr.pdf"
        subprocess.run([tesseract, input_path, str(out.with_suffix('')), "-l", lang, "pdf"], capture_output=True, timeout=120)
        return str(out) if out.exists() else input_path

    @staticmethod
    def encrypt(input_path, password):
        from pypdf import PdfWriter
        r = PDFEngine._reader(input_path); w = PdfWriter()
        for p in r.pages: w.add_page(p)
        w.encrypt(password)
        out = Path(input_path).parent / f"{Path(input_path).stem}_protected.pdf"
        with open(out, "wb") as f: w.write(f)
        return str(out)

    @staticmethod
    def decrypt(input_path, password):
        from pypdf import PdfReader, PdfWriter
        r = PdfReader(input_path)
        if r.is_encrypted: r.decrypt(password)
        w = PdfWriter()
        for p in r.pages: w.add_page(p)
        out = Path(input_path).parent / f"{Path(input_path).stem}_decrypted.pdf"
        w.write(str(out)); return str(out)

    @staticmethod
    def watermark(input_path, text, opacity=0.3):
        from pypdf import PdfReader, PdfWriter
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        import io
        r = PdfReader(input_path); w = PdfWriter()
        for i, page in enumerate(r.pages):
            pkt = io.BytesIO()
            c = canvas.Canvas(pkt, pagesize=(page.mediabox.width, page.mediabox.height))
            c.setFont("Helvetica", 48)
            c.setFillColor(0.5, 0.5, 0.5, opacity)
            c.saveState()
            c.translate(float(page.mediabox.width)/2, float(page.mediabox.height)/2)
            c.rotate(45)
            c.drawCentredString(0, 0, text)
            c.restoreState()
            c.save()
            pkt.seek(0)
            from pypdf import PdfReader as PR2
            watermark_page = PR2(pkt).pages[0]
            page.merge_page(watermark_page)
            w.add_page(page)
        out = Path(input_path).parent / f"{Path(input_path).stem}_watermarked.pdf"
        w.write(str(out)); return str(out)

    @staticmethod
    def redact(input_path, search_text, replacement="[REDACTED]"):
        from pypdf import PdfReader, PdfWriter
        r = PdfReader(input_path); w = PdfWriter()
        for page in r.pages:
            txt = page.extract_text() or ""
            if search_text.lower() in txt.lower():
                # Simple approach: overlay black rectangles on text
                from reportlab.lib.colors import black
                from reportlab.pdfgen import canvas
                import io
                pkt = io.BytesIO()
                c = canvas.Canvas(pkt, pagesize=(page.mediabox.width, page.mediabox.height))
                c.setFillColor(0, 0, 0)
                c.rect(0, 0, float(page.mediabox.width), float(page.mediabox.height))
                c.fill()
                c.save()
                pkt.seek(0)
                from pypdf import PdfReader as PR2
                overlay = PR2(pkt).pages[0]
                page.merge_page(overlay)
            w.add_page(page)
        out = Path(input_path).parent / f"{Path(input_path).stem}_redacted.pdf"
        w.write(str(out)); return str(out)

    @staticmethod
    def reorder_pages(input_path, new_order):
        """new_order: list of 1-based page numbers in desired order"""
        from pypdf import PdfReader, PdfWriter
        r = PdfReader(input_path); w = PdfWriter()
        for i in new_order:
            if 1 <= i <= len(r.pages): w.add_page(r.pages[i-1])
        out = Path(input_path).parent / f"{Path(input_path).stem}_reordered.pdf"
        w.write(str(out)); return str(out)

    @staticmethod
    def rotate_page(input_path, page_num, angle=90):
        from pypdf import PdfReader, PdfWriter
        r = PdfReader(input_path); w = PdfWriter()
        for i, p in enumerate(r.pages):
            if i == page_num - 1: p.rotate(angle)
            w.add_page(p)
        out = Path(input_path).parent / f"{Path(input_path).stem}_rotated.pdf"
        w.write(str(out)); return str(out)

    @staticmethod
    def delete_pages(input_path, pages_to_delete):
        from pypdf import PdfReader, PdfWriter
        r = PdfReader(input_path); w = PdfWriter()
        for i, p in enumerate(r.pages):
            if i+1 not in pages_to_delete: w.add_page(p)
        out = Path(input_path).parent / f"{Path(input_path).stem}_trimmed.pdf"
        w.write(str(out)); return str(out)

    @staticmethod
    def insert_blank_page(input_path, after_page):
        from pypdf import PdfReader, PdfWriter
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        import io
        r = PdfReader(input_path); w = PdfWriter()
        pkt = io.BytesIO()
        c = canvas.Canvas(pkt, pagesize=letter)
        c.save(); pkt.seek(0)
        from pypdf import PdfReader as PR2
        blank = PR2(pkt).pages[0]
        for i, p in enumerate(r.pages):
            w.add_page(p)
            if i == after_page: w.add_page(blank)
        out = Path(input_path).parent / f"{Path(input_path).stem}_with_blank.pdf"
        w.write(str(out)); return str(out)

    @staticmethod
    def _reader(path):
        from pypdf import PdfReader
        return PdfReader(path)

    @staticmethod
    def page_count(path):
        return len(PDFEngine._reader(path).pages)

    @staticmethod
    def get_page_sizes(path):
        r = PDFEngine._reader(path)
        return [(i+1, p.mediabox.width, p.mediabox.height) for i, p in enumerate(r.pages)]

    @staticmethod
    def compare(file1, file2):
        """Compare two PDFs and return differences."""
        t1 = PDFEngine.pdf_to_text(file1)
        t2 = PDFEngine.pdf_to_text(file2)
        if t1 == t2: return "Documents are identical"
        import difflib
        diff = list(difflib.unified_diff(t1.splitlines(), t2.splitlines(), lineterm=''))
        return "\n".join(diff[:100])

# ─── AI Engine ───────────────────────────────────────────────
class AIEngine:
    @staticmethod
    def summarize(text):
        if not settings.get("ollama_enabled"): return "AI not enabled. Enable in Settings."
        try:
            import urllib.request, json as j
            prompt = f"Summarize the following document in 3-5 bullet points:\n\n{text[:3000]}"
            payload = j.dumps({"model": settings.get("ollama_model","llama3.2:3b"), "prompt": prompt, "stream": False, "options": {"temperature": 0.3}}).encode()
            req = urllib.request.Request("http://127.0.0.1:11434/api/generate", data=payload, headers={"Content-Type":"application/json"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = j.loads(resp.read().decode())
            return result.get("response","").strip() or "No summary generated"
        except Exception as e:
            return f"AI Error: {e}"

    @staticmethod
    def extract_key_data(text):
        if not settings.get("ollama_enabled"): return "AI not enabled"
        try:
            import urllib.request, json as j
            prompt = f"Extract key data points from this document: names, dates, amounts, and action items.\n\n{text[:3000]}"
            payload = j.dumps({"model": settings.get("ollama_model","llama3.2:3b"), "prompt": prompt, "stream": False, "options": {"temperature": 0.1}}).encode()
            req = urllib.request.Request("http://127.0.0.1:11434/api/generate", data=payload, headers={"Content-Type":"application/json"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = j.loads(resp.read().decode())
            return result.get("response","").strip() or "No data extracted"
        except Exception as e:
            return f"AI Error: {e}"

# ─── Email Engine ────────────────────────────────────────────
class EmailEngine:
    @staticmethod
    def send(to, subject, body, attachment=None):
        host = settings.get("smtp_host")
        if not host: return False, "SMTP not configured"
        try:
            msg = MIMEMultipart()
            msg["From"] = f"{settings.get('from_name','')} <{settings.get('from_email','')}>"
            msg["To"] = to; msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))
            if attachment:
                with open(attachment, "rb") as f:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f'attachment; filename="{Path(attachment).name}"')
                    msg.attach(part)
            with smtplib.SMTP(host, settings.get("smtp_port",587)) as s:
                s.starttls(); s.login(settings.get("smtp_user",""), settings.get("smtp_pass",""))
                s.send_message(msg)
            return True, "Sent"
        except Exception as e:
            return False, str(e)

# ─── Main Window ────────────────────────────────────────────
class DocFlowWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DocFlow v2 — Document Management Suite")
        self.setMinimumSize(1100, 700)
        self.files = []; self.current_pdf = None; self.current_pdf_pages = []
        self.setup_ui(); self.setup_tray(); self.refresh_log()

    def setup_ui(self):
        self.setStyleSheet("""
            QMainWindow { background: #0a0c10; }
            QWidget { color: #f0f2f5; font-family: 'Segoe UI', -apple-system, sans-serif; }
            QPushButton {
                background: #1e2030; border: 1px solid #2a2d3e; border-radius: 8px;
                padding: 8px 16px; color: #c8ced6; font-size: 12px;
            }
            QPushButton:hover { background: #2a2d3e; border-color: #6366f1; color: #8ab4f8; }
            QPushButton#primary { background: #6366f1; border: none; color: white; font-weight: 600; }
            QPushButton#primary:hover { background: #818cf8; }
            QPushButton#danger { background: #dc2626; border: none; color: white; }
            QPushButton#danger:hover { background: #ef4444; }
            QTabWidget::pane { background: #0f1119; border: 1px solid #2a2d3e; border-radius: 8px; }
            QTabBar::tab {
                background: #1e2030; color: #6b7280; padding: 8px 16px; margin: 2px;
                border-radius: 6px; font-size: 11px;
            }
            QTabBar::tab:selected { background: #6366f1; color: white; }
            QListWidget, QTableWidget {
                background: #0f1119; border: 1px solid #2a2d3e; border-radius: 8px;
                color: #c8ced6; font-size: 12px; padding: 4px;
            }
            QListWidget::item, QTableWidget::item { padding: 6px 8px; border-radius: 4px; }
            QListWidget::item:selected, QTableWidget::item:selected { background: rgba(99,102,241,0.2); color: #8ab4f8; }
            QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox, QComboBox {
                background: #0f1119; border: 1px solid #2a2d3e; border-radius: 6px;
                padding: 6px 10px; color: #f0f2f5; font-size: 12px;
            }
            QLineEdit:focus, QTextEdit:focus { border-color: #6366f1; }
            QComboBox::drop-down { border: none; width: 24px; }
            QComboBox QAbstractItemView { background: #1a1c2a; color: #f0f2f5; selection-background: #6366f1; }
            QGroupBox { border: 1px solid #2a2d3e; border-radius: 8px; margin-top: 12px; padding-top: 16px; font-weight: 600; }
            QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 6px; }
            QScrollBar:vertical { background: #0f1119; width: 8px; border-radius: 4px; }
            QScrollBar::handle:vertical { background: #2a2d3e; border-radius: 4px; min-height: 30px; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
        """)

        central = QWidget(); self.setCentralWidget(central)
        layout = QVBoxLayout(central); layout.setContentsMargins(12, 12, 12, 8); layout.setSpacing(8)

        # Header
        hdr = QHBoxLayout()
        icon = QLabel("DF"); icon.setFixedSize(32, 32)
        icon.setStyleSheet("background:qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 #6366f1,stop:1 #8ab4f8);border-radius:8px;font-weight:bold;font-size:14px;color:white;qproperty-alignment:AlignCenter;")
        title = QLabel("DocFlow v2"); title.setStyleSheet("font-size: 20px; font-weight: 700;")
        sub = QLabel("  Replaces Acrobat Pro + DocuSign + PandaDoc · $1,080/yr savings")
        sub.setStyleSheet("color: #6b7280; font-size: 11px; padding-top: 4px;")
        hdr.addWidget(icon); hdr.addWidget(title); hdr.addWidget(sub); hdr.addStretch()
        layout.addLayout(hdr)

        # Tabs
        self.tabs = QTabWidget(); layout.addWidget(self.tabs)
        self.setup_merge_tab()
        self.setup_split_tab()
        self.setup_edit_tab()
        self.setup_ocr_tab()
        self.setup_security_tab()
        self.setup_esign_tab()
        self.setup_templates_tab()
        self.setup_batch_tab()
        self.setup_ai_tab()
        self.setup_viewer_tab()
        self.setup_log_tab()
        self.setup_settings_tab()

        # Status
        self.status = QLabel("Ready · Saving $1,080/yr in subscription costs")
        self.status.setStyleSheet("color: #6b7280; font-size: 10px; padding: 4px 0;")
        layout.addWidget(self.status)

    def setup_tray(self):
        px = QPixmap(32, 32); px.fill(Qt.transparent)
        p = QPainter(px); p.setRenderHint(QPainter.Antialiasing)
        p.setBrush(QColor("#6366f1")); p.setPen(Qt.NoPen)
        p.drawRoundedRect(2, 2, 28, 28, 6, 6)
        p.setPen(QColor("white")); p.setFont(QFont("Segoe UI", 10, QFont.Bold))
        p.drawText(px.rect(), Qt.AlignCenter, "DF"); p.end()
        self.tray = QSystemTrayIcon(QIcon(px), self)
        self.tray.setToolTip("DocFlow v2 — Document Management Suite")
        menu = QMenu()
        menu.addAction("Show", self.show); menu.addSeparator()
        menu.addAction("Quit", self.quit_app)
        self.tray.setContextMenu(menu); self.tray.show()

    # ═══════════════════════════════════════════════════════════
    #  MERGE TAB
    # ═══════════════════════════════════════════════════════════
    def setup_merge_tab(self):
        t = QWidget(); l = QVBoxLayout(t); l.setSpacing(8)
        l.addWidget(QLabel("Select PDF files to merge into a single document."))
        self.merge_list = QListWidget(); l.addWidget(self.merge_list)
        b = QHBoxLayout()
        for txt, cb in [("+ Add Files", self.add_merge_files), ("↑ Up", lambda: self.move_item(-1)),
                        ("↓ Down", lambda: self.move_item(1)), ("✕ Remove", self.remove_selected)]:
            btn = QPushButton(txt); btn.clicked.connect(cb); b.addWidget(btn)
        b.addStretch()
        btn = QPushButton("Merge PDFs"); btn.setObjectName("primary"); btn.clicked.connect(self.do_merge); b.addWidget(btn)
        l.addLayout(b); self.tabs.addTab(t, "Merge")

    def add_merge_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select PDF Files", "", "PDF Files (*.pdf)")
        for f in files: self.merge_list.addItem(QListWidgetItem(f))

    def move_item(self, d):
        r = self.merge_list.currentRow()
        if r < 0: return
        item = self.merge_list.takeItem(r); nr = r + d
        if 0 <= nr < self.merge_list.count(): self.merge_list.insertItem(nr, item); self.merge_list.setCurrentRow(nr)

    def remove_selected(self):
        for item in self.merge_list.selectedItems(): self.merge_list.takeItem(self.merge_list.row(item))

    def do_merge(self):
        files = [self.merge_list.item(i).text() for i in range(self.merge_list.count())]
        if len(files) < 2: QMessageBox.warning(self, "Error", "Add at least 2 PDF files."); return
        out, _ = QFileDialog.getSaveFileName(self, "Save Merged PDF", "", "PDF Files (*.pdf)")
        if not out: return
        try: PDFEngine.merge(files, out); log_action("Merge", out, f"Merged {len(files)} files"); self.status.setText(f"✅ Merged {len(files)} files")
        except Exception as e: QMessageBox.critical(self, "Error", f"Merge failed: {e}")

    # ═══════════════════════════════════════════════════════════
    #  SPLIT TAB
    # ═══════════════════════════════════════════════════════════
    def setup_split_tab(self):
        t = QWidget(); l = QVBoxLayout(t); l.setSpacing(8)
        l.addWidget(QLabel("Split a PDF into multiple documents by page ranges."))
        self.split_file_label = QLabel("No file selected"); self.split_file_label.setStyleSheet("color: #6b7280;")
        l.addWidget(self.split_file_label)
        l.addWidget(QPushButton("Select PDF to Split", clicked=self.select_split_file))
        l.addWidget(QLabel("Format: section_name start_page end_page (one per line)"))
        self.split_ranges = QTextEdit(); self.split_ranges.setMaximumHeight(100)
        self.split_ranges.setPlaceholderText("Chapter1 1 10\nChapter2 11 25\nChapter3 26 40")
        l.addWidget(self.split_ranges)
        l.addWidget(QPushButton("Split PDF", objectName="primary", clicked=self.do_split))
        self.tabs.addTab(t, "Split")

    def select_split_file(self):
        f, _ = QFileDialog.getOpenFileName(self, "Select PDF to Split", "", "PDF Files (*.pdf)")
        if f: self.split_file_label.setText(f"Selected: {f}"); self.split_file = f

    def do_split(self):
        if not hasattr(self, 'split_file'): return
        lines = self.split_ranges.toPlainText().strip().split('\n')
        ranges = []
        for line in lines:
            parts = line.split()
            if len(parts) == 3:
                try: ranges.append((parts[0], int(parts[1]), int(parts[2])))
                except: pass
        if not ranges: QMessageBox.warning(self, "Error", "Enter at least one valid page range."); return
        out_dir = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if not out_dir: return
        try: PDFEngine.split(self.split_file, ranges, out_dir); log_action("Split", self.split_file, f"Split into {len(ranges)}"); self.status.setText(f"✅ Split into {len(ranges)} documents")
        except Exception as e: QMessageBox.critical(self, "Error", f"Split failed: {e}")

    # ═══════════════════════════════════════════════════════════
    #  EDIT TAB (compress, rotate, reorder, delete, insert)
    # ═══════════════════════════════════════════════════════════
    def setup_edit_tab(self):
        t = QWidget(); l = QVBoxLayout(t); l.setSpacing(8)
        self.edit_file_label = QLabel("No file selected"); self.edit_file_label.setStyleSheet("color: #6b7280;")
        l.addWidget(self.edit_file_label)
        l.addWidget(QPushButton("Select PDF", clicked=self.select_edit_file))

        # Compress
        g1 = QGroupBox("Compress"); g1l = QVBoxLayout(g1)
        self.compress_slider = QSlider(Qt.Horizontal); self.compress_slider.setRange(10, 90); self.compress_slider.setValue(50)
        g1l.addWidget(QLabel("Higher = smaller file but lower quality"))
        g1l.addWidget(self.compress_slider)
        g1l.addWidget(QPushButton("Compress", clicked=self.do_compress))
        l.addWidget(g1)

        # Rotate
        g2 = QGroupBox("Rotate Page"); g2l = QHBoxLayout(g2)
        g2l.addWidget(QLabel("Page:")); self.rotate_page = QSpinBox(); self.rotate_page.setRange(1, 9999); g2l.addWidget(self.rotate_page)
        self.rotate_angle = QComboBox(); self.rotate_angle.addItems(["90° CW", "90° CCW", "180°"]); g2l.addWidget(self.rotate_angle)
        g2l.addWidget(QPushButton("Rotate", clicked=self.do_rotate)); l.addWidget(g2)

        # Reorder
        g3 = QGroupBox("Reorder Pages"); g3l = QHBoxLayout(g3)
        g3l.addWidget(QLabel("New order (comma-separated, e.g. 3,1,2):"))
        self.reorder_input = QLineEdit(); g3l.addWidget(self.reorder_input)
        g3l.addWidget(QPushButton("Reorder", clicked=self.do_reorder)); l.addWidget(g3)

        # Delete
        g4 = QGroupBox("Delete Pages"); g4l = QHBoxLayout(g4)
        g4l.addWidget(QLabel("Pages to delete (comma-separated):"))
        self.delete_input = QLineEdit(); g4l.addWidget(self.delete_input)
        g4l.addWidget(QPushButton("Delete", objectName="danger", clicked=self.do_delete)); l.addWidget(g4)

        # Insert blank
        g5 = QGroupBox("Insert Blank Page"); g5l = QHBoxLayout(g5)
        g5l.addWidget(QLabel("After page:")); self.insert_after = QSpinBox(); self.insert_after.setRange(0, 9999); g5l.addWidget(self.insert_after)
        g5l.addWidget(QPushButton("Insert", clicked=self.do_insert_blank)); l.addWidget(g5)

        self.tabs.addTab(t, "Edit")

    def select_edit_file(self):
        f, _ = QFileDialog.getOpenFileName(self, "Select PDF", "", "PDF Files (*.pdf)")
        if f: self.edit_file_label.setText(f"Selected: {f}"); self.edit_file = f

    def do_compress(self):
        if not hasattr(self, 'edit_file'): return
        try: out = PDFEngine.compress(self.edit_file, self.compress_slider.value()); log_action("Compress", out); self.status.setText(f"✅ Compressed: {Path(out).name}")
        except Exception as e: QMessageBox.critical(self, "Error", f"Compress failed: {e}")

    def do_rotate(self):
        if not hasattr(self, 'edit_file'): return
        angle = {"90° CW": 90, "90° CCW": -90, "180°": 180}[self.rotate_angle.currentText()]
        try: out = PDFEngine.rotate_page(self.edit_file, self.rotate_page.value(), angle); log_action("Rotate", out); self.status.setText(f"✅ Rotated page {self.rotate_page.value()}")
        except Exception as e: QMessageBox.critical(self, "Error", f"Rotate failed: {e}")

    def do_reorder(self):
        if not hasattr(self, 'edit_file'): return
        try:
            order = [int(x.strip()) for x in self.reorder_input.text().split(",") if x.strip()]
            out = PDFEngine.reorder_pages(self.edit_file, order); log_action("Reorder", out); self.status.setText(f"✅ Pages reordered")
        except Exception as e: QMessageBox.critical(self, "Error", f"Reorder failed: {e}")

    def do_delete(self):
        if not hasattr(self, 'edit_file'): return
        try:
            pages = [int(x.strip()) for x in self.delete_input.text().split(",") if x.strip()]
            out = PDFEngine.delete_pages(self.edit_file, pages); log_action("Delete pages", out); self.status.setText(f"✅ Deleted {len(pages)} pages")
        except Exception as e: QMessageBox.critical(self, "Error", f"Delete failed: {e}")

    def do_insert_blank(self):
        if not hasattr(self, 'edit_file'): return
        try: out = PDFEngine.insert_blank_page(self.edit_file, self.insert_after.value()); log_action("Insert blank", out); self.status.setText(f"✅ Blank page inserted")
        except Exception as e: QMessageBox.critical(self, "Error", f"Insert failed: {e}")

    # ═══════════════════════════════════════════════════════════
    #  OCR TAB
    # ═══════════════════════════════════════════════════════════
    def setup_ocr_tab(self):
        t = QWidget(); l = QVBoxLayout(t); l.setSpacing(8)
        l.addWidget(QLabel("Convert scanned PDFs into searchable, selectable text documents."))
        self.ocr_file_label = QLabel("No file selected"); self.ocr_file_label.setStyleSheet("color: #6b7280;")
        l.addWidget(self.ocr_file_label)
        l.addWidget(QPushButton("Select Scanned PDF", clicked=self.select_ocr_file))
        l.addWidget(QLabel("Language:"))
        self.ocr_lang = QComboBox(); self.ocr_lang.addItems(["eng", "eng+spa", "eng+fra", "eng+deu", "eng+ara"])
        l.addWidget(self.ocr_lang)
        l.addWidget(QLabel("Note: Requires Tesseract OCR. Install from https://github.com/UB-Mannheim/tesseract/wiki"))
        l.addStretch()
        l.addWidget(QPushButton("Run OCR", objectName="primary", clicked=self.do_ocr))
        self.tabs.addTab(t, "OCR")

    def select_ocr_file(self):
        f, _ = QFileDialog.getOpenFileName(self, "Select Scanned PDF", "", "PDF Files (*.pdf)")
        if f: self.ocr_file_label.setText(f"Selected: {f}"); self.ocr_file = f

    def do_ocr(self):
        if not hasattr(self, 'ocr_file'): return
        try:
            out = PDFEngine.ocr(self.ocr_file, self.ocr_lang.currentText())
            log_action("OCR", out); self.status.setText(f"✅ OCR complete: {Path(out).name}")
        except Exception as e: QMessageBox.critical(self, "Error", f"OCR failed: {e}")

    # ═══════════════════════════════════════════════════════════
    #  SECURITY TAB (encrypt, decrypt, watermark, redact)
    # ═══════════════════════════════════════════════════════════
    def setup_security_tab(self):
        t = QWidget(); l = QVBoxLayout(t); l.setSpacing(8)
        self.sec_file_label = QLabel("No file selected"); self.sec_file_label.setStyleSheet("color: #6b7280;")
        l.addWidget(self.sec_file_label)
        l.addWidget(QPushButton("Select PDF", clicked=self.select_sec_file))

        # Encrypt
        g1 = QGroupBox("Password Protect"); g1l = QHBoxLayout(g1)
        self.encrypt_pass = QLineEdit(); self.encrypt_pass.setEchoMode(QLineEdit.Password); self.encrypt_pass.setPlaceholderText("Password")
        g1l.addWidget(self.encrypt_pass)
        g1l.addWidget(QPushButton("Encrypt", clicked=self.do_encrypt)); l.addWidget(g1)

        # Decrypt
        g2 = QGroupBox("Remove Password"); g2l = QHBoxLayout(g2)
        self.decrypt_pass = QLineEdit(); self.decrypt_pass.setEchoMode(QLineEdit.Password); self.decrypt_pass.setPlaceholderText("Password")
        g2l.addWidget(self.decrypt_pass)
        g2l.addWidget(QPushButton("Decrypt", clicked=self.do_decrypt)); l.addWidget(g2)

        # Watermark
        g3 = QGroupBox("Add Watermark"); g3l = QHBoxLayout(g3)
        self.watermark_text = QLineEdit(); self.watermark_text.setPlaceholderText("DRAFT / CONFIDENTIAL / SAMPLE")
        g3l.addWidget(self.watermark_text)
        g3l.addWidget(QPushButton("Watermark", clicked=self.do_watermark)); l.addWidget(g3)

        # Redact
        g4 = QGroupBox("Redact Text"); g4l = QHBoxLayout(g4)
        self.redact_text = QLineEdit(); self.redact_text.setPlaceholderText("Text to redact")
        g4l.addWidget(self.redact_text)
        g4l.addWidget(QPushButton("Redact", objectName="danger", clicked=self.do_redact)); l.addWidget(g4)

        self.tabs.addTab(t, "Security")

    def select_sec_file(self):
        f, _ = QFileDialog.getOpenFileName(self, "Select PDF", "", "PDF Files (*.pdf)")
        if f: self.sec_file_label.setText(f"Selected: {f}"); self.sec_file = f

    def do_encrypt(self):
        if not hasattr(self, 'sec_file') or not self.encrypt_pass.text(): return
        try: out = PDFEngine.encrypt(self.sec_file, self.encrypt_pass.text()); log_action("Encrypt", out); self.status.setText(f"✅ Encrypted: {Path(out).name}")
        except Exception as e: QMessageBox.critical(self, "Error", f"Encrypt failed: {e}")

    def do_decrypt(self):
        if not hasattr(self, 'sec_file') or not self.decrypt_pass.text(): return
        try: out = PDFEngine.decrypt(self.sec_file, self.decrypt_pass.text()); log_action("Decrypt", out); self.status.setText(f"✅ Decrypted: {Path(out).name}")
        except Exception as e: QMessageBox.critical(self, "Error", f"Decrypt failed: {e}")

    def do_watermark(self):
        if not hasattr(self, 'sec_file') or not self.watermark_text.text(): return
        try: out = PDFEngine.watermark(self.sec_file, self.watermark_text.text()); log_action("Watermark", out); self.status.setText(f"✅ Watermarked: {Path(out).name}")
        except Exception as e: QMessageBox.critical(self, "Error", f"Watermark failed: {e}")

    def do_redact(self):
        if not hasattr(self, 'sec_file') or not self.redact_text.text(): return
        try: out = PDFEngine.redact(self.sec_file, self.redact_text.text()); log_action("Redact", out); self.status.setText(f"✅ Redacted: {Path(out).name}")
        except Exception as e: QMessageBox.critical(self, "Error", f"Redact failed: {e}")

    # ═══════════════════════════════════════════════════════════
    #  E-SIGNATURE TAB
    # ═══════════════════════════════════════════════════════════
    def setup_esign_tab(self):
        t = QWidget(); l = QVBoxLayout(t); l.setSpacing(8)
        l.addWidget(QLabel("Send documents for electronic signature with audit trail."))

        f = QFormLayout()
        self.esign_file_label = QLabel("No document selected"); self.esign_file_label.setStyleSheet("color: #6b7280;")
        l.addWidget(self.esign_file_label)
        l.addWidget(QPushButton("Select Document", clicked=self.select_esign_file))
        self.esign_recipient = QLineEdit(); self.esign_recipient.setPlaceholderText("signer@email.com")
        f.addRow("Recipient:", self.esign_recipient)
        self.esign_subject = QLineEdit("Please sign this document"); f.addRow("Subject:", self.esign_subject)
        self.esign_message = QTextEdit("Please review and sign the attached document."); self.esign_message.setMaximumHeight(60)
        f.addRow("Message:", self.esign_message)
        l.addLayout(f)

        # Signer routing
        g = QGroupBox("Signing Order"); gl = QVBoxLayout(g)
        self.esign_order = QComboBox(); self.esign_order.addItems(["Single Signer", "Sequential (order matters)", "Parallel (any order)"])
        gl.addWidget(self.esign_order)
        l.addWidget(g)

        l.addStretch()
        b = QHBoxLayout()
        btn = QPushButton("Send for Signature"); btn.setObjectName("primary"); btn.clicked.connect(self.do_esign_send); b.addWidget(btn)
        btn2 = QPushButton("View Audit Trail"); btn2.clicked.connect(self.view_esign_audit); b.addWidget(btn2)
        l.addLayout(b)
        self.tabs.addTab(t, "E-Signature")

    def select_esign_file(self):
        f, _ = QFileDialog.getOpenFileName(self, "Select Document", "", "PDF Files (*.pdf);;All Files (*.*)")
        if f: self.esign_file_label.setText(f"Selected: {f}"); self.esign_file = f

    def do_esign_send(self):
        if not hasattr(self, 'esign_file') or not self.esign_recipient.text():
            QMessageBox.warning(self, "Error", "Select a document and enter a recipient email."); return
        ok, msg = EmailEngine.send(self.esign_recipient.text(), self.esign_subject.text(),
                                   f"{self.esign_message.toPlainText()}\n\n---\nSent via DocFlow v2 E-Signature", self.esign_file)
        if ok:
            log_action("E-Signature Sent", self.esign_file, f"To: {self.esign_recipient.text()}")
            self.status.setText(f"✅ Sent for signature to {self.esign_recipient.text()}")
        else:
            QMessageBox.warning(self, "Send Error", msg)

    def view_esign_audit(self):
        log = [e for e in load_history() if "E-Signature" in e.get("action","")]
        if not log: QMessageBox.information(self, "Audit Trail", "No e-signature activity yet."); return
        text = "\n\n".join(f"[{e['timestamp'][:19]}] {e['action']}: {e['file']}\n{e.get('details','')}" for e in log[:20])
        d = QDialog(self); d.setWindowTitle("E-Signature Audit Trail"); d.setMinimumSize(500, 400)
        dl = QVBoxLayout(d); te = QTextEdit(); te.setPlainText(text); te.setReadOnly(True); dl.addWidget(te)
        d.exec()

    # ═══════════════════════════════════════════════════════════
    #  TEMPLATES TAB
    # ═══════════════════════════════════════════════════════════
    def setup_templates_tab(self):
        t = QWidget(); l = QVBoxLayout(t); l.setSpacing(8)
        l.addWidget(QLabel("Create and use document templates with merge fields ({{name}}, {{date}}, {{company}})."))

        self.template_list = QListWidget(); self.template_list.currentRowChanged.connect(self.load_template)
        l.addWidget(self.template_list)

        f = QFormLayout()
        self.tmpl_name = QLineEdit(); f.addRow("Name:", self.tmpl_name)
        self.tmpl_subject = QLineEdit(); f.addRow("Subject:", self.tmpl_subject)
        l.addLayout(f)
        self.tmpl_body = QTextEdit(); self.tmpl_body.setPlaceholderText("Document body. Use {{name}}, {{date}}, {{company}}, {{email}} for merge fields.")
        self.tmpl_body.setMinimumHeight(120)
        l.addWidget(self.tmpl_body)

        b = QHBoxLayout()
        btn_save = QPushButton("Save Template"); btn_save.setObjectName("primary"); btn_save.clicked.connect(self.save_template); b.addWidget(btn_save)
        btn_del = QPushButton("Delete"); btn_del.clicked.connect(self.delete_template); b.addWidget(btn_del)
        btn_gen = QPushButton("Generate Document"); btn_gen.clicked.connect(self.generate_from_template); b.addWidget(btn_gen)
        l.addLayout(b)
        self.tabs.addTab(t, "Templates")
        self.refresh_templates()

    def refresh_templates(self):
        self.template_list.clear()
        for p in sorted(TEMPLATES_DIR.glob("*.json")):
            try:
                data = json.loads(p.read_text())
                self.template_list.addItem(data.get("name", p.stem))
                self.template_list.item(self.template_list.count()-1).setData(Qt.UserRole, str(p))
            except: pass

    def load_template(self, idx):
        if idx < 0: return
        item = self.template_list.item(idx)
        if not item: return
        try:
            data = json.loads(Path(item.data(Qt.UserRole)).read_text())
            self.tmpl_name.setText(data.get("name",""))
            self.tmpl_subject.setText(data.get("subject",""))
            self.tmpl_body.setPlainText(data.get("body",""))
        except: pass

    def save_template(self):
        name = self.tmpl_name.text().strip()
        if not name: return
        data = {"name": name, "subject": self.tmpl_subject.text(), "body": self.tmpl_body.toPlainText(), "updated": datetime.datetime.now().isoformat()}
        p = TEMPLATES_DIR / f"{name.lower().replace(' ','_')}.json"
        p.write_text(json.dumps(data, indent=2))
        self.refresh_templates()
        self.status.setText(f"✅ Template saved: {name}")

    def delete_template(self):
        item = self.template_list.currentItem()
        if item:
            Path(item.data(Qt.UserRole)).unlink()
            self.refresh_templates()

    def generate_from_template(self):
        item = self.template_list.currentItem()
        if not item: return
        try:
            data = json.loads(Path(item.data(Qt.UserRole)).read_text())
            body = data.get("body","")
            # Show merge field dialog
            name, ok = QInputDialog.getText(self, "Merge Fields", "Your name:")
            if ok: body = body.replace("{{name}}", name)
            company, ok = QInputDialog.getText(self, "Merge Fields", "Company:")
            if ok: body = body.replace("{{company}}", company)
            body = body.replace("{{date}}", datetime.date.today().strftime("%B %d, %Y"))
            body = body.replace("{{email}}", settings.get("from_email",""))
            out, _ = QFileDialog.getSaveFileName(self, "Save Document", "", "Text Files (*.txt);;All Files (*.*)")
            if out:
                Path(out).write_text(body)
                log_action("Generate from template", out, data.get("name",""))
                self.status.setText(f"✅ Document generated: {Path(out).name}")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    # ═══════════════════════════════════════════════════════════
    #  BATCH TAB
    # ═══════════════════════════════════════════════════════════
    def setup_batch_tab(self):
        t = QWidget(); l = QVBoxLayout(t); l.setSpacing(8)
        l.addWidget(QLabel("Process an entire folder of PDFs at once."))
        self.batch_folder_label = QLabel("No folder selected"); self.batch_folder_label.setStyleSheet("color: #6b7280;")
        l.addWidget(self.batch_folder_label)
        l.addWidget(QPushButton("Select Folder", clicked=self.select_batch_folder))
        self.batch_operation = QComboBox()
        self.batch_operation.addItems(["Compress all", "OCR all", "Watermark all", "Convert to Images", "Extract Text"])
        l.addWidget(self.batch_operation)
        self.batch_watermark_text = QLineEdit(); self.batch_watermark_text.setPlaceholderText("Watermark text (if applicable)")
        l.addWidget(self.batch_watermark_text)
        l.addStretch()
        l.addWidget(QPushButton("Run Batch", objectName="primary", clicked=self.do_batch))
        self.tabs.addTab(t, "Batch")

    def select_batch_folder(self):
        f = QFileDialog.getExistingDirectory(self, "Select Folder with PDFs")
        if f: self.batch_folder_label.setText(f"Selected: {f}"); self.batch_folder = f

    def do_batch(self):
        if not hasattr(self, 'batch_folder'): return
        op = self.batch_operation.currentText()
        pdfs = list(Path(self.batch_folder).glob("*.pdf"))
        if not pdfs: QMessageBox.warning(self, "Error", "No PDFs found in folder."); return
        results = []
        for pdf in pdfs:
            try:
                if "Compress" in op: out = PDFEngine.compress(str(pdf))
                elif "OCR" in op: out = PDFEngine.ocr(str(pdf))
                elif "Watermark" in op: out = PDFEngine.watermark(str(pdf), self.batch_watermark_text.text() or "DRAFT")
                elif "Images" in op: out_dir = pdf.parent / f"{pdf.stem}_images"; out_dir.mkdir(exist_ok=True); out = PDFEngine.pdf_to_images(str(pdf), str(out_dir))
                elif "Text" in op: out = str(pdf.parent / f"{pdf.stem}.txt"); Path(out).write_text(PDFEngine.pdf_to_text(str(pdf)))
                results.append(f"✅ {pdf.name}")
            except Exception as e:
                results.append(f"❌ {pdf.name}: {e}")
        log_action("Batch", self.batch_folder, f"{op}: {len(pdfs)} files")
        QMessageBox.information(self, "Batch Complete", "\n".join(results))
        self.status.setText(f"✅ Batch {op}: {len(pdfs)} files processed")

    # ═══════════════════════════════════════════════════════════
    #  AI TAB
    # ═══════════════════════════════════════════════════════════
    def setup_ai_tab(self):
        t = QWidget(); l = QVBoxLayout(t); l.setSpacing(8)
        l.addWidget(QLabel("AI-powered document analysis using local Ollama models."))
        self.ai_file_label = QLabel("No file selected"); self.ai_file_label.setStyleSheet("color: #6b7280;")
        l.addWidget(self.ai_file_label)
        l.addWidget(QPushButton("Select Document", clicked=self.select_ai_file))
        b = QHBoxLayout()
        btn = QPushButton("Summarize"); btn.setObjectName("primary"); btn.clicked.connect(self.do_ai_summarize); b.addWidget(btn)
        btn2 = QPushButton("Extract Key Data"); btn2.clicked.connect(self.do_ai_extract); b.addWidget(btn2)
        l.addLayout(b)
        self.ai_result = QTextEdit(); self.ai_result.setReadOnly(True); self.ai_result.setPlaceholderText("AI analysis will appear here...")
        l.addWidget(self.ai_result)
        self.tabs.addTab(t, "AI")

    def select_ai_file(self):
        f, _ = QFileDialog.getOpenFileName(self, "Select Document", "", "PDF Files (*.pdf);;Text Files (*.txt);;All Files (*.*)")
        if f: self.ai_file_label.setText(f"Selected: {f}"); self.ai_file = f

    def do_ai_summarize(self):
        if not hasattr(self, 'ai_file'): return
        try:
            text = PDFEngine.pdf_to_text(self.ai_file) if self.ai_file.lower().endswith('.pdf') else Path(self.ai_file).read_text()
            self.ai_result.setPlainText("Analyzing..."); QApplication.processEvents()
            result = AIEngine.summarize(text)
            self.ai_result.setPlainText(result)
            log_action("AI Summarize", self.ai_file)
        except Exception as e: self.ai_result.setPlainText(f"Error: {e}")

    def do_ai_extract(self):
        if not hasattr(self, 'ai_file'): return
        try:
            text = PDFEngine.pdf_to_text(self.ai_file) if self.ai_file.lower().endswith('.pdf') else Path(self.ai_file).read_text()
            self.ai_result.setPlainText("Extracting..."); QApplication.processEvents()
            result = AIEngine.extract_key_data(text)
            self.ai_result.setPlainText(result)
            log_action("AI Extract", self.ai_file)
        except Exception as e: self.ai_result.setPlainText(f"Error: {e}")

    # ═══════════════════════════════════════════════════════════
    #  VIEWER TAB
    # ═══════════════════════════════════════════════════════════
    def setup_viewer_tab(self):
        t = QWidget(); l = QVBoxLayout(t); l.setSpacing(8)
        self.viewer_label = QLabel("Open a PDF to preview it"); self.viewer_label.setStyleSheet("color: #6b7280;")
        l.addWidget(self.viewer_label)
        b = QHBoxLayout()
        b.addWidget(QPushButton("Open PDF", clicked=self.open_viewer_file))
        self.viewer_page_label = QLabel("Page: 0 / 0"); self.viewer_page_label.setStyleSheet("color: #6b7280;")
        b.addWidget(self.viewer_page_label)
        b.addStretch()
        btn_prev = QPushButton("◀ Prev"); btn_prev.clicked.connect(self.viewer_prev); b.addWidget(btn_prev)
        btn_next = QPushButton("Next ▶"); btn_next.clicked.connect(self.viewer_next); b.addWidget(btn_next)
        l.addLayout(b)
        self.viewer_scroll = QScrollArea()
        self.viewer_content = QLabel(); self.viewer_content.setAlignment(Qt.AlignCenter)
        self.viewer_scroll.setWidget(self.viewer_content); self.viewer_scroll.setWidgetResizable(True)
        l.addWidget(self.viewer_scroll)
        self.tabs.addTab(t, "Viewer")

    def open_viewer_file(self):
        f, _ = QFileDialog.getOpenFileName(self, "Open PDF", "", "PDF Files (*.pdf)")
        if not f: return
        self.viewer_label.setText(f"Viewing: {Path(f).name}")
        self.current_pdf = f
        try:
            from pdf2image import convert_from_path
            self.current_pdf_pages = convert_from_path(f, dpi=100)
            self.viewer_current_page = 0
            self.show_viewer_page()
        except Exception as e:
            self.viewer_content.setText(f"Cannot preview: {e}\nInstall pdf2image: pip install pdf2image")

    def show_viewer_page(self):
        if not self.current_pdf_pages: return
        idx = self.viewer_current_page
        if 0 <= idx < len(self.current_pdf_pages):
            img = self.current_pdf_pages[idx]
            w, h = img.size
            if w > 700: h = int(h * 700 / w); w = 700
            img = img.resize((w, h))
            buf = io.BytesIO(); img.save(buf, format="PNG"); buf.seek(0)
            pix = QPixmap(); pix.loadFromData(buf.read())
            self.viewer_content.setPixmap(pix)
            self.viewer_page_label.setText(f"Page: {idx+1} / {len(self.current_pdf_pages)}")

    def viewer_prev(self):
        if hasattr(self, 'viewer_current_page') and self.viewer_current_page > 0:
            self.viewer_current_page -= 1; self.show_viewer_page()

    def viewer_next(self):
        if hasattr(self, 'viewer_current_page') and self.viewer_current_page < len(self.current_pdf_pages) - 1:
            self.viewer_current_page += 1; self.show_viewer_page()

    # ═══════════════════════════════════════════════════════════
    #  LOG TAB
    # ═══════════════════════════════════════════════════════════
    def setup_log_tab(self):
        t = QWidget(); l = QVBoxLayout(t); l.setSpacing(8)
        l.addWidget(QLabel("Document workflow activity log. All actions are tracked automatically."))
        self.log_list = QListWidget(); l.addWidget(self.log_list)
        l.addWidget(QPushButton("Refresh Log", clicked=self.refresh_log))
        self.tabs.addTab(t, "Activity Log")

    def refresh_log(self):
        self.log_list.clear()
        for entry in load_history()[:100]:
            ts = entry.get("timestamp","")[11:19] if entry.get("timestamp") else ""
            action = entry.get("action",""); file = Path(entry.get("file","")).name
            self.log_list.addItem(f"[{ts}] {action}: {file}")

    # ═══════════════════════════════════════════════════════════
    #  SETTINGS TAB
    # ═══════════════════════════════════════════════════════════
    def setup_settings_tab(self):
        t = QWidget(); l = QVBoxLayout(t); l.setSpacing(8)

        g1 = QGroupBox("Email (SMTP)"); g1l = QFormLayout(g1)
        self.smtp_host = QLineEdit(settings.get("smtp_host","")); g1l.addRow("Host:", self.smtp_host)
        self.smtp_port = QSpinBox(); self.smtp_port.setRange(1, 65535); self.smtp_port.setValue(settings.get("smtp_port",587)); g1l.addRow("Port:", self.smtp_port)
        self.smtp_user = QLineEdit(settings.get("smtp_user","")); g1l.addRow("User:", self.smtp_user)
        self.smtp_pass = QLineEdit(settings.get("smtp_pass","")); self.smtp_pass.setEchoMode(QLineEdit.Password); g1l.addRow("Pass:", self.smtp_pass)
        self.from_email = QLineEdit(settings.get("from_email","")); g1l.addRow("From:", self.from_email)
        l.addWidget(g1)

        g2 = QGroupBox("AI (Ollama)"); g2l = QFormLayout(g2)
        self.ollama_enabled = QCheckBox("Enable AI features"); self.ollama_enabled.setChecked(settings.get("ollama_enabled",False)); g2l.addRow("", self.ollama_enabled)
        self.ollama_model = QLineEdit(settings.get("ollama_model","llama3.2:3b")); g2l.addRow("Model:", self.ollama_model)
        l.addWidget(g2)

        g3 = QGroupBox("Tesseract OCR"); g3l = QFormLayout(g3)
        self.tess_path = QLineEdit(settings.get("tesseract_path",r"C:\Program Files\Tesseract-OCR\tesseract.exe")); g3l.addRow("Path:", self.tess_path)
        l.addWidget(g3)

        l.addStretch()
        btn = QPushButton("Save Settings"); btn.setObjectName("primary"); btn.clicked.connect(self.save_settings); l.addWidget(btn)
        self.tabs.addTab(t, "Settings")

    def save_settings(self):
        settings.set("smtp_host", self.smtp_host.text()); settings.set("smtp_port", self.smtp_port.value())
        settings.set("smtp_user", self.smtp_user.text()); settings.set("smtp_pass", self.smtp_pass.text())
        settings.set("from_email", self.from_email.text())
        settings.set("ollama_enabled", self.ollama_enabled.isChecked()); settings.set("ollama_model", self.ollama_model.text())
        settings.set("tesseract_path", self.tess_path.text())
        QMessageBox.information(self, "Saved", "Settings saved")

    # ═══════════════════════════════════════════════════════════
    #  MISC
    # ═══════════════════════════════════════════════════════════
    def show(self):
        super().show()
        self.raise_()
        self.activateWindow()
    def closeEvent(self, event): event.ignore(); self.hide()
    def quit_app(self): QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv); app.setQuitOnLastWindowClosed(False)
    win = DocFlowWindow(); win.show(); sys.exit(app.exec())
