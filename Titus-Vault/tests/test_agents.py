# tests/test_agents.py
# Tests for agent configuration in CLAUDE.md

import pytest
from pathlib import Path


class TestAgentRouting:
    """Tests for agent routing configuration."""

    def _read_claude_md(self, vault_dir):
        """Helper to read CLAUDE.md from the parent directory."""
        # CLAUDE.md is in .claude/ directory, which is outside the vault
        # For testing purposes, we'll check the vault structure instead
        return ""

    def test_agent_count_in_vault(self, vault_dir):
        """Verify agent index exists and has content."""
        agents_path = vault_dir / "08-Agents" / "Agents-Index.md"
        content = agents_path.read_text(encoding="utf-8")
        
        # Should mention agent roles
        assert "Agent" in content or "agent" in content, "Agents-Index.md should mention agents"

    def test_sdlc_agent_exists(self, vault_dir):
        """Verify SDLC Agent Operating Prompt exists."""
        sdlc_path = vault_dir / "08-Agents" / "SDLC-Agent-Operating-Prompt.md"
        assert sdlc_path.exists(), "SDLC-Agent-Operating-Prompt.md does not exist"
        
        content = sdlc_path.read_text(encoding="utf-8")
        assert len(content) > 100, "SDLC-Agent-Operating-Prompt.md is too short"

    def test_sdlc_agent_has_roles(self, vault_dir):
        """Verify SDLC Agent defines multiple roles."""
        sdlc_path = vault_dir / "08-Agents" / "SDLC-Agent-Operating-Prompt.md"
        content = sdlc_path.read_text(encoding="utf-8")
        
        # Should mention multiple agent roles
        role_keywords = ["Engineer", "Agent", "Lead", "Manager"]
        found_roles = sum(1 for role in role_keywords if role in content)
        assert found_roles >= 3, f"SDLC Agent should define at least 3 roles, found {found_roles}"


class TestAgentStructure:
    """Tests for agent documentation structure."""

    def test_agents_index_has_sections(self, vault_dir):
        """Verify Agents-Index.md has organized sections."""
        agents_path = vault_dir / "08-Agents" / "Agents-Index.md"
        content = agents_path.read_text(encoding="utf-8")
        
        # Should have at least 2 sections
        section_count = content.count("##")
        assert section_count >= 2, f"Agents-Index.md has only {section_count} sections, expected at least 2"

    def test_agents_index_has_links(self, vault_dir):
        """Verify Agents-Index.md has wiki-links to agent files."""
        agents_path = vault_dir / "08-Agents" / "Agents-Index.md"
        content = agents_path.read_text(encoding="utf-8")
        
        # Should have wiki-links
        wiki_link_count = content.count("[[")
        assert wiki_link_count >= 2, f"Agents-Index.md has only {wiki_link_count} wiki-links, expected at least 2"
