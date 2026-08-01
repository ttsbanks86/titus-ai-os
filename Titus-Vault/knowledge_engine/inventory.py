# knowledge_engine/inventory.py
# Phase B: Knowledge Inventory — catalog all vault content

from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from .config import KnowledgeEngineConfig
from .models import (
    AccessLevel,
    AuthorityRank,
    DocumentMetadata,
    DocumentType,
)


def _parse_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return {}
    end = content.find("---", 3)
    if end == -1:
        return {}
    fm_text = content[3:end].strip()
    result = {}
    for line in fm_text.split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key == "tags":
                # Parse tags list
                value = [t.strip().strip("[]").strip() for t in value.split(",") if t.strip()]
            result[key] = value
    return result


def _extract_wiki_links(content: str) -> list[str]:
    """Extract wiki-links from markdown content."""
    pattern = r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]"
    return list(set(re.findall(pattern, content)))


def _extract_title(content: str, filename: str) -> str:
    """Extract title from content or fallback to filename."""
    for line in content.split("\n")[:20]:
        if line.startswith("# "):
            return line[2:].strip()
    return Path(filename).stem.replace("-", " ").replace("_", " ").title()


def _compute_checksum(filepath: Path) -> str:
    """Compute SHA-256 checksum of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _detect_doc_type(filepath: Path, rel_path: str, content: str) -> DocumentType:
    """Detect document type from path and content."""
    parts = Path(rel_path).parts
    filename = filepath.name.lower()

    if "sop" in filename or "07-SOPs" in parts:
        return DocumentType.SOP
    if "agent" in filename or "08-Agents" in parts:
        return DocumentType.AGENT
    if "06-Projects" in parts:
        return DocumentType.PROJECT
    if "10-Archive" in parts:
        return DocumentType.ARCHIVE
    if "11-Templates" in parts:
        return DocumentType.TEMPLATE
    if "12-Reference" in parts:
        return DocumentType.REFERENCE
    if "01-Dashboard" in parts:
        return DocumentType.DASHBOARD
    if "02-Daily-Notes" in parts:
        return DocumentType.NOTE
    if "09-Knowledge" in parts:
        return DocumentType.REFERENCE
    if filename.startswith("decision") or filename.startswith("decisions"):
        return DocumentType.DECISION
    return DocumentType.NOTE


def _detect_project(rel_path: str) -> str:
    """Detect project name from path."""
    parts = Path(rel_path).parts
    if "06-Projects" in parts:
        idx = parts.index("06-Projects")
        if idx + 1 < len(parts):
            return parts[idx + 1]
    if "09-Knowledge" in parts:
        idx = parts.index("09-Knowledge")
        if idx + 1 < len(parts):
            return parts[idx + 1]
    return "general"


def _detect_access_level(filepath: Path, rel_path: str) -> AccessLevel:
    """Detect access level from path."""
    filename = filepath.name.lower()
    if filename in (".env", ".env.local", ".env.production"):
        return AccessLevel.SECRET
    if "secret" in filename or "credential" in filename:
        return AccessLevel.SECRET
    if "private" in filename or "personal" in filename:
        return AccessLevel.RESTRICTED
    return AccessLevel.PUBLIC


def _is_source_of_truth(rel_path: str, config: KnowledgeEngineConfig) -> bool:
    """Check if a document is source of truth."""
    parts = Path(rel_path).parts
    # Direct files in source of truth directories
    if len(parts) == 2 and parts[0] in config.source_of_truth_dirs:
        return True
    # Specific known source of truth files
    filename = Path(rel_path).name
    sot_files = {"Home.md", "My-Rules.md", "My-Goals.md", "SOPs-Index.md", "Agents-Index.md"}
    return filename in sot_files


def _get_authority(rel_path: str, config: KnowledgeEngineConfig) -> AuthorityRank:
    """Get authority rank from path."""
    authority_str = config.get_authority_for_path(rel_path)
    mapping = {
        "source_of_truth": AuthorityRank.SOURCE_OF_TRUTH,
        "governing": AuthorityRank.GOVERNING,
        "project": AuthorityRank.CURRENT,
        "reference": AuthorityRank.REFERENCE,
        "archived": AuthorityRank.ARCHIVED,
    }
    return mapping.get(authority_str, AuthorityRank.UNKNOWN)


def scan_vault(
    vault_root: Optional[Path] = None,
    config: Optional[KnowledgeEngineConfig] = None,
) -> list[DocumentMetadata]:
    """
    Scan the vault and build a complete inventory of all documents.

    Args:
        vault_root: Root directory of the vault. Defaults to config.
        config: Knowledge engine configuration.

    Returns:
        List of DocumentMetadata for all discoverable documents.
    """
    if config is None:
        config = KnowledgeEngineConfig()
    if vault_root is None:
        vault_root = config.vault_root

    documents = []

    for root, dirs, files in os.walk(vault_root):
        root_path = Path(root)
        rel_root = root_path.relative_to(vault_root)

        # Skip excluded directories
        dirs[:] = [
            d for d in dirs
            if not config.should_exclude_path(str(rel_root / d))
        ]

        for filename in files:
            # Skip excluded files
            if config.should_exclude_file(filename):
                continue

            filepath = root_path / filename
            rel_path = str(rel_root / filename)

            if config.should_exclude_path(rel_path):
                continue

            # Only index markdown and text files for now
            if filepath.suffix.lower() not in (".md", ".txt", ".json", ".yaml", ".yml", ".toml"):
                continue

            try:
                stat = filepath.stat()
                content = filepath.read_text(encoding="utf-8", errors="replace")

                frontmatter = _parse_frontmatter(content)
                wiki_links = _extract_wiki_links(content)
                title = _extract_title(content, filename)
                checksum = _compute_checksum(filepath)

                # Determine fields from frontmatter or auto-detect
                doc_type_str = frontmatter.get("type", "")
                try:
                    doc_type = DocumentType(doc_type_str) if doc_type_str else _detect_doc_type(filepath, rel_path, content)
                except ValueError:
                    doc_type = _detect_doc_type(filepath, rel_path, content)

                project = frontmatter.get("project", "") or _detect_project(rel_path)

                status = frontmatter.get("status", "active")
                is_archived = status == "archived" or "archive" in rel_path.lower()

                tags = frontmatter.get("tags", [])
                if isinstance(tags, str):
                    tags = [t.strip() for t in tags.split(",") if t.strip()]

                created = None
                modified = None
                if frontmatter.get("created"):
                    try:
                        created = datetime.fromisoformat(frontmatter["created"])
                    except (ValueError, TypeError):
                        pass
                if frontmatter.get("updated"):
                    try:
                        modified = datetime.fromisoformat(frontmatter["updated"])
                    except (ValueError, TypeError):
                        pass
                if modified is None:
                    modified = datetime.fromtimestamp(stat.st_mtime)

                doc = DocumentMetadata(
                    path=rel_path,
                    filename=filename,
                    title=title,
                    doc_type=doc_type,
                    project=project,
                    owner=frontmatter.get("owner", "titus"),
                    authority=_get_authority(rel_path, config),
                    tags=tags,
                    created=created,
                    modified=modified,
                    size_bytes=stat.st_size,
                    is_archived=is_archived,
                    is_source_of_truth=_is_source_of_truth(rel_path, config),
                    access_level=_detect_access_level(filepath, rel_path),
                    wiki_links=wiki_links,
                    content_preview=content[:200].replace("\n", " ").strip(),
                    checksum=checksum,
                )
                documents.append(doc)

            except (PermissionError, OSError):
                continue

    return documents


def build_inventory_report(documents: list[DocumentMetadata]) -> dict:
    """Build a summary report of the inventory."""
    by_type = {}
    by_project = {}
    by_authority = {}
    by_access = {}
    archived_count = 0
    sot_count = 0

    for doc in documents:
        by_type[doc.doc_type.value] = by_type.get(doc.doc_type.value, 0) + 1
        by_project[doc.project] = by_project.get(doc.project, 0) + 1
        by_authority[doc.authority.name] = by_authority.get(doc.authority.name, 0) + 1
        by_access[doc.access_level.value] = by_access.get(doc.access_level.value, 0) + 1
        if doc.is_archived:
            archived_count += 1
        if doc.is_source_of_truth:
            sot_count += 1

    return {
        "total_documents": len(documents),
        "by_type": by_type,
        "by_project": by_project,
        "by_authority": by_authority,
        "by_access_level": by_access,
        "archived_count": archived_count,
        "source_of_truth_count": sot_count,
        "scan_time": datetime.now().isoformat(),
    }


def save_inventory(
    documents: list[DocumentMetadata],
    output_path: Path,
) -> None:
    """Save inventory to JSON file."""
    data = []
    for doc in documents:
        data.append({
            "path": doc.path,
            "filename": doc.filename,
            "title": doc.title,
            "doc_type": doc.doc_type.value,
            "project": doc.project,
            "owner": doc.owner,
            "authority": doc.authority.value,
            "tags": doc.tags,
            "created": doc.created.isoformat() if doc.created else None,
            "modified": doc.modified.isoformat() if doc.modified else None,
            "size_bytes": doc.size_bytes,
            "is_archived": doc.is_archived,
            "is_source_of_truth": doc.is_source_of_truth,
            "access_level": doc.access_level.value,
            "wiki_links": doc.wiki_links,
            "content_preview": doc.content_preview,
            "checksum": doc.checksum,
        })
    output_path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def load_inventory(input_path: Path) -> list[DocumentMetadata]:
    """Load inventory from JSON file."""
    data = json.loads(input_path.read_text(encoding="utf-8"))
    documents = []
    for item in data:
        doc = DocumentMetadata(
            path=item["path"],
            filename=item["filename"],
            title=item["title"],
            doc_type=DocumentType(item["doc_type"]),
            project=item["project"],
            owner=item["owner"],
            authority=AuthorityRank(item["authority"]),
            tags=item.get("tags", []),
            created=datetime.fromisoformat(item["created"]) if item.get("created") else None,
            modified=datetime.fromisoformat(item["modified"]) if item.get("modified") else None,
            size_bytes=item.get("size_bytes", 0),
            is_archived=item.get("is_archived", False),
            is_source_of_truth=item.get("is_source_of_truth", False),
            access_level=AccessLevel(item.get("access_level", "public")),
            wiki_links=item.get("wiki_links", []),
            content_preview=item.get("content_preview", ""),
            checksum=item.get("checksum", ""),
        )
        documents.append(doc)
    return documents
