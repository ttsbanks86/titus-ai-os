from __future__ import annotations

import csv
import hashlib
import json
import os
import re
from collections import Counter, defaultdict
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "01-Dashboard" / "Vault-Audit-2026-07-12"
EXCLUDED_DIRS = {".git", ".obsidian", ".trash", "node_modules", "Vault-Audit-2026-07-12"}

WIKILINK = re.compile(r"!?(?:\[\[)([^\]|#]+)(?:[#|][^\]]*)?\]\]")
MDLINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
TAG = re.compile(r"(?<![\w/])#([A-Za-z][\w/-]*)")
WORD = re.compile(r"\b[\w'-]+\b")

OWNER_RULES = [
    ("Shared Family", ("family", "household", "kids", "children", "travel", "vehicle", "shared")),
    ("Bonolo", ("bonolo",)),
    ("AI System", ("agent", "jarvis", "prompt", "automation", "ai-", "ai ", "llm", "mcp")),
    ("Business", ("business", "product", "carenotes", "echokeys", "whisper", "customer", "startup")),
    ("Reference Library", ("reference", "knowledge", "research", "resource", "documentation")),
    ("Archive", ("archive", "legacy", "obsolete", "deprecated")),
    ("Titus", ("titus", "career", "resume", "job", "goal", "journal", "daily")),
]

CATEGORY_RULES = [
    ("Daily Note", ("daily", "journal", "2024-", "2025-", "2026-")),
    ("Template", ("template",)), ("AI Agent", ("agent", "jarvis", "prompt", "llm")),
    ("SOP", ("sop", "procedure", "workflow", "playbook")),
    ("Career", ("career", "resume", "job", "interview", "linkedin")),
    ("Education", ("education", "course", "learning", "school", "study")),
    ("Certification", ("certification", "certificate", "exam")),
    ("Business", ("business", "company", "customer", "sales", "marketing")),
    ("Product", ("product", "carenotes", "echokeys", "whisper")),
    ("Project", ("project",)), ("Meeting", ("meeting", "minutes")),
    ("Finance", ("finance", "budget", "money", "tax")),
    ("Health", ("health", "medical", "fitness")), ("Family", ("family", "kids", "household")),
    ("Identity", ("identity", "personal-context", "about me")), ("Goals", ("goal",)),
    ("Research", ("research",)), ("Knowledge", ("knowledge", "note")),
    ("Reference", ("reference", "resource")), ("Archive", ("archive", "legacy")),
]

def files():
    for p in ROOT.rglob("*.md"):
        rel = p.relative_to(ROOT)
        if not any(part in EXCLUDED_DIRS for part in rel.parts):
            yield p

def frontmatter(text: str):
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    raw, body = parts[1], parts[2]
    data, current = {}, None
    for line in raw.splitlines():
        if re.match(r"^[A-Za-z][\w -]*:\s*", line):
            k, v = line.split(":", 1); current = k.strip(); data[current] = v.strip()
        elif current and re.match(r"^\s*-\s+", line):
            val = re.sub(r"^\s*-\s+", "", line).strip()
            old = data.get(current, "")
            data[current] = [old] if old and not isinstance(old, list) else (old or [])
            data[current].append(val)
    return data, body

def classify(haystack: str, rules):
    hits = [(label, sum(haystack.count(x) for x in terms)) for label, terms in rules]
    hits.sort(key=lambda x: x[1], reverse=True)
    if not hits or hits[0][1] == 0 or (len(hits) > 1 and hits[0][1] == hits[1][1]):
        return "Uncertain", 0.0
    return hits[0][0], min(0.98, 0.55 + hits[0][1] * 0.08)

