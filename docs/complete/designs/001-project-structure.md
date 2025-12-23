# Design 001: Project Structure

## Document Purpose

This document defines the complete directory structure, file organization, and packaging strategy for the EAD LangChain Template. It establishes where every file belongs and why.

---

## Directory Tree

```
ead-langchain-template/
├── src/                          # Package source code (src-layout)
│   └── langchain_llm/           # Main package
│       ├── __init__.py          # Public API exports
│       ├── interfaces.py        # Protocols and ABCs
│       ├── config.py            # Configuration management
│       └── logging_config.py    # Logging utilities
│
├── examples/                     # Progressive tutorial examples
│   ├── 01_basic.py              # Basic LLM usage (Python script)
│   ├── 01_basic.ipynb           # Basic LLM usage (Jupyter notebook)
│   ├── 02_streaming.py          # Streaming responses
│   ├── 02_streaming.ipynb       # Streaming responses (notebook)
│   ├── 03_conversation.py       # Multi-turn conversations
│   ├── 03_conversation.ipynb    # Conversations (notebook)
│   ├── 04_advanced.py           # Advanced features (callbacks, batching)
│   └── 04_advanced.ipynb        # Advanced features (notebook)
│
├── tests/                        # Test suite
│   ├── conftest.py              # Shared pytest fixtures
│   ├── test_config.py           # Tests for config.py
│   ├── test_logging.py          # Tests for logging_config.py
│   └── enforcement/             # Code quality enforcement tests
│       ├── __init__.py
│       ├── test_sphinx_docstrings.py  # Enforce Sphinx docstrings
│       └── test_no_emojis.py    # Prevent emojis in code
│
├── docs/                         # Documentation
│   ├── complete/                # AI-executable project blueprints
│   │   ├── requirements/        # What to build
│   │   ├── designs/             # How to build it
│   │   ├── phases/              # Execution roadmap
│   │   └── tasks/               # Step-by-step instructions
│   └── api/                     # API documentation (future)
│
├── .github/                      # GitHub configuration
│   ├── copilot-instructions.md  # AI coding assistant guidelines
│   ├── ISSUE_TEMPLATE/          # Issue templates (optional)
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── PULL_REQUEST_TEMPLATE.md # PR template (optional)
│   └── workflows/               # CI/CD workflows (future)
│       └── tests.yml
│
├── .vscode/                      # VS Code settings (optional, gitignored)
│   └── settings.json
│
├── logs/                         # Log files (gitignored)
│   └── app.log                  # Created if EADLANGCHAIN_LOG_FILE set
│
├── pyproject.toml               # Poetry configuration + tool settings
├── requirements.txt             # pip dependencies (generated from poetry)
├── poetry.lock                  # Locked dependency versions
│
├── .env                          # Environment variables (gitignored)
├── .env.example                 # Environment variable template
│
├── .gitignore                   # Git ignore rules
├── .python-version              # Python version for pyenv (optional)
│
├── README.md                    # User-facing documentation
├── LICENSE                      # Open source license (if applicable)
└── CONTRIBUTING.md              # Contribution guidelines (optional)
```

---

## Directory Purposes

### `/src/langchain_llm/` - Package Source

**Purpose**: Core utility package code

**Why src-layout**:
- Prevents importing uninstalled package (catches packaging bugs early)
- Industry best practice (PyPA recommended)
- Forces proper `pip install -e .` or `poetry install`
- Cleaner separation of package vs project

**Files**:
- `__init__.py`: Public API, exports functions
- `interfaces.py`: Protocol and ABC definitions
- `config.py`: Environment variable and API key management
- `logging_config.py`: Custom logging setup

**Rules**:
- All code must follow TDD
- All functions need Sphinx docstrings
- Maximum ~150 lines per file (guideline)
- No business logic (only utilities)

**Size Target**: ~500 lines total (keep it minimal)

### `/examples/` - Tutorial Examples

**Purpose**: Progressive learning examples (educational)

**Structure**: Numbered pairs (script + notebook)
- `0X_name.py`: Python script (runs standalone)
- `0X_name.ipynb`: Jupyter notebook (interactive)

**Progression**:
1. **01_basic**: Simplest usage (invoke)
2. **02_streaming**: Add streaming responses
3. **03_conversation**: Add message history
4. **04_advanced**: Add callbacks, batching

