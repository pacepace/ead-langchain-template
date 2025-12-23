# Requirements 002: Technical Requirements

## Document Purpose

This document specifies the technical stack, dependencies, versions, and infrastructure requirements for the EAD LangChain Template. It serves as the definitive reference for all technical decisions.

---

## TR-001: Python Environment

### TR-001.1: Python Version
- **Requirement**: Python 3.10 or higher
- **Rationale**:
  - Modern type hints (PEP 604 - `str | None` syntax)
  - Structural pattern matching (match statements)
  - Better error messages
  - LangChain full compatibility
  - Maintained and actively developed

**Acceptance Criteria**:
- [ ] Package specifies `python = "^3.10"` in pyproject.toml
- [ ] Code uses Python 3.10+ features where appropriate
- [ ] No Python 3.9 or earlier specific code
- [ ] Works on Python 3.10, 3.11, and 3.12

### TR-001.2: Platform Support
- **Requirement**: Cross-platform compatibility
- **Supported Platforms**:
  - macOS 12+ (Monterey and later)
  - Linux (Ubuntu 20.04+, Fedora 35+, Debian 11+)
  - Windows 10/11 (with WSL2 recommended for best experience)

**Acceptance Criteria**:
- [ ] All path operations use `pathlib.Path` (not os.path)
- [ ] No platform-specific system calls
- [ ] Virtual environment creation works on all platforms
- [ ] Examples run successfully on macOS, Linux, Windows

---

## TR-002: Package Management

### TR-002.1: Poetry (Primary)
- **Requirement**: Poetry 1.5+ for dependency management
- **Rationale**:
  - Modern Python packaging
  - Deterministic dependency resolution
  - Built-in virtual environment management
  - Lockfile for reproducible builds
  - Development vs production dependencies

**Configuration File**: `pyproject.toml`

**Acceptance Criteria**:
- [ ] Valid `pyproject.toml` with all required fields
- [ ] `poetry.lock` tracks exact versions
- [ ] `poetry install` creates working environment
- [ ] `poetry run pytest` executes tests
- [ ] `poetry add` successfully adds dependencies

**Example pyproject.toml Structure**:
```toml
[tool.poetry]
name = "langchain-llm"
version = "0.1.0"
description = "LangChain LLM utilities for EAD LangChain Template"
authors = ["EAD Team"]
packages = [{include = "langchain_llm", from = "src"}]

[tool.poetry.dependencies]
python = "^3.10"
langchain-core = "^0.1.0"
langchain-openai = "^0.0.5"
langchain-anthropic = "^0.1.0"
langchain-google-genai = "^0.0.5"
python-dotenv = "^1.0.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
pytest-cov = "^4.1.0"
ruff = "^0.1.0"
jupyter = "^1.0.0"
```

### TR-002.2: pip (Alternative)
- **Requirement**: pip 23+ support for traditional users
- **Rationale**:
  - Some users prefer traditional workflow
  - CI/CD systems often use pip
  - Simpler for quick testing
  - Wider ecosystem compatibility

**Configuration File**: `requirements.txt`

**Acceptance Criteria**:
- [ ] `requirements.txt` exists and is up-to-date
- [ ] `pip install -r requirements.txt` installs all dependencies
- [ ] `pip install -e .` installs package in editable mode
- [ ] requirements.txt matches poetry.lock versions
- [ ] Can generate from Poetry: `poetry export -f requirements.txt -o requirements.txt --without-hashes`

**Maintenance**:
- requirements.txt must be regenerated after any Poetry dependency change:
  ```bash
  poetry export -f requirements.txt -o requirements.txt --without-hashes
  ```
- Both methods should produce identical environments

---

## TR-003: Core Dependencies

### TR-003.1: LangChain Ecosystem
**Purpose**: LLM abstraction and provider integration

#### langchain-core
- **Version**: ^0.3.0 (latest stable)
- **Purpose**: Core LangChain abstractions
- **Key Components Used**:
  - `langchain_core.messages` - Message types (SystemMessage, HumanMessage, AIMessage)
  - `langchain_core.callbacks` - Callback system (BaseCallbackHandler)
  - `langchain_core.language_models` - Base LLM interfaces

