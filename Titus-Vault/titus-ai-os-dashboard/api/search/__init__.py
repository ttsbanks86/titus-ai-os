"""
Titus AI OS Semantic Search
Natural language queries over the knowledge engine.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
import json
import re
from pathlib import Path


@dataclass
class SearchResult:
    """A single search result."""
    id: str
    title: str
    content: str
    score: float
    source: str
    file_path: str
    line_number: Optional[int] = None
    context: str = ""


@dataclass
class SearchQuery:
    """A search query with metadata."""
    query: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    results_count: int = 0
    execution_time_ms: float = 0


class SemanticSearch:
    """
    Semantic search engine for the knowledge base.
    
    Supports natural language queries, keyword matching,
    and relevance scoring.
    """
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.index: Dict[str, Dict] = {}
        self.build_index()
    
    def build_index(self):
        """Build search index from vault files."""
        for md_file in self.vault_path.rglob("*.md"):
            try:
                content = md_file.read_text(encoding="utf-8")
                relative_path = md_file.relative_to(self.vault_path)
                
                # Extract title from first heading
                title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
                title = title_match.group(1) if title_match else md_file.stem
                
                # Store in index
                self.index[str(relative_path)] = {
                    "title": title,
                    "content": content,
                    "path": str(relative_path),
                    "size": len(content),
                    "modified": datetime.fromtimestamp(md_file.stat().st_mtime).isoformat(),
                }
            except Exception:
                continue
    
    def search(
        self,
        query: str,
        max_results: int = 10,
        min_score: float = 0.1,
    ) -> List[SearchResult]:
        """
        Search the knowledge base.
        
        Uses keyword matching with relevance scoring.
        """
        query_lower = query.lower()
        query_words = set(re.findall(r"\w+", query_lower))
        
        results = []
        
        for path, doc in self.index.items():
            content_lower = doc["content"].lower()
            title_lower = doc["title"].lower()
            
            # Calculate score
            score = 0.0
            
            # Title match (highest weight)
            if query_lower in title_lower:
                score += 1.0
            for word in query_words:
                if word in title_lower:
                    score += 0.3
            
            # Content match
            if query_lower in content_lower:
                score += 0.5
            for word in query_words:
                if word in content_lower:
                    score += 0.1
            
            # Frequency bonus
            for word in query_words:
                count = content_lower.count(word)
                score += min(count * 0.05, 0.3)
            
            if score >= min_score:
                # Find context around first match
                context = self._extract_context(content_lower, query_lower)
                
                result = SearchResult(
                    id=path,
                    title=doc["title"],
                    content=doc["content"][:500] + "..." if len(doc["content"]) > 500 else doc["content"],
                    score=min(score, 1.0),
                    source=doc["path"],
                    file_path=path,
                    context=context,
                )
                results.append(result)
        
        # Sort by score
        results.sort(key=lambda r: r.score, reverse=True)
        
        return results[:max_results]
    
    def _extract_context(self, content: str, query: str, chars: int = 200) -> str:
        """Extract context around the first match."""
        idx = content.find(query)
        if idx == -1:
            return ""
        
        start = max(0, idx - chars // 2)
        end = min(len(content), idx + len(query) + chars // 2)
        
        return content[start:end].strip()
    
    def search_by_tag(self, tag: str) -> List[SearchResult]:
        """Search for files with a specific tag."""
        results = []
        
        for path, doc in self.index.items():
            if f"#{tag}" in doc["content"] or f"tags: {tag}" in doc["content"].lower():
                result = SearchResult(
                    id=path,
                    title=doc["title"],
                    content=doc["content"][:200],
                    score=1.0,
                    source=doc["path"],
                    file_path=path,
                )
                results.append(result)
        
        return results
    
    def search_by_folder(self, folder: str) -> List[SearchResult]:
        """Search for files in a specific folder."""
        results = []
        
        for path, doc in self.index.items():
            if folder.lower() in path.lower():
                result = SearchResult(
                    id=path,
                    title=doc["title"],
                    content=doc["content"][:200],
                    score=0.8,
                    source=doc["path"],
                    file_path=path,
                )
                results.append(result)
        
        return results
    
    def get_suggestions(self, partial_query: str) -> List[str]:
        """Get search suggestions based on partial query."""
        suggestions = []
        partial_lower = partial_query.lower()
        
        # Check titles
        for doc in self.index.values():
            if partial_lower in doc["title"].lower():
                suggestions.append(doc["title"])
        
        # Check common terms
        common_terms = [
            "project", "milestone", "task", "agent", "knowledge",
            "verification", "test", "security", "performance",
        ]
        for term in common_terms:
            if partial_lower in term:
                suggestions.append(term)
        
        return list(set(suggestions))[:10]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get search index statistics."""
        total_size = sum(doc["size"] for doc in self.index.values())
        
        # Count by folder
        folder_counts = {}
        for path in self.index.keys():
            folder = path.split("/")[0] if "/" in path else "root"
            folder_counts[folder] = folder_counts.get(folder, 0) + 1
        
        return {
            "total_documents": len(self.index),
            "total_size_bytes": total_size,
            "total_size_kb": round(total_size / 1024, 2),
            "folders": folder_counts,
            "last_indexed": datetime.now().isoformat(),
        }