**Rules**:
- Each example independent (can run alone)
- Each introduces ONE new concept
- Both .py and .ipynb versions have identical content
- Include error handling (graceful provider skipping)
- Extensive comments explaining WHY, not just what

**Not in scope**:
- Examples don't need unit tests (but should work when run)
- Can have print statements (educational clarity)
- Can repeat setup code (each example self-contained)

### `/tests/` - Test Suite

**Purpose**: Automated testing infrastructure

**Structure**:
- `conftest.py`: Shared fixtures (root level)
- `unit/`: Unit tests for core modules
  - `test_<module>.py`: Unit tests mirroring src/ structure
- `integration/`: Integration and utility tests
  - Tests for scripts, workflows, cross-module interactions
- `enforcement/`: Code quality enforcement tests

**Test File Naming**:
- Pattern: `test_<module_name>.py`
- Examples:
  - `src/langchain_llm/config.py` → `tests/unit/test_config.py`
  - `scripts/sync_notebooks.py` → `tests/integration/test_sync_notebooks.py`

**Rules**:
- Use pytest
- All tests must pass
- Use fixtures from conftest.py
- Group related tests in classes
- Descriptive test names: `test_<function>_<scenario>`

**Coverage Target**: >80% for all modules in src/

### `/tests/enforcement/` - Quality Gates

**Purpose**: Automated enforcement of code standards

**Tests**:
- `test_sphinx_docstrings.py`: Ensures Sphinx-style (not Google/NumPy)
- `test_no_emojis.py`: Prevents emoji characters in code

**Why Separate**:
- Different concern (code quality vs functionality)
- Can be run independently: `pytest tests/enforcement/`
- Clear responsibility separation
- Easy to add new enforcement rules

**How It Works**:
- Scans all `.py` files
- Uses regex to detect violations
- Fails build if violations found
- Reports specific files with issues

### `/docs/` - Documentation

**Purpose**: Project documentation

**Subdirectories**:
- `complete/`: AI-executable blueprints (requirements, designs, phases, tasks)
- `api/`: Generated API docs (future, using Sphinx)

**docs/complete** Structure:
```
complete/
├── requirements/     # 5 files: What to build
├── designs/          # 7 files: How to build it
├── phases/           # 6 files: Execution roadmap
└── tasks/            # 22 files: Step-by-step instructions
```

**Purpose of docs/complete**:
- Reverse-engineered project blueprint
- Each file fits in AI context window (~120k tokens)
- Documents "how we should have built this"
- Educational for understanding project decisions

### `/.github/` - GitHub Configuration

**Purpose**: GitHub-specific files and workflows

**Key Files**:
- `copilot-instructions.md`: AI assistant guidelines (CRITICAL)
- `ISSUE_TEMPLATE/`: Templates for bug reports, feature requests
- `PULL_REQUEST_TEMPLATE.md`: PR template
- `workflows/`: GitHub Actions CI/CD (future)

**Why copilot-instructions.md is critical**:
- Ensures AI assistants follow project conventions
- Documents TDD workflow
- Explains environment variable conventions
- Shows correct patterns

**Location**: Must be in `.github/` for GitHub Copilot to find it

### `/logs/` - Log Files (gitignored)

**Purpose**: Runtime log file storage

**Created**: When `EADLANGCHAIN_LOG_FILE` environment variable is set

**Rules**:
- Entire directory in .gitignore
- Created automatically by logging setup
- Not required (console logging works without this)

---

## File-Level Design

### `pyproject.toml` - Project Configuration

**Purpose**: Single source of truth for project metadata and tool config

**Sections**:
```toml
[tool.poetry]
# Project metadata, dependencies

[tool.poetry.dependencies]
# Runtime dependencies

[tool.poetry.group.dev.dependencies]
# Development dependencies (tests, linting, notebooks)

[tool.pytest.ini_options]
# pytest configuration

[tool.ruff]
# Ruff linter/formatter configuration

[tool.ruff.lint]
# Linting rules

[tool.ruff.format]
# Formatting options

[build-system]
# PEP 517 build backend
```

**Key Settings**:
- Package name: `langchain-llm`
- Python version: `^3.10`
- Package location: `src/langchain_llm`
- Line length: 130 characters

**Tools Configured**:
- Poetry (dependencies)
- pytest (test runner)
- Ruff (linter and formatter)

### `requirements.txt` - pip Dependencies

**Purpose**: pip-compatible dependency list

**Generation**: `poetry export -f requirements.txt -o requirements.txt --without-hashes`