**Acceptance Criteria**:
- [ ] Can import message types
- [ ] Can create custom callbacks
- [ ] Compatible with all provider packages

#### langchain-openai
- **Version**: ^0.2.0 (latest stable)
- **Purpose**: OpenAI integration (GPT-5, GPT-4o, etc.)
- **Key Components Used**:
  - `ChatOpenAI` - OpenAI chat models
  - Streaming support
  - Function calling (future)

**Acceptance Criteria**:
- [ ] Can instantiate ChatOpenAI with API key
- [ ] Supports invoke() and stream() methods
- [ ] Works with gpt-5-nano, gpt-5-mini, gpt-5, gpt-4o

**Temperature Constraint**:
GPT-5 family models (gpt-5-nano, gpt-5-mini, gpt-5) require `temperature=1.0` as of October 2025. This is an OpenAI API requirement. Only gpt-5-chat-latest and GPT-4o models support custom temperature values (0.0-2.0).

#### langchain-anthropic
- **Version**: ^0.3.0 (latest stable)
- **Purpose**: Anthropic Claude integration
- **Key Components Used**:
  - `ChatAnthropic` - Claude chat models
  - Streaming support
  - Tool use (future)

**Acceptance Criteria**:
- [ ] Can instantiate ChatAnthropic with API key
- [ ] Supports invoke() and stream() methods
- [ ] Works with claude-3-haiku-20240307, claude-3-5-sonnet-20241022, claude-haiku-4-5

#### langchain-google-genai
- **Version**: ^2.0.0 (latest stable)
- **Purpose**: Google Gemini integration
- **Key Components Used**:
  - `ChatGoogleGenerativeAI` - Gemini chat models
  - Streaming support

**Acceptance Criteria**:
- [ ] Can instantiate ChatGoogleGenerativeAI with API key
- [ ] Supports invoke() and stream() methods
- [ ] Works with gemini-2.0-flash-lite, gemini-2.5-flash, gemini-2.0-flash, gemini-1.5-pro

**Provider Version Matrix**:
| Provider   | Package               | Minimum Version | Models Supported           |
|------------|-----------------------|-----------------|----------------------------|
| OpenAI     | langchain-openai      | 0.2.0           | gpt-5-nano, gpt-5-mini, gpt-5, gpt-4o |
| Anthropic  | langchain-anthropic   | 0.3.0           | claude-3-haiku-20240307, claude-3-5-sonnet-20241022, claude-haiku-4-5 |
| Google     | langchain-google-genai| 2.0.0           | gemini-2.0-flash-lite, gemini-2.5-flash, gemini-2.0-flash |

### TR-003.2: Configuration Management
**Purpose**: Environment variable and .env file handling

#### python-dotenv
- **Version**: ^1.0.0
- **Purpose**: Load environment variables from .env files
- **Key Features Used**:
  - `load_dotenv()` - Load .env file
  - Automatic `.env` file discovery
  - Override system environment variables

**Acceptance Criteria**:
- [ ] Can load .env from project root
- [ ] Can specify custom .env path
- [ ] Environment variables accessible via os.getenv()
- [ ] No conflicts with system environment variables

---

## TR-004: Development Dependencies

### TR-004.1: Testing Framework
**Purpose**: Test-Driven Development infrastructure

#### pytest
- **Version**: ^7.4.0
- **Purpose**: Test runner and framework
- **Key Features Used**:
  - Test discovery (`test_*.py` files)
  - Fixtures (conftest.py)
  - Parametrized tests
  - Markers (for categorizing tests)
  - Verbose output mode

**Acceptance Criteria**:
- [ ] `pytest` discovers all test files
- [ ] Fixtures load from conftest.py
- [ ] Can run specific tests: `pytest tests/unit/test_config.py`
- [ ] Can run with coverage: `pytest --cov`

