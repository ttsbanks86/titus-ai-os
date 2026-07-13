from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path

USER = Path(r"C:\Users\tbank")
VAULT = Path(r"C:\Users\tbank\Desktop\Live Cowork\Titus-Vault")
OUT = VAULT / "Reference" / "Digital Library Discovery 2026-07-12"

PRIMARY = ["Desktop", "Documents", "Downloads", "Pictures", "Videos", "OneDrive", "Dropbox", "iCloudDrive"]
ADDITIONAL = [
    "AI_Operations", "Brand2Social_Automation", "Career_Source_of_Truth", "Creator_System",
    "Daily_AI_Briefing", "Knowledge_Base", "LeadGen", "OpenCode_Video_Editor", "quizgpt-api",
    "Reports", "telegram-opencode-assistant", "tts", "tvstartupmedia", "Wife_Content_System",
    "workspace", "YouTube_Channel_System", "agent-skills", ".agents", ".floating-ai-tutor",
    ".n8n", ".openclaw", ".opencode", ".openwhispr", ".whisper-flow",
]
ROOTS = [USER / x for x in PRIMARY + ADDITIONAL if (USER / x).exists()]
REPOS = set()

SKIP_DIRS = {
    ".git", ".svn", ".hg", "node_modules", "vendor", "packages", "dist", "build", ".next",
    ".cache", "cache", "caches", "tmp", "temp", "__pycache__", ".pytest_cache", ".mypy_cache",
    ".venv", "venv", "env", ".tox", "coverage", ".idea", ".vscode", "$recycle.bin",
    "windows", "program files", "program files (x86)", "appdata", "system volume information",
    "virtualbox vms", ".obsidian", "digital library discovery 2026-07-12", "_tkos_backups",
}
IMPORTANT_EXT = {
    ".pdf", ".doc", ".docx", ".odt", ".rtf", ".txt", ".md", ".html", ".htm", ".epub",
    ".ppt", ".pptx", ".odp", ".xls", ".xlsx", ".csv", ".tsv", ".json", ".yaml", ".yml",
    ".xml", ".sql", ".db", ".sqlite", ".zip", ".7z", ".rar", ".tar", ".gz",
    ".jpg", ".jpeg", ".png", ".gif", ".webp", ".tif", ".tiff", ".svg", ".heic",
    ".mp3", ".wav", ".m4a", ".flac", ".mp4", ".mov", ".avi", ".mkv", ".webm",
    ".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".cs", ".cpp", ".c", ".h", ".go",
    ".rs", ".php", ".rb", ".ps1", ".sh", ".bat", ".cmd", ".ipynb", ".canvas",
}
EVIDENCE_TERMS = {
    "Education": ["diploma", "transcript", "capstone", "degree plan", "academic calendar", "graduation", "course completion"],
    "Certification": ["pearson vue", "isc2", "comptia", "certificate", "certification", "credly", "score report", "exam registration", "aws", "cisco", "pmi", "scrum"],
    "Career": ["resume", "résumé", "cover letter", "interview", "offer letter", "performance review", "recruiter", "application confirmation", "linkedin", "portfolio", "reference"],
    "Business": ["business plan", "market research", "customer interview", "marketing", "sales", "crm", "operations", "financial plan"],
    "Project": ["requirements", "architecture", "project", "design", "meeting notes", "report", "presentation"],
    "Ministry": ["faithful journey quest", "open door", "struck down but not destroyed", "ministry", "sermon", "teaching", "publishing", "book draft"],
    "Personal": ["award", "volunteer", "identity", "milestone"],
}
LEARNING_PROVIDERS = ["pearson vue", "isc2", "wgu", "mosaic christian college", "coursecareers", "riipen", "aerocardia", "linkedin learning", "microsoft learn", "aws training", "google", "cisco", "comptia", "pmi", "scrum alliance"]
LEARNING_TERMS = ["study", "guide", "exam", "registration", "candidate", "resources", "training", "practice", "handbook", "outline", "objectives", "course", "orientation", "workbook", "ebook", "slides", "labs", "practice test", "domain", "checklist", "curriculum"]
SKILLS = {
    "Business Analysis": ["business analyst", "requirements", "process map", "stakeholder", "sql", "power bi"],
    "Cybersecurity": ["cyber", "isc2", "security", "comptia", "network", "risk"],
    "Leadership": ["leadership", "management", "team"], "AI": [" ai ", "llm", "prompt", "agent", "jarvis", "automation"],
    "Project Management": ["project management", "pmi", "scrum", "agile", "kanban"],
    "Communication": ["communication", "presentation", "writing", "public speaking"],
    "Ministry": ["ministry", "theology", "divinity", "sermon", "biblical"],
}

