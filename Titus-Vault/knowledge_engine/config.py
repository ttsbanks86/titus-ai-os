# knowledge_engine/config.py
# Configuration for the Knowledge & Context Engine

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class KnowledgeEngineConfig:
    """Configuration for the knowledge engine."""
    # Vault root directory
    vault_root: Path = field(default_factory=lambda: Path(__file__).parent.parent)

    # Index settings
    index_filename: str = "knowledge_index.json"
    incremental_index: bool = True

    # Search settings
    max_search_results: int = 20
    min_relevance_score: float = 0.1
    authority_weight: float = 0.3
    recency_weight: float = 0.2
    relevance_weight: float = 0.5

    # Cache settings
    cache_max_entries: int = 100
    cache_default_ttl_seconds: int = 3600  # 1 hour
    cache_cleanup_interval: int = 300       # 5 minutes

    # Context assembly settings
    default_context_budget: int = 4000      # Max tokens
    max_documents_per_context: int = 20
    token_estimate_ratio: float = 4.0       # ~4 chars per token

    # Access model settings
    default_access_level: str = "public"
    enforce_access: bool = True

    # Excluded paths (always excluded from indexing)
    excluded_paths: list[str] = field(default_factory=lambda: [
        ".env",
        ".env.*",
        "__pycache__",
        ".pytest_cache",
        ".git",
        ".obsidian",
        "node_modules",
        ".coverage",
        "htmlcov",
        "*.pyc",
        "*.pyo",
        "*.so",
        "*.egg-info",
        "build",
        "dist",
        "tmp",
        ".playwright-mcp",
        ".codex",
        ".codex-temp",
        ".agents",
    ])

    # Excluded file patterns
    excluded_extensions: list[str] = field(default_factory=lambda: [
        ".pyc", ".pyo", ".so", ".dll", ".exe", ".bin",
        ".jpg", ".jpeg", ".png", ".gif", ".webp", ".ico",
        ".mp3", ".mp4", ".wav", ".avi", ".mov",
        ".zip", ".tar", ".gz", ".rar", ".7z",
        ".pdf", ".docx", ".xlsx", ".pptx",
        ".db", ".sqlite", ".sqlite3",
    ])

    # Source of truth directories (highest authority)
    source_of_truth_dirs: list[str] = field(default_factory=lambda: [
        "01-Dashboard",
    ])

    # Governing directories
    governing_dirs: list[str] = field(default_factory=lambda: [
        "07-SOPs",
        "08-Agents",
    ])

    # Project directories
    project_dirs: list[str] = field(default_factory=lambda: [
        "06-Projects",
    ])

    # Archive directories
    archive_dirs: list[str] = field(default_factory=lambda: [
        "10-Archive",
    ])

    def should_exclude_path(self, rel_path: str) -> bool:
        """Check if a path should be excluded from indexing."""
        parts = Path(rel_path).parts
        for excluded in self.excluded_paths:
            if excluded.startswith("*"):
                if rel_path.endswith(excluded[1:]):
                    return True
            elif excluded in parts:
                return True
        return False

    def should_exclude_file(self, filename: str) -> bool:
        """Check if a file should be excluded based on extension."""
        suffix = Path(filename).suffix.lower()
        return suffix in self.excluded_extensions

    def get_authority_for_path(self, rel_path: str) -> str:
        """Determine authority level based on path."""
        parts = Path(rel_path).parts
        if any(d in parts for d in self.source_of_truth_dirs):
            return "source_of_truth"
        if any(d in parts for d in self.governing_dirs):
            return "governing"
        if any(d in parts for d in self.project_dirs):
            return "project"
        if any(d in parts for d in self.archive_dirs):
            return "archived"
        return "reference"