**Configuration** (`pyproject.toml`):
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --strict-markers"
```

#### pytest-cov
- **Version**: ^4.1.0
- **Purpose**: Code coverage measurement
- **Key Features Used**:
  - Line coverage
  - Branch coverage
  - HTML reports
  - Coverage thresholds

**Acceptance Criteria**:
- [ ] Can measure utility coverage: `pytest --cov=src/langchain_llm`
- [ ] Can measure example coverage: `pytest --cov=examples`
- [ ] Can measure combined coverage: `pytest --cov=src/langchain_llm --cov=examples`
- [ ] Can generate HTML report: `pytest --cov --cov-report=html`
- [ ] Coverage data accurate for all modules
- [ ] Utilities achieve >80% coverage (target: ~93%)
- [ ] Examples achieve >80% coverage (target: ~89%)

### TR-004.2: Code Quality Tools
**Purpose**: Linting, formatting, and style enforcement

#### ruff
- **Version**: ^0.1.0
- **Purpose**: Fast Python linter and formatter (replaces flake8, black, isort)
- **Key Features Used**:
  - Linting (`ruff check`)
  - Auto-fixing (`ruff check --fix`)
  - Formatting (`ruff format`)
  - Import sorting
  - 130 character line length

**Acceptance Criteria**:
- [ ] `ruff check .` runs without errors
- [ ] `ruff format .` formats all Python files
- [ ] Configuration in pyproject.toml
- [ ] All code passes ruff checks

**Configuration** (`pyproject.toml`):
```toml
[tool.ruff]
line-length = 130
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]
ignore = []

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

### TR-004.3: Interactive Development
**Purpose**: Jupyter notebook support for examples

#### jupyter
- **Version**: ^1.0.0
- **Purpose**: Interactive notebook environment
- **Key Features Used**:
  - Notebook execution
  - Code cells + markdown cells
  - Inline output display
  - Integration with Poetry/pip venv

**Acceptance Criteria**:
- [ ] `jupyter notebook` launches successfully
- [ ] Can execute all example notebooks
- [ ] Notebook kernel uses correct Python environment
- [ ] Examples produce expected output in notebooks

#### ipykernel
- **Version**: ^6.25.0 (often installed with jupyter)
- **Purpose**: IPython kernel for Jupyter
- **Key Features Used**:
  - Kernel installation: `python -m ipykernel install --user --name=ead-langchain`
  - Environment isolation

---

## TR-005: Project Structure

### TR-005.1: Package Layout
**Requirement**: Src-layout packaging structure

```
ead-langchain-template/
├── src/
│   └── langchain_llm/           # Package root
│       ├── __init__.py          # Public API exports
│       ├── interfaces.py        # Protocol/ABC definitions (NEW)
│       ├── config.py            # Configuration management
│       └── logging_config.py    # Logging utilities
├── examples/                     # Progressive examples
│   ├── 01_basic.py
│   ├── 01_basic.ipynb
│   ├── 02_streaming.py
│   ├── 02_streaming.ipynb
│   ├── 03_conversation.py
│   ├── 03_conversation.ipynb
│   ├── 04_advanced.py
│   └── 04_advanced.ipynb
├── tests/                        # Test suite
│   ├── conftest.py              # Shared fixtures
│   ├── test_config.py           # Config module tests
│   ├── test_logging.py          # Logging module tests
│   └── enforcement/             # Quality enforcement tests
│       ├── __init__.py
│       ├── test_sphinx_docstrings.py
│       └── test_no_emojis.py
├── docs/                         # Documentation
│   └── complete/                # AI-executable blueprints
│       ├── requirements/
│       ├── designs/
│       ├── phases/
│       └── tasks/
├── .github/
│   └── copilot-instructions.md  # AI assistant guidelines
├── pyproject.toml               # Poetry config + tool settings
├── requirements.txt             # pip dependencies
├── .env.example                 # Environment variable template
├── .gitignore                   # Git ignore rules
└── README.md                    # User documentation
```

**Rationale for Src-Layout**:
- Prevents accidental imports of development version
- Forces proper package installation
- Cleaner separation of package vs project
- Industry best practice

**Acceptance Criteria**:
- [ ] Package code in `src/langchain_llm/`
- [ ] Examples in top-level `examples/`
- [ ] Tests in top-level `tests/`
- [ ] Cannot import package without installation
- [ ] `pip install -e .` or `poetry install` required

### TR-005.2: File Naming Conventions

#### Python Modules
- **Pattern**: `snake_case.py`
- **Examples**: `config.py`, `logging_config.py`, `interfaces.py`

#### Test Files
- **Pattern**: `test_<module>.py`
- **Examples**: `test_config.py`, `test_logging.py`
- **Location**: Mirror source structure in `tests/`