def walk():
    seen = set()
    count = 0
    for root in ROOTS:
        before = count
        print(f"SCANNING_ROOT={root}", flush=True)
        for base, dirs, files in os.walk(root, topdown=True, followlinks=False):
            p = Path(base)
            if ".git" in dirs: REPOS.add(str(p))
            dirs[:] = [d for d in dirs if d.lower() not in SKIP_DIRS and not (p / d).is_symlink()]
            for name in files:
                f = p / name
                try:
                    key = os.path.normcase(os.path.abspath(str(f)))
                    if key in seen or f.is_symlink() or f.suffix.lower() not in IMPORTANT_EXT: continue
                    seen.add(key); count += 1
                    if count % 50000 == 0: print(f"ENUMERATED={count}", flush=True)
                    yield f
                except OSError: continue
        print(f"ROOT_COMPLETE={root}|FILES={count-before}", flush=True)

def sha256(p):
    try:
        h=hashlib.sha256()
        with p.open("rb") as f:
            for chunk in iter(lambda:f.read(4*1024*1024), b""): h.update(chunk)
        return h.hexdigest(), ""
    except Exception as e: return "", type(e).__name__

def safe_time(value):
    try: return datetime.fromtimestamp(value).isoformat(timespec="seconds")
    except (OSError, OverflowError, ValueError): return ""

def suggest(text):
    t=text.lower()
    if any(x in t for x in ["bonolo", "open door", "struck down but not destroyed", "wife_content"]): return "Bonolo", .96
    if any(x in t for x in ["family", "household", "children", "vehicle", "shared"]): return "Family", .86
    if any(x in t for x in ["jarvis", "agent", "automation", "ai_operations", "llm"]): return "Titus", .82
    if any(x in t for x in ["business", "client", "crm", "sales", "marketing"]): return "Business", .78
    if any(x in t for x in ["course", "book", "tutorial", "reference", "documentation"]): return "Reference", .76
    if any(x in t for x in ["archive", "legacy", "old", "backup"]): return "Archive", .78
    if any(x in t for x in ["career", "resume", "isc2", "divinity", "titus", "portfolio"]): return "Titus", .9
    return "Review", .3

def category(text):
    scores=[]; t=text.lower()
    for cat, terms in EVIDENCE_TERMS.items(): scores.append((sum(t.count(x) for x in terms),cat))
    scores.sort(reverse=True)
    return scores[0][1] if scores and scores[0][0] else "Reference"

