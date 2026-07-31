"""
Titus AI OS Indexing — Manual Incremental Indexer

Gate E: Reclassified from "AutoIndexer" to "ManualIncrementalIndexer".
No file watcher, no background thread, no automatic triggers.
All operations (index_all, rebuild_index, cleanup_index) must be invoked manually.

Classification: MANUAL_INCREMENTAL_INDEXER
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
import json
import hashlib
from pathlib import Path


@dataclass
class IndexEntry:
    """A single index entry."""
    path: str
    title: str
    content_hash: str
    size: int
    created_at: str
    modified_at: str
    indexed_at: str = field(default_factory=lambda: datetime.now().isoformat())
    tags: List[str] = field(default_factory=list)
    links: List[str] = field(default_factory=list)


class ManualIncrementalIndexer:
    """
    Manual incremental indexer for the knowledge base.

    Provides hash-based change detection, metadata extraction, and
    index persistence. All operations are manually invoked — there is
    no file watcher, no background thread, and no automatic triggers.

    Gate E: Renamed from AutoIndexer to ManualIncrementalIndexer.

    Usage:
        indexer = ManualIncrementalIndexer(vault_path)
        stats = indexer.index_all()           # Manual full index
        stale = indexer.get_stale_files()     # Manual staleness check
        cleaned = indexer.cleanup_index()     # Manual orphan removal
    """
    
    def __init__(self, vault_path: str, index_path: str = ".vault-index.json"):
        self.vault_path = Path(vault_path)
        self.index_path = self.vault_path / index_path
        self.index: Dict[str, IndexEntry] = {}
        self.load_index()
    
    def load_index(self):
        """Load existing index from file."""
        if self.index_path.exists():
            try:
                data = json.loads(self.index_path.read_text(encoding="utf-8"))
                for path, entry_data in data.items():
                    self.index[path] = IndexEntry(**entry_data)
            except Exception:
                self.index = {}
    
    def save_index(self):
        """Save index to file."""
        data = {
            path: {
                "path": entry.path,
                "title": entry.title,
                "content_hash": entry.content_hash,
                "size": entry.size,
                "created_at": entry.created_at,
                "modified_at": entry.modified_at,
                "indexed_at": entry.indexed_at,
                "tags": entry.tags,
                "links": entry.links,
            }
            for path, entry in self.index.items()
        }
        
        self.index_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    
    def compute_hash(self, content: str) -> str:
        """Compute content hash."""
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def extract_metadata(self, content: str) -> Dict[str, Any]:
        """Extract metadata from markdown content."""
        import re
        
        # Extract title
        title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        title = title_match.group(1) if title_match else "Untitled"
        
        # Extract tags
        tags = re.findall(r"#(\w+)", content)
        
        # Extract wiki-links
        links = re.findall(r"\[\[([^\]]+)\]\]", content)
        
        return {
            "title": title,
            "tags": tags,
            "links": links,
        }
    
    def index_file(self, file_path: Path) -> Optional[IndexEntry]:
        """Index a single file."""
        try:
            relative_path = str(file_path.relative_to(self.vault_path))
            content = file_path.read_text(encoding="utf-8")
            content_hash = self.compute_hash(content)
            
            # Check if already indexed and unchanged
            if relative_path in self.index:
                existing = self.index[relative_path]
                if existing.content_hash == content_hash:
                    return existing
            
            # Extract metadata
            metadata = self.extract_metadata(content)
            
            # Get file stats
            stat = file_path.stat()
            
            entry = IndexEntry(
                path=relative_path,
                title=metadata["title"],
                content_hash=content_hash,
                size=len(content),
                created_at=datetime.fromtimestamp(stat.st_ctime).isoformat(),
                modified_at=datetime.fromtimestamp(stat.st_mtime).isoformat(),
                tags=metadata["tags"],
                links=metadata["links"],
            )
            
            self.index[relative_path] = entry
            return entry
        
        except Exception:
            return None
    
    def index_all(self) -> Dict[str, Any]:
        """Index all files in the vault."""
        stats = {
            "indexed": 0,
            "updated": 0,
            "unchanged": 0,
            "errors": 0,
        }
        
        for md_file in self.vault_path.rglob("*.md"):
            # Skip index file
            if md_file.name == ".vault-index.json":
                continue
            
            result = self.index_file(md_file)
            if result:
                if result.content_hash:
                    stats["indexed"] += 1
            else:
                stats["errors"] += 1
        
        # Save index
        self.save_index()
        
        return stats
    
    def get_stale_files(self) -> List[str]:
        """Get files that have been modified since last index."""
        stale = []
        
        for md_file in self.vault_path.rglob("*.md"):
            if md_file.name == ".vault-index.json":
                continue
            
            try:
                relative_path = str(md_file.relative_to(self.vault_path))
                current_hash = self.compute_hash(md_file.read_text(encoding="utf-8"))
                
                if relative_path in self.index:
                    if self.index[relative_path].content_hash != current_hash:
                        stale.append(relative_path)
                else:
                    stale.append(relative_path)
            except Exception:
                continue
        
        return stale
    
    def get_orphaned_files(self) -> List[str]:
        """Get files in index that no longer exist."""
        orphaned = []
        
        for path in list(self.index.keys()):
            full_path = self.vault_path / path
            if not full_path.exists():
                orphaned.append(path)
        
        return orphaned
    
    def cleanup_index(self) -> int:
        """Remove orphaned entries from index."""
        orphaned = self.get_orphaned_files()
        
        for path in orphaned:
            del self.index[path]
        
        self.save_index()
        return len(orphaned)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get indexing statistics."""
        total_size = sum(entry.size for entry in self.index.values())
        
        # Count by folder
        folder_counts = {}
        for path in self.index.keys():
            folder = path.split("/")[0] if "/" in path else "root"
            folder_counts[folder] = folder_counts.get(folder, 0) + 1
        
        # Count tags
        all_tags = []
        for entry in self.index.values():
            all_tags.extend(entry.tags)
        tag_counts = {}
        for tag in all_tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        return {
            "total_files": len(self.index),
            "total_size_bytes": total_size,
            "total_size_kb": round(total_size / 1024, 2),
            "folders": folder_counts,
            "top_tags": dict(sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]),
            "last_indexed": datetime.now().isoformat(),
        }
    
    def rebuild_index(self) -> Dict[str, Any]:
        """Force rebuild of entire index."""
        self.index = {}
        return self.index_all()


# Backwards-compatible alias
AutoIndexer = ManualIncrementalIndexer