#### Example Files
- **Pattern**: `0X_<name>.py` and `0X_<name>.ipynb`
- **Examples**: `01_basic.py`, `02_streaming.ipynb`
- **Sequential Numbering**: 01, 02, 03, 04, ... (pad with zero)

#### Documentation Files
- **Pattern**: `NNN-<name>.md` for ordered docs, `<name>.md` for others
- **Examples**: `000-overview.md`, `001-functional-requirements.md`, `README.md`

**Acceptance Criteria**:
- [ ] All files follow naming conventions
- [ ] No camelCase, PascalCase, or kebab-case filenames
- [ ] Numbered files properly zero-padded
- [ ] All markdown files use `.md` extension

---

## TR-006: Version Control

### TR-006.1: Git Configuration
**Requirement**: Git repository with proper ignore rules

**Gitignore Requirements**:
```gitignore
# Environment variables (NEVER commit secrets)
.env
*.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
ENV/

# Poetry
poetry.lock  # or commit it for reproducible builds (project decision)

# Testing
.coverage
.pytest_cache/
htmlcov/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# Jupyter
.ipynb_checkpoints/
*.ipynb_checkpoints

# OS
.DS_Store
Thumbs.db
```

**Acceptance Criteria**:
- [ ] .gitignore file exists and is comprehensive
- [ ] .env files never committed
- [ ] __pycache__ directories ignored
- [ ] IDE-specific files ignored
- [ ] No secrets in repository history

### TR-006.2: GitHub Structure
**Requirement**: GitHub repository setup

**Required Files**:
- `.github/copilot-instructions.md` - AI coding assistant guidelines
- `README.md` - User-facing documentation
- `LICENSE` - Open source license (if applicable)

**Optional But Recommended**:
- `.github/ISSUE_TEMPLATE/` - Issue templates
- `.github/PULL_REQUEST_TEMPLATE.md` - PR template
- `.github/workflows/` - CI/CD (future)

**Acceptance Criteria**:
- [ ] .github/copilot-instructions.md exists
- [ ] README.md is comprehensive
- [ ] Repository is properly initialized
- [ ] Remote origin is set

---

## TR-007: Environment Variables

### TR-007.1: Naming Convention
**Requirement**: Namespaced environment variables with `EADLANGCHAIN_` prefix

**Pattern**: `EADLANGCHAIN_<TYPE>_<KEY>`

**Types**:
- `AI` - AI provider configuration
- `LOG` - Logging configuration
- `DB` - Database configuration (future)
- `APP` - Application settings (future)

**Examples**:
```bash
# AI Provider Keys
EADLANGCHAIN_AI_OPENAI_API_KEY=sk-...
EADLANGCHAIN_AI_ANTHROPIC_API_KEY=sk-ant-...
EADLANGCHAIN_AI_GEMINI_API_KEY=...

# Optional Model Overrides
EADLANGCHAIN_AI_OPENAI_MODEL=gpt-4o
EADLANGCHAIN_AI_ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
EADLANGCHAIN_AI_GEMINI_MODEL=gemini-2.0-flash-exp

# Logging Configuration
EADLANGCHAIN_LOG_LEVEL=INFO
EADLANGCHAIN_LOG_FILE=logs/app.log
```

**Rationale**:
- Prevents conflicts with system/other project variables
- Clear ownership and grouping
- Easy to grep/filter
- Professional/enterprise pattern

**Acceptance Criteria**:
- [ ] All env vars use `EADLANGCHAIN_` prefix
- [ ] Vars are organized by type (AI, LOG, etc.)
- [ ] .env.example documents all variables
- [ ] No generic names like `OPENAI_API_KEY`

### TR-007.2: .env.example Template
**Requirement**: Example environment file with documentation