def dest(owner, cat, name):
    return f"Digital-Library/{owner}/{cat}/{name}"

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    paths=list(walk()); print(f"DISCOVERED={len(paths)}", flush=True)
    cache_path=OUT/"Checksum Cache.csv"
    cache={}
    if cache_path.exists():
        with cache_path.open(encoding="utf-8-sig",errors="replace") as f:
            for r in csv.DictReader(f): cache[(r["full_path"],r["size_bytes"],r["modified_raw"])]=(r["sha256"],r["hash_error"])
    hashes=[]; missing=[]; missing_idx=[]
    for i,p in enumerate(paths):
        try: s=p.stat(); key=(str(p),str(s.st_size),str(s.st_mtime_ns))
        except OSError: key=(str(p),"","")
        if key in cache: hashes.append(cache[key])
        else: hashes.append(None); missing.append(p); missing_idx.append((i,key))
    print(f"HASH_CACHE_HITS={len(paths)-len(missing)}|TO_HASH={len(missing)}",flush=True)
    with ThreadPoolExecutor(max_workers=6) as ex: new_hashes=list(ex.map(sha256, missing))
    for (i,key),result in zip(missing_idx,new_hashes): hashes[i]=result; cache[key]=result
    with cache_path.open("w",newline="",encoding="utf-8-sig") as f:
        cols=["full_path","size_bytes","modified_raw","sha256","hash_error"]; w=csv.DictWriter(f,fieldnames=cols); w.writeheader()
        for (path,size,mtime),(digest,error) in cache.items(): w.writerow({"full_path":path,"size_bytes":size,"modified_raw":mtime,"sha256":digest,"hash_error":error})
    print(f"HASH_CACHE_SAVED={len(cache)}",flush=True)
    records=[]; folder_stats=defaultdict(lambda:Counter(files=0,bytes=0,review=0)); repos=list(REPOS)
    for p,(digest,error) in zip(paths,hashes):
        try: s=p.stat()
        except OSError: continue
        searchable=(str(p)+" "+p.stem.replace("_"," ").replace("-"," ")).lower()
        owner,conf=suggest(searchable); cat=category(searchable)
        evidence=[k for k,terms in EVIDENCE_TERMS.items() if any(x in searchable for x in terms)]
        provider=next((x for x in LEARNING_PROVIDERS if x in searchable),"")
        learning=bool(provider or any(x in searchable for x in LEARNING_TERMS))
        if "pearson" in searchable and "reschedule" in searchable: learning=False
        skill=next((k for k,v in SKILLS.items() if any(x in searchable for x in v)),"")
        quality="Good" if p.parent.name.lower() in {"education","career","projects","business","portfolio","certifications"} else ("Mixed" if len(set(evidence))>1 else "Unclear")
        folder=str(p.parent); folder_stats[folder]["files"]+=1; folder_stats[folder]["bytes"]+=s.st_size; folder_stats[folder]["review"]+=owner=="Review"
        records.append({"full_path":str(p),"filename":p.name,"extension":p.suffix.lower(),"created":safe_time(s.st_ctime),"modified":safe_time(s.st_mtime),"size_bytes":s.st_size,"sha256":digest,"hash_error":error,"owner_suggestion":owner,"category_suggestion":cat,"confidence":conf,"current_folder_quality":quality,"recommended_destination":dest(owner,cat,p.name),"evidence_types":"; ".join(evidence),"learning_resource":learning,"provider":provider,"skill":skill})
    with (OUT/"Computer Inventory.csv").open("w",newline="",encoding="utf-8-sig") as f:
        w=csv.DictWriter(f,fieldnames=list(records[0]) if records else []); w.writeheader(); w.writerows(records)
    groups=defaultdict(list)
    for r in records:
        if r["sha256"]: groups[r["sha256"]].append(r)
    duplicates=[g for g in groups.values() if len(g)>1]
    names=defaultdict(list)
    for r in records: names[re.sub(r"[^a-z0-9]","",Path(r["filename"]).stem.lower())].append(r)
    versions=[g for g in names.values() if len(g)>1 and len({x["sha256"] for x in g})>1]
    with (OUT/"Duplicate Report.csv").open("w",newline="",encoding="utf-8-sig") as f:
        cols=["group_type","group_id","classification","canonical_suggestion","path","sha256","modified","size_bytes"]
        w=csv.DictWriter(f,fieldnames=cols); w.writeheader()
        for typ,sets in [("Exact",duplicates),("Filename/Version",versions)]:
            for i,g in enumerate(sets,1):
                canonical=max(g,key=lambda x:(x["modified"],x["size_bytes"]))
                for r in g: w.writerow({"group_type":typ,"group_id":f"{typ}-{i}","classification":"Canonical suggestion" if r is canonical else ("Exact duplicate" if typ=="Exact" else "Unknown / updated version review"),"canonical_suggestion":canonical["full_path"],"path":r["full_path"],"sha256":r["sha256"],"modified":r["modified"],"size_bytes":r["size_bytes"]})
    duplicate_by_folder=Counter(str(Path(r["full_path"]).parent) for g in duplicates for r in g)
    folder_rows=[]
    for folder,c in folder_stats.items():
        duplicate_count=duplicate_by_folder[folder]
        review_rate=c["review"]/max(1,c["files"]); score=max(0,round(100-review_rate*45-min(35,duplicate_count*3)-(15 if c["files"]>500 else 0)))
        label="Well-organized" if score>=80 else ("Mixed" if score>=50 else "Review Required")
        folder_rows.append({"folder":folder,"file_count":c["files"],"bytes":c["bytes"],"duplicate_files":duplicate_count,"review_files":c["review"],"health_score":score,"assessment":label})
    with (OUT/"Folder Health Report.csv").open("w",newline="",encoding="utf-8-sig") as f:
        w=csv.DictWriter(f,fieldnames=list(folder_rows[0]) if folder_rows else []); w.writeheader(); w.writerows(sorted(folder_rows,key=lambda x:x["health_score"]))
    evidence=[r for r in records if r["evidence_types"]]
    learning=[r for r in records if r["learning_resource"]]
    resumes=[r for r in records if re.search(r"resume|résumé|cv",r["filename"],re.I)]
    projects=[]
    for repo in sorted(set(repos)):
        p=Path(repo); m=safe_time(p.stat().st_mtime)
        owner,conf=suggest(repo); status="Active" if m and (datetime.now()-datetime.fromtimestamp(p.stat().st_mtime)).days<90 else "Review Required"
        projects.append({"path":repo,"name":p.name,"owner":owner,"confidence":conf,"last_activity":m,"status":status,"recommendation":"Connect to Project Registry; do not promote automatically"})
    def write_csv(name, rows, cols=None):
        with (OUT/name).open("w",newline="",encoding="utf-8-sig") as f:
            cols=cols or (list(rows[0]) if rows else ["result"]); w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)
    write_csv("Evidence Catalog.csv",evidence); write_csv("Professional Development Library.csv",learning)
    write_csv("Project Report.csv",projects); write_csv("Resume Evidence Report.csv",[{**r,"claim_status":"Needs Evidence","recommendation":"Review résumé claims against Evidence Catalog"} for r in resumes])
    cats=Counter(r["category_suggestion"] for r in records); owners=Counter(r["owner_suggestion"] for r in records); ext=Counter(r["extension"] for r in records)
    exact_redundant=sum(len(g)-1 for g in duplicates); hash_errors=sum(bool(r["hash_error"]) for r in records)
    report=["---","title: Master Digital Discovery Executive Summary","date: 2026-07-12","status: review-required","tags:","  - tkos/discovery","  - digital-library","---","","# Master Digital Discovery — Executive Summary","","> [!warning] Recommendations only\n> No original file was moved, renamed, modified, imported, overwritten, or deleted.","","## Scope","",*[f"- `{r}`" for r in ROOTS],"","## Results","",f"- Important files indexed: **{len(records):,}**",f"- Bytes indexed: **{sum(r['size_bytes'] for r in records):,}**",f"- SHA-256 failures: **{hash_errors:,}**",f"- Exact duplicate groups: **{len(duplicates):,}**",f"- Redundant exact copies: **{exact_redundant:,}**",f"- Filename/version review groups: **{len(versions):,}**",f"- Evidence candidates: **{len(evidence):,}**",f"- Learning-resource candidates: **{len(learning):,}**",f"- Résumé versions: **{len(resumes):,}**",f"- Git projects: **{len(projects):,}**","","## Ownership suggestions","",*[f"- {k}: {v:,}" for k,v in owners.most_common()],"","## Evidence categories","",*[f"- {k}: {v:,}" for k,v in cats.most_common()],"","## Recommended permanent library","","1. Evidence","2. Education","3. Career","4. Certifications","5. Employment","6. Projects","7. Business","8. Portfolio","9. AI","10. Ministry","11. Family","12. Reference","13. Historical","14. Archive","","## Recommended review and import order","","1. Evidence","2. Education","3. Career","4. Projects","5. Business","6. Historical archives","","## Known evidence gaps","","- Connected email mailboxes were not available to this local scanner; recruiter emails, confirmations, and provider messages require a separate mailbox audit.","- Résumé claim verification requires human review of each claim against the Evidence Catalog.","- Image similarity beyond exact SHA-256 matches requires a later visual-review pass; no images were modified.","- Document similarity candidates are represented by filename/version groups and require content review.","","## Approval gate","","> [!todo] Stop here\n> Review the discovery reports before importing or reorganizing any original files."]
    (OUT/"Executive Summary.md").write_text("\n".join(report)+"\n",encoding="utf-8")
    report_defs={
      "Education Report.md":"Education", "Certification Report.md":"Certification", "Career Report.md":"Career",
      "Business Report.md":"Business", "AI Systems Report.md":"AI", "Historical Archive Report.md":"Archive",
    }
    for name,term in report_defs.items():
        selected=[r for r in records if term.lower() in (r["category_suggestion"]+" "+r["skill"]+" "+r["owner_suggestion"]+" "+r["full_path"]).lower()]
        lines=[f"# {name[:-3]}","",f"Candidates: **{len(selected):,}**","",* [f"- `{r['full_path']}` — {r['owner_suggestion']} / {r['category_suggestion']} ({r['confidence']:.0%})" for r in selected[:2000]],""]
        (OUT/name).write_text("\n".join(lines),encoding="utf-8")
    gaps=["# Evidence Gap Analysis","",f"- Résumé versions needing claim mapping: **{len(resumes):,}**",f"- Files with ownership confidence below 75%: **{sum(r['confidence']<.75 for r in records):,}**",f"- Files whose checksum could not be read: **{hash_errors:,}**","- Email evidence requires a separate connected-mailbox audit.","- Low-confidence results must remain in Review.",""]
    (OUT/"Evidence Gap Analysis.md").write_text("\n".join(gaps),encoding="utf-8")
    (OUT/"Recommended Import Order.md").write_text("# Recommended Import Order\n\n1. Evidence\n2. Education\n3. Career\n4. Projects\n5. Business\n6. Historical archives\n\nNo import is authorized until the reports are approved.\n",encoding="utf-8")
    (OUT/"Migration Recommendation.md").write_text("# Migration Recommendation\n\nMigrate only reviewed, high-confidence records. Preserve originals, provenance, checksums, and folder history. Use batches of no more than 100 files with link and metadata validation after every batch. Low-confidence items remain in Review.\n",encoding="utf-8")
    print(json.dumps({"files":len(records),"duplicates":len(duplicates),"evidence":len(evidence),"learning":len(learning),"projects":len(projects),"output":str(OUT)},indent=2),flush=True)

if __name__=="__main__": main()
