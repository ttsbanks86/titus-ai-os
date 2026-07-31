# tests/test_vault.py
# Tests for Titus Vault structure and integrity

import pytest
from pathlib import Path


class TestVaultStructure:
    """Tests for vault directory structure."""

    def test_vault_directories_exist(self, vault_dir, required_directories):
        """Verify all 10 vault directories exist."""
        for directory in required_directories:
            dir_path = vault_dir / directory
            assert dir_path.exists(), f"Directory {directory} does not exist"
            assert dir_path.is_dir(), f"{directory} is not a directory"

    def test_vault_directory_count(self, vault_dir, required_directories):
        """Verify vault has the expected number of directories."""
        assert len(required_directories) == 12, "Expected 12 required directories"

    def test_vault_directories_are_directories(self, vault_dir, required_directories):
        """Verify all required paths are directories, not files."""
        for directory in required_directories:
            dir_path = vault_dir / directory
            assert dir_path.is_dir(), f"{directory} should be a directory"


class TestVaultFiles:
    """Tests for vault file existence and readability."""

    def test_vault_index_exists(self, vault_dir):
        """Verify Home.md exists and is readable."""
        home_path = vault_dir / "01-Dashboard" / "Home.md"
        assert home_path.exists(), "Home.md does not exist"
        assert home_path.is_file(), "Home.md is not a file"
        
        # Verify file is readable
        content = home_path.read_text(encoding="utf-8")
        assert len(content) > 0, "Home.md is empty"

    def test_goals_file_exists(self, vault_dir):
        """Verify My-Goals.md exists and is readable."""
        goals_path = vault_dir / "01-Dashboard" / "My-Goals.md"
        assert goals_path.exists(), "My-Goals.md does not exist"
        assert goals_path.is_file(), "My-Goals.md is not a file"
        
        content = goals_path.read_text(encoding="utf-8")
        assert len(content) > 0, "My-Goals.md is empty"

    def test_sops_index_exists(self, vault_dir):
        """Verify SOPs-Index.md exists and is readable."""
        sops_path = vault_dir / "07-SOPs" / "SOPs-Index.md"
        assert sops_path.exists(), "SOPs-Index.md does not exist"
        assert sops_path.is_file(), "SOPs-Index.md is not a file"
        
        content = sops_path.read_text(encoding="utf-8")
        assert len(content) > 0, "SOPs-Index.md is empty"

    def test_agents_index_exists(self, vault_dir):
        """Verify Agents-Index.md exists and is readable."""
        agents_path = vault_dir / "08-Agents" / "Agents-Index.md"
        assert agents_path.exists(), "Agents-Index.md does not exist"
        assert agents_path.is_file(), "Agents-Index.md is not a file"
        
        content = agents_path.read_text(encoding="utf-8")
        assert len(content) > 0, "Agents-Index.md is empty"


class TestVaultWikiLinks:
    """Tests for wiki-link validity."""

    def test_home_md_has_content(self, vault_dir):
        """Verify Home.md has substantial content."""
        home_path = vault_dir / "01-Dashboard" / "Home.md"
        content = home_path.read_text(encoding="utf-8")
        
        # Should have at least 10 lines
        lines = content.strip().split("\n")
        assert len(lines) >= 10, f"Home.md has only {len(lines)} lines, expected at least 10"

    def test_sops_index_has_entries(self, vault_dir):
        """Verify SOPs-Index.md has multiple SOP entries."""
        sops_path = vault_dir / "07-SOPs" / "SOPs-Index.md"
        content = sops_path.read_text(encoding="utf-8")
        
        # Should have multiple wiki-links
        wiki_link_count = content.count("[[")
        assert wiki_link_count >= 5, f"SOPs-Index.md has only {wiki_link_count} wiki-links, expected at least 5"