**Contents**:
```bash
# EAD LangChain Template - Environment Configuration Template
#
# Copy this file to .env and fill in your API keys:
#   cp .env.example .env
#
# IMPORTANT: Never commit .env to version control!

# ============================================================================
# AI Provider API Keys (at least one required)
# ============================================================================

# OpenAI API Key
# Get yours at: https://platform.openai.com/api-keys
EADLANGCHAIN_AI_OPENAI_API_KEY=your-openai-api-key-here

# Anthropic API Key
# Get yours at: https://console.anthropic.com/settings/keys
EADLANGCHAIN_AI_ANTHROPIC_API_KEY=your-anthropic-api-key-here

# Google Gemini API Key
# Get yours at: https://aistudio.google.com/app/apikey
EADLANGCHAIN_AI_GEMINI_API_KEY=your-google-api-key-here

# ============================================================================
# Optional Configuration
# ============================================================================

# Logging Level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
# Default: INFO
# EADLANGCHAIN_LOG_LEVEL=INFO

# Log File Path (optional - logs to console if not set)
# EADLANGCHAIN_LOG_FILE=logs/app.log

# Default Model Overrides (optional)
# EADLANGCHAIN_AI_OPENAI_MODEL=gpt-4o
# EADLANGCHAIN_AI_ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
# EADLANGCHAIN_AI_GEMINI_MODEL=gemini-2.0-flash-exp
```

**Acceptance Criteria**:
- [ ] .env.example exists and is complete
- [ ] All required variables documented
- [ ] Links to get API keys included
- [ ] Default values shown in comments
- [ ] Clear copy instructions at top

---

## TR-008: API Provider Requirements

### TR-008.1: OpenAI
- **API Version**: OpenAI API v1
- **Models Used**: gpt-5-nano (default), gpt-5-mini, gpt-5, gpt-4o
- **Features**: Chat completions, streaming, function calling
- **API Key Format**: Starts with `sk-` or `sk-proj-`
- **Rate Limits**: Respect OpenAI tier limits
- **Temperature Constraint**: GPT-5 models (gpt-5-nano, gpt-5-mini, gpt-5) require `temperature=1.0`. Only gpt-5-chat-latest and GPT-4o support custom temperature values.
- **Documentation**: https://platform.openai.com/docs

**Acceptance Criteria**:
- [ ] Works with OpenAI API v1
- [ ] Handles authentication errors gracefully
- [ ] Respects API rate limits
- [ ] Streaming works correctly
- [ ] Error messages reference OpenAI docs
- [ ] Temperature parameter correctly set for GPT-5 models (1.0 required)

### TR-008.2: Anthropic
- **API Version**: Anthropic API 2024-01
- **Models Used**: claude-3-haiku-20240307 (default), claude-3-5-sonnet-20241022, claude-haiku-4-5
- **Features**: Messages API, streaming, tool use
- **API Key Format**: Starts with `sk-ant-`
- **Rate Limits**: Respect Anthropic tier limits
- **Documentation**: https://docs.anthropic.com

**Acceptance Criteria**:
- [ ] Works with Anthropic Messages API
- [ ] Handles authentication errors gracefully
- [ ] Respects API rate limits
- [ ] Streaming works correctly
- [ ] Error messages reference Anthropic docs

### TR-008.3: Google Gemini
- **API Version**: Gemini API v1
- **Models Used**: gemini-2.0-flash-lite (default), gemini-2.5-flash, gemini-2.0-flash, gemini-1.5-pro
- **Features**: Generate content, streaming, multi-modal (future)
- **API Key Format**: Alphanumeric string
- **Rate Limits**: Respect Google API quotas
- **Documentation**: https://ai.google.dev/docs

**Acceptance Criteria**:
- [ ] Works with Gemini API v1
- [ ] Handles authentication errors gracefully
- [ ] Respects API rate limits
- [ ] Streaming works correctly
- [ ] Error messages reference Google docs

---

## TR-009: Documentation Requirements

### TR-009.1: Docstring Standard
**Requirement**: Sphinx-style docstrings for all code

**Format Example**:
```python
def function_name(param1: str, param2: int) -> str:
    """
    Brief description of function.

    Longer description if needed. Can span multiple paragraphs.

    :param param1: Description of param1
    :ptype param1: str
    :param param2: Description of param2
    :ptype param2: int
    :return: Description of return value
    :rtype: str
    :raises ValueError: When param1 is invalid
    :raises KeyError: When required key is missing

    Example usage::

        result = function_name("test", 42)
        print(result)
    """
    pass
```