**When to Update**: After any `poetry add` or `poetry update`

**Why Both**:
- Poetry users: Use `poetry install`
- pip users: Use `pip install -r requirements.txt`
- CI/CD: Often uses requirements.txt

**Maintenance**: Keep in sync with poetry.lock

### `poetry.lock` - Locked Dependencies

**Purpose**: Exact dependency versions for reproducible builds

**Management**:
- Auto-generated by Poetry
- Should be committed to git
- Updated with `poetry lock` or `poetry update`

**Benefits**:
- Reproducible environments
- Prevents dependency drift
- Documents exact working versions

### `.env` and `.env.example` - Environment Configuration

**`.env`** (gitignored):
- Contains actual API keys and secrets
- User-specific, never committed
- Created by copying .env.example

**`.env.example`** (committed):
- Template showing required variables
- Includes helpful comments and links
- Documents default values
- Safe to commit (no secrets)

**Workflow**:
```bash
cp .env.example .env
# Edit .env with actual API keys
```

### `.gitignore` - Version Control Exclusions

**Key Exclusions**:
```gitignore
# Secrets
.env
*.env

# Python
__pycache__/
*.pyc
.pytest_cache/
.coverage

# Virtual environments
.venv/
venv/
ENV/

# IDEs
.vscode/
.idea/

# OS
.DS_Store

# Logs
logs/

# Build artifacts
dist/
build/
*.egg-info/
```

**Must Include**:
- .env files (all variations)
- Python bytecode and caches
- Virtual environments
- IDE-specific files
- OS-specific files

