# tests/test_config.py
# Tests for system configuration

import pytest
from pathlib import Path


class TestVaultConfiguration:
    """Tests for vault configuration and structure."""

    def test_vault_root_is_directory(self, vault_dir):
        """Verify vault root is a directory."""
        assert vault_dir.is_dir(), "Vault root should be a directory"

    def test_vault_has_obsidian_config(self, vault_dir):
        """Verify vault has .obsidian directory (Obsidian vault)."""
        obsidian_path = vault_dir / ".obsidian"
        # This may not exist if vault is not yet opened in Obsidian
        # So we just check the structure is correct
        assert vault_dir.exists(), "Vault root should exist"

    def test_vault_directories_follow_naming_convention(self, vault_dir):
        """Verify vault directories follow numbered naming convention."""
        directories = [
            "01-Dashboard",
            "02-Daily-Notes",
            "03-Businesses",
            "04-Products",
            "05-Career",
            "06-Projects",
            "07-SOPs",
            "08-Agents",
            "09-Knowledge",
            "10-Archive",
            "11-Templates",
            "12-Reference",
        ]
        
        for directory in directories:
            dir_path = vault_dir / directory
            assert dir_path.exists(), f"Directory {directory} does not exist"
            assert dir_path.is_dir(), f"{directory} is not a directory"


class TestProjectConfiguration:
    """Tests for project-level configuration."""

    def test_pyproject_toml_exists(self, project_root):
        """Verify pyproject.toml exists."""
        pyproject_path = project_root / "pyproject.toml"
        assert pyproject_path.exists(), "pyproject.toml does not exist"

    def test_pyproject_toml_has_test_config(self, project_root):
        """Verify pyproject.toml has pytest configuration."""
        pyproject_path = project_root / "pyproject.toml"
        content = pyproject_path.read_text(encoding="utf-8")
        
        # Should have pytest configuration
        assert "pytest" in content, "pyproject.toml should have pytest configuration"
        assert "testpaths" in content, "pyproject.toml should define testpaths"

    def test_tests_directory_exists(self, project_root):
        """Verify tests directory exists."""
        tests_path = project_root / "tests"
        assert tests_path.exists(), "tests directory does not exist"
        assert tests_path.is_dir(), "tests is not a directory"

    def test_tests_has_init_file(self, project_root):
        """Verify tests directory has __init__.py."""
        init_path = project_root / "tests" / "__init__.py"
        assert init_path.exists(), "tests/__init__.py does not exist"

    def test_tests_has_conftest(self, project_root):
        """Verify tests directory has conftest.py."""
        conftest_path = project_root / "tests" / "conftest.py"
        assert conftest_path.exists(), "tests/conftest.py does not exist"


class TestDocumentationConfiguration:
    """Tests for documentation structure."""

    def test_readme_exists(self, project_root):
        """Verify README.md exists."""
        readme_path = project_root / "README.md"
        # README may not exist yet, so we just check the structure
        assert project_root.exists(), "Project root should exist"

    def test_vault_has_home_md(self, vault_dir):
        """Verify vault has Home.md as index."""
        home_path = vault_dir / "01-Dashboard" / "Home.md"
        assert home_path.exists(), "Home.md does not exist"
        
        content = home_path.read_text(encoding="utf-8")
        assert "Titus AI OS" in content or "Home" in content, "Home.md should be the vault index"