**Acceptance Criteria**:
- [ ] All public functions have docstrings
- [ ] All classes have docstrings
- [ ] All modules have module docstrings
- [ ] Format is strictly Sphinx-style (no Google/NumPy)
- [ ] Enforcement test validates all docstrings

**Enforcement**: `tests/enforcement/test_sphinx_docstrings.py` scans all Python files

### TR-009.2: Type Hints
**Requirement**: Type hints for all function signatures

**Usage**:
```python
from typing import Optional, Dict, List

def get_config(name: str, default: Optional[str] = None) -> str:
    pass

def process_data(items: List[Dict[str, str]]) -> Dict[str, int]:
    pass
```

**Acceptance Criteria**:
- [ ] All function parameters have type hints
- [ ] All return types specified
- [ ] Optional types use Optional[] or | None
- [ ] Complex types use typing module

---

## TR-010: Quality Gates

### TR-010.1: Pre-Commit Checks
**Requirement**: All code must pass quality checks before commit

**Checks**:
1. **Ruff Linting**: `ruff check .`
2. **Ruff Formatting**: `ruff format .`
3. **Pytest**: `pytest tests/`
4. **Enforcement Tests**: `pytest tests/enforcement/`

**Acceptance Criteria**:
- [ ] All ruff checks pass
- [ ] Code is properly formatted
- [ ] All tests pass (0 failures)
- [ ] Enforcement tests pass (Sphinx docstrings, no emojis)

### TR-010.2: Test Coverage Target
**Requirement**: Maintain >80% test coverage for utility modules

**Scope**:
- `src/langchain_llm/config.py` - Must have >80% coverage
- `src/langchain_llm/logging_config.py` - Must have >80% coverage
- `src/langchain_llm/interfaces.py` - Must have >80% coverage
- Examples - Not required to have tests

**Measurement**: `pytest --cov=src/langchain_llm --cov-report=term --cov-report=html`

**Acceptance Criteria**:
- [ ] Overall coverage >80%
- [ ] Each utility module >80%
- [ ] Coverage report generated
- [ ] No critical code paths untested

---

## TR-011: Performance Requirements

### TR-011.1: Package Import Time
**Requirement**: Package import completes in <1 second

**Measurement**:
```python
import time
start = time.time()
import langchain_llm
elapsed = time.time() - start
assert elapsed < 1.0
```

**Acceptance Criteria**:
- [ ] Cold import <1 second
- [ ] No heavy computations during import
- [ ] No network calls during import
- [ ] Lazy loading of heavy dependencies

### TR-011.2: Example Execution Time
**Requirement**: Examples complete in <10 seconds (excluding LLM API calls)

**Measurement**: Time from start to first LLM call

**Acceptance Criteria**:
- [ ] Setup code runs quickly
- [ ] Configuration loading fast
- [ ] No unnecessary delays
- [ ] Examples don't hang or timeout

---

## TR-012: Security Requirements

### TR-012.1: Secret Management
**Requirement**: No secrets in code or version control

**Rules**:
- All API keys via environment variables
- .env files in .gitignore
- No hardcoded credentials
- No secrets in logs
- No secrets in error messages

**Acceptance Criteria**:
- [ ] .env in .gitignore
- [ ] No API keys in code
- [ ] Logs don't contain secrets
- [ ] Error messages don't leak keys
- [ ] Git history clean (no committed secrets)

### TR-012.2: Dependency Security
**Requirement**: Use trusted, maintained dependencies

**Checks**:
- All dependencies from PyPI
- No deprecated packages
- Known vulnerabilities checked (optional: safety, pip-audit)
- Version pinning in poetry.lock

**Acceptance Criteria**:
- [ ] All dependencies from official sources
- [ ] No deprecated packages
- [ ] Version lockfile exists
- [ ] Regular dependency updates

---

## Related Documents

- **Previous**: [001-functional-requirements.md](001-functional-requirements.md) - Feature requirements
- **Next**: [003-environment-conventions.md](003-environment-conventions.md) - Configuration patterns
- **See Also**:
  - [004-quality-requirements.md](004-quality-requirements.md) - Testing and quality
  - [designs/001-project-structure.md](../designs/001-project-structure.md) - Structure implementation

## Document Metadata

- **Version**: 1.0
- **Status**: Active
- **Owner**: EAD LangChain Template Team
