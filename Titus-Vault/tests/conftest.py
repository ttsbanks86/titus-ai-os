# tests/conftest.py
# Pytest configuration and fixtures for Titus AI OS tests

import pytest
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Vault directory
VAULT_DIR = PROJECT_ROOT

# Required vault directories (actual structure)
REQUIRED_DIRECTORIES = [
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

# Required vault files
REQUIRED_FILES = [
    "01-Dashboard/Home.md",
    "01-Dashboard/My-Goals.md",
    "07-SOPs/SOPs-Index.md",
    "08-Agents/Agents-Index.md",
]


@pytest.fixture
def project_root():
    """Return the project root directory."""
    return PROJECT_ROOT


@pytest.fixture
def vault_dir():
    """Return the vault directory."""
    return VAULT_DIR


@pytest.fixture
def required_directories():
    """Return list of required vault directories."""
    return REQUIRED_DIRECTORIES


@pytest.fixture
def required_files():
    """Return list of required vault files."""
    return REQUIRED_FILES