def destination(owner, category, name):
    base = {"Titus":"Titus-Vault", "Bonolo":"Bonolo-Vault", "Shared Family":"Family-Vault",
            "Business":"Businesses", "AI System":"AI-Systems", "Reference Library":"Reference-Library",
            "Archive":"Archive"}.get(owner, "Review-Queue")
    return f"{base}/{category}/{name}.md"

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    paths = list(files())
    stem_index = defaultdict(list)
    for p in paths: stem_index[p.stem.lower()].append(p)
    path_index = {p.relative_to(ROOT).with_suffix("").as_posix().lower(): p for p in paths}
    records, outgoing, hash_groups, attachment_refs = [], defaultdict(set), defaultdict(list), defaultdict(list)
    total_bytes = 0
    for p in paths:
        rel = p.relative_to(ROOT).as_posix(); raw = p.read_text(encoding="utf-8", errors="replace")
        stat = p.stat(); meta, body = frontmatter(raw); total_bytes += stat.st_size
        wiki = [x.strip() for x in WIKILINK.findall(raw)]; mdlinks = MDLINK.findall(raw)
        resolved = set()
        for target in wiki:
            clean_target = target.strip().replace("\\", "/").removesuffix(".md").lower()
            if clean_target in path_index: resolved.add(path_index[clean_target].relative_to(ROOT).as_posix())
            elif Path(clean_target).name in stem_index: resolved.update(x.relative_to(ROOT).as_posix() for x in stem_index[Path(clean_target).name])
            else: attachment_refs[rel].append(target)
        outgoing[rel] = resolved
        normalized = re.sub(r"\s+", " ", body).strip().lower()
        digest = hashlib.sha256(normalized.encode()).hexdigest() if normalized else ""
        if digest: hash_groups[digest].append(rel)
        hay = (rel + " " + raw[:2500]).lower()
        owner, oconf = classify(hay, OWNER_RULES); category, cconf = classify(hay, CATEGORY_RULES)
        tags = sorted(set(TAG.findall(body)))
        yaml_tags = meta.get("tags", [])
        if isinstance(yaml_tags, str) and yaml_tags: tags += [x.strip(" []\"") for x in yaml_tags.split(",")]
        attachments = [x for x in wiki + mdlinks if Path(x.split("#")[0]).suffix.lower() not in ("", ".md")]
        records.append({"path":rel,"name":p.stem,"folder":p.parent.relative_to(ROOT).as_posix(),
          "created":datetime.fromtimestamp(stat.st_ctime).isoformat(timespec="seconds"),
          "modified":datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds"),
          "word_count":len(WORD.findall(body)),"outgoing_links":len(resolved),"backlinks":0,
          "tags":"; ".join(sorted(set(tags))),"yaml":json.dumps(meta, ensure_ascii=False),
          "attachments":"; ".join(attachments),"linked_projects":"; ".join(x for x in wiki if "project" in x.lower()),
          "related_notes":"; ".join(sorted(resolved)),"owner":owner,"owner_confidence":round(oconf,2),
          "category":category,"category_confidence":round(cconf,2),"recommended_location":destination(owner, category, p.stem),
          "risk":"High" if owner == "Uncertain" or category == "Uncertain" else ("Medium" if min(oconf,cconf)<.75 else "Low"),
          "empty":not bool(normalized),"content_hash":digest,"size_bytes":stat.st_size})
    backlinks = Counter(t for targets in outgoing.values() for t in targets)
    for r in records: r["backlinks"] = backlinks[r["path"]]
    exact = [v for v in hash_groups.values() if len(v)>1]
    by_name = defaultdict(list)
    for r in records: by_name[re.sub(r"[^a-z0-9]+", " ", r["name"].lower()).strip()].append(r["path"])
    similar = [v for k,v in by_name.items() if k and len(v)>1]
    conflicting = [g for g in similar if len({next(r["content_hash"] for r in records if r["path"] == p) for p in g}) > 1]
    broken = [(src, target) for src, targets in attachment_refs.items() for target in targets
              if Path(target).suffix.lower() in ("", ".md")]
    fields = list(records[0]) if records else []
    with (OUT/"vault-inventory.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(records)
    with (OUT/"migration-plan.csv").open("w", newline="", encoding="utf-8-sig") as f:
        cols=["path","recommended_location","owner","category","owner_confidence","category_confidence","risk"]
        w=csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows({k:r[k] for k in cols} for r in records)
    owner_counts=Counter(r["owner"] for r in records); cat_counts=Counter(r["category"] for r in records)
    empty=[r for r in records if r["empty"]]; orphans=[r for r in records if r["backlinks"]==0 and r["outgoing_links"]==0]
    untagged=[r for r in records if not r["tags"]]; no_links=[r for r in records if r["outgoing_links"]==0]
    large=[r for r in records if r["word_count"]>=3000]; small=[r for r in records if 0<r["word_count"]<=40]
    uncertain=[r for r in records if r["owner"]=="Uncertain" or r["category"]=="Uncertain"]
    missing_meta=[r for r in records if not r["yaml"] or r["yaml"]=="{}"]
    templates=[r for r in records if r["category"]=="Template" or "template" in r["folder"].lower()]
    unused_templates=[r for r in templates if r["backlinks"]==0]
    all_dirs=[p for p in ROOT.rglob("*") if p.is_dir() and not any(x in EXCLUDED_DIRS for x in p.relative_to(ROOT).parts)]
    unused_folders=[p.relative_to(ROOT).as_posix() for p in all_dirs if not any(x.is_file() for x in p.iterdir())]
    top_connected=sorted(records,key=lambda r:r["backlinks"]+r["outgoing_links"],reverse=True)[:25]
    dup_files=sum(len(x)-1 for x in exact)
    health=max(0,round(100-(len(orphans)/max(1,len(records))*25+len(missing_meta)/max(1,len(records))*25+len(untagged)/max(1,len(records))*15+len(broken)/max(1,len(records))*20+dup_files/max(1,len(records))*15)))
    report = ["---","title: Vault Intelligence Audit","date: 2026-07-12","status: review-required","tags:","  - vault/audit","  - knowledge-management","---","","# Vault Intelligence & Information Architecture Audit","",
      "> [!warning] Audit only\n> No existing note was moved, renamed, merged, deleted, or given metadata. Review and approve the migration plan before any migration.","",
      "## Executive summary","",f"- Notes inventoried: **{len(records):,}**",f"- Overall health score: **{health}/100**",f"- Organization score: **{max(0,100-round(len(orphans)/max(1,len(records))*100))}/100**",f"- Searchability score: **{max(0,100-round(len(no_links)/max(1,len(records))*70+len(untagged)/max(1,len(records))*30))}/100**",f"- Knowledge quality score: **{max(0,100-round(len(empty)/max(1,len(records))*30+len(large)/max(1,len(records))*20+dup_files/max(1,len(records))*50))}/100**",f"- Exact duplicate percentage: **{dup_files/max(1,len(records))*100:.1f}%**",f"- Missing YAML metadata: **{len(missing_meta)/max(1,len(records))*100:.1f}%**",f"- Notes needing classification review: **{len(uncertain):,}**",f"- Estimated cleanup effort: **{round((len(uncertain)*1.5+len(broken)*1+dup_files*3+len(empty)*.5)/60):,} person-hours** (triage estimate)","",
      "## Ownership classification","",* [f"- {k}: {v:,}" for k,v in owner_counts.most_common()],"","## Information categories","",* [f"- {k}: {v:,}" for k,v in cat_counts.most_common()],"",
      "## Problems found","",f"- Exact duplicate groups: **{len(exact):,}** ({dup_files:,} redundant copies)",f"- Same normalized-name groups: **{len(similar):,}**",f"- Conflicting same-name groups: **{len(conflicting):,}**",f"- Empty notes: **{len(empty):,}**",f"- Orphaned notes: **{len(orphans):,}**",f"- Untagged notes: **{len(untagged):,}**",f"- Notes without outgoing links: **{len(no_links):,}**",f"- Potential broken wikilinks: **{len(broken):,}**",f"- Unused templates (no backlinks): **{len(unused_templates):,}**",f"- Empty folders: **{len(unused_folders):,}**",f"- Large notes (3,000+ words): **{len(large):,}**",f"- Very small notes (1-40 words): **{len(small):,}**","",
      "## Relationship analysis","","Most connected notes:","",* [f"- `[[{r['path'][:-3]}]]` — {r['backlinks']} backlinks, {r['outgoing_links']} outgoing" for r in top_connected],"","Primary clusters inferred from content and location:","",* [f"- **{k}:** {v:,} notes" for k,v in cat_counts.most_common()],"","Missing-link candidates are concentrated among same-name groups and notes sharing a category but having no links. These require human review because similarity alone does not prove a relationship.","",
      "## Proposed architecture","","- **Titus-Vault:** Dashboard, Identity, Daily, Projects, Businesses, Career, Education, Knowledge, Journal, Agents.","- **Bonolo-Vault:** Dashboard, Identity, Career, Education, Health, Projects, Daily, Archive.","- **Family-Vault:** Finances, Kids, Household, Vehicles, Travel, Shared Goals, Important Documents, Planning.","- **Businesses:** independent product/company knowledge, separated by business.","- **AI-Systems:** JARVIS, agents, prompts, automations, and AI infrastructure.","- **Reference-Library:** inactive source/reference material.","- **Archive:** obsolete or historical material retained for traceability.","",
      "## Quick wins","","1. Review the uncertain-owner queue before moving anything.","2. Resolve broken links, beginning with notes that have many backlinks.","3. Add a standard metadata schema to active notes only after classification approval.","4. Review exact duplicates by group; retain the best-connected canonical note.","5. Create evergreen hub notes for repeated idea families instead of adding more fragments.","",
      "## Long-term recommendations","","- Use one primary owner and one primary category per note.","- Add `owner`, `area`, `status`, `project`, `priority`, `created`, `updated`, `related`, and `tags` properties.","- Require an ownership decision before note creation or migration.","- Prefer updating an evergreen note when an idea already has a durable home.","- Run this audit periodically and compare results over time.","",
      "## Deliverables","","- [[vault-inventory.csv]] — complete machine-readable inventory.","- [[migration-plan.csv]] — proposed destination, confidence, and risk for every note.","- [[problem-details.md]] — duplicate, broken-link, orphan, empty, large, and merge-candidate details.","","## Approval gate","","> [!todo] Decision required\n> Review the migration plan. No migration should begin until ownership uncertainties and high-risk rows are approved."]
    (OUT/"Vault-Intelligence-Audit.md").write_text("\n".join(report)+"\n", encoding="utf-8")
    details=["# Vault Audit — Problem Details","","> Generated 2026-07-12. Findings are candidates for review, not automatic cleanup decisions.",""]
    def section(title, groups, limit=500):
        details.extend([f"## {title}",""])
        for i,g in enumerate(groups[:limit],1): details.append(f"{i}. " + " · ".join(f"`{x}`" for x in g))
        if len(groups)>limit: details.append(f"\n_Additional groups omitted from this view: {len(groups)-limit:,}. Full note data is in the inventory._")
        details.append("")
    section("Exact duplicate groups", exact); section("Same-name / likely similar groups", similar); section("Conflicting same-name groups", conflicting)
    for title, rows in [("Empty notes",empty),("Orphaned notes",orphans),("Large notes — split candidates",large),("Very small notes — merge candidates",small),("Uncertain classifications",uncertain)]:
        details.extend([f"## {title}",""]+[f"- `{r['path']}`" for r in rows[:1000]]+[""])
    details.extend(["## Potential broken wikilinks",""]+[f"- `{src}` → `[[{target}]]`" for src,target in broken[:2000]]+[""])
    details.extend(["## Unused templates",""]+[f"- `{r['path']}`" for r in unused_templates]+["","## Empty folders",""]+[f"- `{p}`" for p in unused_folders]+[""])
    (OUT/"problem-details.md").write_text("\n".join(details), encoding="utf-8")
    print(json.dumps({"notes":len(records),"health":health,"duplicates":dup_files,"orphans":len(orphans),"broken":len(broken),"uncertain":len(uncertain),"output":str(OUT)},indent=2))

if __name__ == "__main__": main()