**Must NOT Ignore**:
- .env.example (it's a template)
- poetry.lock (reproducible builds)
- Source code in src/

---

## Package Layout (src-layout)

### Why Src-Layout vs Flat Layout

**Flat Layout** (NOT used):
```
project/
├── langchain_llm/  # Package at root
│   ├── __init__.py
│   └── config.py
└── tests/
```

**Problems with Flat**:
- Can import uninstalled package (misleading during development)
- Pollutes project root
- Harder to distinguish package vs project files

**Src-Layout** (USED):
```
project/
├── src/
│   └── langchain_llm/  # Package in src/
│       ├── __init__.py
│       └── config.py
└── tests/
```

**Benefits**:
- Must install package to import (catches packaging issues)
- Cleaner root directory
- Clear separation
- PEP 420 compliant
- Industry best practice

### Package Discovery Configuration

**pyproject.toml**:
```toml
[tool.poetry]
packages = [{include = "langchain_llm", from = "src"}]
```

This tells Poetry:
- Package name: `langchain_llm`
- Location: `src/langchain_llm/`

**Installation**:
```bash
# Poetry
poetry install

# pip
pip install -e .
```

Both make `src/langchain_llm/` importable as `langchain_llm`

---

## File Naming Conventions

### Python Modules
- **Pattern**: `snake_case.py`
- **Examples**: `config.py`, `logging_config.py`, `interfaces.py`
- **Rationale**: Python standard, PEP 8

### Test Files
- **Pattern**: `test_<module_name>.py`
- **Examples**: `test_config.py`, `test_logging.py`
- **Rationale**: pytest discovery

### Example Files
- **Pattern**: `0X_<name>.py` and `0X_<name>.ipynb`
- **Examples**: `01_basic.py`, `02_streaming.ipynb`
- **Rationale**: Sequential ordering, clear progression

### Documentation Files
- **Pattern**:
  - Ordered: `NNN-<name>.md` (e.g., `000-overview.md`)
  - Unordered: `<name>.md` (e.g., `README.md`)
- **Rationale**: Alphabetical sorting shows intended order

### Private Modules
- **Pattern**: `_<name>.py`
- **Examples**: `_internal.py`, `_utils.py`
- **Rationale**: Convention for private/internal modules
- **Note**: Not currently used (package is small enough)

---

## Import Structure

### Public API (`src/langchain_llm/__init__.py`)

**Purpose**: Define what users can import

**Pattern**:
```python
"""
Package docstring.
"""

from langchain_llm.config import get_api_key, load_env_config
from langchain_llm.logging_config import get_logger, setup_logging

__version__ = "0.1.0"

__all__ = [
    "setup_logging",
    "get_logger",
    "load_env_config",
    "get_api_key",
]
```

**What This Allows**:
```python
# Users can import from package root
from langchain_llm import setup_logging, get_api_key

# Instead of deep imports
from langchain_llm.config import get_api_key  # Also works, but not needed
```

**Rules**:
- Only export public functions
- Keep __all__ up to date
- Document in module docstring
- Version string for package identification

### Internal Imports

**Within Package** (src/langchain_llm/):
```python
# Absolute imports (preferred)
from langchain_llm.interfaces import ConfigProvider

# Relative imports (also ok for nearby modules)
from .interfaces import ConfigProvider
```

**From Tests**:
```python
# Import from package (requires installation)
from langchain_llm import get_api_key, load_env_config
from langchain_llm.config import ConfigError
```

**From Examples**:
```python
# Import from installed package
from langchain_llm import setup_logging, get_logger, load_env_config, get_api_key

# Import LangChain (external)
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
```

---

## Build and Distribution

### Build Artifacts

**Generated by Poetry**:
- `dist/` - Built distributions (.whl, .tar.gz)
- `build/` - Build intermediates
- `*.egg-info/` - Package metadata

**Gitignored**: All build artifacts

**Building**:
```bash
poetry build
# Creates:
# dist/langchain_llm-0.1.0-py3-none-any.whl
# dist/langchain_llm-0.1.0.tar.gz
```

### Installation Modes

#### Development Mode (Editable)
```bash
# Poetry
poetry install

# pip
pip install -e .
```

**Effect**: Imports resolve to `src/langchain_llm/` directly (changes reflected immediately)

**Use Case**: Active development

#### User Mode (Package)
```bash
# Poetry
poetry add langchain-llm

# pip
pip install langchain-llm
```

**Effect**: Installs packaged version from PyPI

**Use Case**: Using as dependency

---

## Repository Structure Decisions

### Decision: Keep Examples at Root Level

**Why**:
- High visibility (first thing users see)
- Easy to run: `python examples/01_basic.py`
- Emphasizes educational purpose

**Alternative Considered**: `src/examples/` or `docs/examples/`
**Rejected Because**: Less discoverable, implies they're part of package

### Decision: Separate enforcement/ tests

**Why**:
- Different concern (quality vs functionality)
- Can be run separately
- Clearer organization
- Easy to add more enforcement rules

**Alternative Considered**: Mix in `tests/test_quality.py`
**Rejected Because**: Doesn't scale well with multiple enforcement rules

### Decision: Keep interfaces.py separate

**Why**:
- Clear documentation of all protocols/ABCs
- Avoids circular imports
- Easy to find interfaces
- Can import just interfaces for type hints

**Alternative Considered**: Define protocols in respective modules
**Rejected Because**: Harder to discover, circular import risk

### Decision: Include Both .py and .ipynb Examples

**Why**:
- Different learning styles
- .py easier to read on GitHub
- .ipynb better for interactive learning
- Content is identical (not double work)

**Alternative Considered**: Only .py or only .ipynb
**Rejected Because**: Limits accessibility

---

## Growth Patterns

### Adding New Utility Module

**Steps**:
1. Create `src/langchain_llm/new_module.py`
2. Define interface in `src/langchain_llm/interfaces.py` (if needed)
3. Create `tests/test_new_module.py`
4. Export public functions in `src/langchain_llm/__init__.py`
5. Update documentation

**Example** (adding utils.py):
```
src/langchain_llm/
├── __init__.py          # Add: from langchain_llm.utils import helper
├── interfaces.py
├── config.py
├── logging_config.py
└── utils.py             # NEW

tests/
├── test_config.py
├── test_logging.py
└── test_utils.py        # NEW
```

### Adding New Example

**Steps**:
1. Create `examples/0X_name.py` (Python script)
2. Create `examples/0X_name.ipynb` (Jupyter notebook)
3. Update README with new example description
4. Test both versions

**Numbering**: Use next available number (01, 02, 03, ...)

### Adding New Provider Support

**No structure changes needed!**

Just:
1. Install provider package: `poetry add langchain-<provider>`
2. Update `.env.example` with new API key variable
3. Update `config.py` provider mapping
4. Add example in existing example files

---

## Related Documents

- **Previous**: [000-architecture-overview.md](000-architecture-overview.md) - System design
- **Next**: [002-configuration-design.md](002-configuration-design.md) - Config module design
- **See Also**:
  - [requirements/002-technical-requirements.md](../requirements/002-technical-requirements.md) - Technical specs

## Document Metadata

- **Version**: 1.0
- **Status**: Active
- **Owner**: EAD LangChain Template Team
