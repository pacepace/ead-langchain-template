# Requirements 004: Quality Requirements

## Document Purpose

This document defines quality standards, testing requirements, and enforcement mechanisms for the EAD LangChain Template. It establishes the Test-Driven Development (TDD) methodology and automated quality gates.

---

## QR-001: Test-Driven Development (TDD)

### QR-001.1: TDD Mandate

**Requirement**: All utility code MUST be developed using TDD methodology

**TDD Cycle** (Red-Green-Refactor):
1. **Red**: Write a failing test first
2. **Green**: Write minimal code to make the test pass
3. **Refactor**: Improve code while keeping tests green
4. **Repeat**: Continue for next feature

**Scope**:
- **MUST follow TDD**: All code in `src/langchain_llm/`
- **MUST have tests**: Example code in `examples/` (with >80% coverage)
- **Documentation**: No tests required

**Note on Example Tests**:
Examples are tested using mocked LLM responses to avoid actual API calls. This demonstrates how to test LLM-dependent code and serves as a teaching tool for testing patterns in production applications.

**Rationale**:
- Ensures code is testable by design
- Documents expected behavior
- Catches regressions early
- Forces thinking about interfaces
- Builds confidence in refactoring

**Acceptance Criteria**:
- [ ] All functions in `src/langchain_llm/` have unit tests
- [ ] Tests exist before implementation (verified by git history)
- [ ] All tests pass: `pytest`
- [ ] TDD process documented in README and copilot-instructions.md

### QR-001.2: TDD Workflow Example

**Scenario**: Adding a new function `validate_provider()`

**Step 1 - Red** (Write Failing Test):
```python
# tests/unit/test_config.py
def test_validate_provider_with_valid_key(mock_env_vars):
    """Test that validate_provider succeeds when key is set."""
    load_env_config()
    validate_provider("openai")  # Should not raise

def test_validate_provider_with_missing_key():
    """Test that validate_provider raises ConfigError when key is missing."""
    with pytest.raises(ConfigError):
        validate_provider("openai")
```

**Run Test**: `pytest tests/unit/test_config.py::test_validate_provider_with_valid_key -v`
**Expected**: Test fails (function doesn't exist yet)

**Step 2 - Green** (Minimal Implementation):
```python
# src/langchain_llm/config.py
def validate_provider(provider: str) -> None:
    """Validate that a provider is configured with an API key."""
    get_api_key(provider, required=True)
```

**Run Test**: `pytest tests/unit/test_config.py::test_validate_provider_with_valid_key -v`
**Expected**: Test passes

**Step 3 - Refactor** (Improve):
```python
def validate_provider(provider: str) -> None:
    """
    Validate that a provider is configured with an API key.

    :param provider: Provider name to validate
    :ptype provider: str
    :return: None
    :rtype: None
    :raises ConfigError: If provider is not configured
    """
    get_api_key(provider, required=True)
```

**Run All Tests**: `pytest tests/unit/test_config.py -v`
**Expected**: All tests still pass

**Acceptance Criteria**:
- [ ] Tests written before implementation
- [ ] Minimal code to pass tests
- [ ] Refactoring doesn't break tests
- [ ] Process documented for contributors

---

## QR-002: Test Coverage Requirements

### QR-002.1: Coverage Targets

**Requirement**: Maintain high test coverage for all utility modules

**Targets**:
- **Utilities**: ≥80% for `src/langchain_llm/` (currently ~94%)
- **Examples**: ≥80% for `examples/` (currently ~89%)
- **Per-Module Coverage**:
  - `config.py`: ≥80% (currently ~100%)
  - `logging_config.py`: ≥80% (currently ~90%)
  - `interfaces.py`: ≥80% (currently ~92%)
  - `__init__.py`: ≥80% (currently 100%)
  - `01_basic.py`: ≥80% (currently ~94%)
  - `02_streaming.py`: ≥80% (currently ~87%)
  - `03_conversation.py`: ≥80% (currently ~84%)
  - `04_advanced.py`: ≥80% (currently ~92%)

**Measurement**:
```bash
# Utility coverage
pytest --cov=src/langchain_llm --cov-report=term

# Example coverage
pytest --cov=examples --cov-report=term

# Combined coverage
pytest --cov=src/langchain_llm --cov=examples --cov-report=term --cov-report=html
```

**Exclusions**:
- Enforcement tests themselves
- Documentation
- Scripts (scripts/sync_notebooks.py has integration tests)

**Acceptance Criteria**:
- [ ] Coverage measured with pytest-cov
- [ ] HTML coverage report generated
- [ ] All modules meet target coverage
- [ ] Coverage enforced in code review

### QR-002.2: Coverage Quality (Not Just Quantity)

**Requirement**: Tests must meaningfully exercise code, not just touch lines

**Good Test** (tests behavior):
```python
def test_get_api_key_returns_correct_value(mock_env_vars):
    """Test that get_api_key returns the correct API key from environment."""
    load_env_config()
    key = get_api_key("openai")
    assert key == "test-openai-key"
    assert key.startswith("test-")
```

**Bad Test** (just touches code):
```python
def test_get_api_key_runs():
    """Test that get_api_key runs without error."""
    try:
        get_api_key("openai", required=False)
    except:
        pass  # Ignore errors, just want coverage
```

**What to Test**:
- **Happy Path**: Function works with valid input
- **Error Cases**: Function handles invalid input correctly
- **Edge Cases**: Boundary conditions (empty strings, None, etc.)
- **Integration**: Functions work together correctly

**Acceptance Criteria**:
- [ ] Tests verify behavior, not just execution
- [ ] Both success and failure paths tested
- [ ] Edge cases covered
- [ ] Assertions check actual vs expected values

---

## QR-003: pytest Configuration

### QR-003.1: Test Discovery

**Requirement**: Automatic test discovery with consistent naming

**Configuration** (`pyproject.toml`):
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --strict-markers --tb=short"  # --tb=short for more readable test failures
```

**Test File Structure**:
```
tests/
├── conftest.py                # Shared fixtures
├── test_config.py             # Tests for config.py
├── test_logging.py            # Tests for logging_config.py
└── enforcement/
    ├── __init__.py
    ├── test_sphinx_docstrings.py
    └── test_no_emojis.py
```

**Naming Conventions**:
- **Test Files**: `test_<module>.py`
- **Test Functions**: `test_<function_name>_<scenario>`
- **Test Classes**: `Test<ClassName>` (optional, for grouping)
- **Fixtures**: Descriptive names (e.g., `mock_env_vars`, `temp_env_file`)

**Acceptance Criteria**:
- [ ] `pytest` discovers all test files automatically
- [ ] Test naming follows conventions
- [ ] pytest.ini_options configured in pyproject.toml
- [ ] All tests run with single `pytest` command

### QR-003.2: Fixtures and Test Helpers

**Requirement**: Shared test utilities via conftest.py

**Common Fixtures**:

```python
# tests/conftest.py
import pytest
from unittest.mock import patch
import os

@pytest.fixture
def mock_env_vars(monkeypatch):
    """
    Mock environment variables for testing.

    Sets up test API keys for all providers.
    """
    monkeypatch.setenv("EADLANGCHAIN_AI_OPENAI_API_KEY", "test-openai-key")
    monkeypatch.setenv("EADLANGCHAIN_AI_ANTHROPIC_API_KEY", "test-anthropic-key")
    monkeypatch.setenv("EADLANGCHAIN_AI_GEMINI_API_KEY", "test-gemini-key")
    monkeypatch.setenv("EADLANGCHAIN_LOG_LEVEL", "DEBUG")

@pytest.fixture
def clean_env(monkeypatch):
    """
    Remove all EADLANGCHAIN environment variables.

    Useful for testing error handling when variables are missing.
    """
    for key in list(os.environ.keys()):
        if key.startswith("EADLANGCHAIN_"):
            monkeypatch.delenv(key, raising=False)

@pytest.fixture
def temp_env_file(tmp_path):
    """
    Create a temporary .env file for testing.

    Returns path to the temp file.
    """
    env_file = tmp_path / ".env"
    env_file.write_text("""
EADLANGCHAIN_AI_OPENAI_API_KEY=test-key
EADLANGCHAIN_LOG_LEVEL=INFO
""")
    return env_file
```

**Usage**:
```python
def test_get_api_key_with_valid_key(mock_env_vars):
    """Test get_api_key with valid environment variables."""
    key = get_api_key("openai")
    assert key == "test-openai-key"

def test_get_api_key_with_missing_key(clean_env):
    """Test get_api_key raises error when key is missing."""
    with pytest.raises(ConfigError):
        get_api_key("openai", required=True)
```

**Acceptance Criteria**:
- [ ] conftest.py exists with shared fixtures
- [ ] Fixtures use monkeypatch for environment isolation
- [ ] Fixtures documented with docstrings
- [ ] Tests use fixtures to avoid duplication

### QR-003.3: Test Execution

**Requirement**: Multiple ways to run tests for different scenarios

**Run All Tests**:
```bash
pytest
```

**Run Specific Test File**:
```bash
pytest tests/unit/test_config.py
```

**Run Specific Test**:
```bash
pytest tests/unit/test_config.py::test_get_api_key_with_valid_key
```

**Run with Verbose Output**:
```bash
pytest -v
```

**Run with Coverage**:
```bash
pytest --cov=src/langchain_llm --cov-report=term --cov-report=html
```

**Run Only Enforcement Tests**:
```bash
pytest tests/enforcement/
```

**Acceptance Criteria**:
- [ ] All test run modes work
- [ ] Output is clear and readable
- [ ] Failed tests show helpful error messages
- [ ] Coverage reports generated correctly

---

## QR-004: Code Quality Tools

### QR-004.1: Ruff Configuration

**Requirement**: All code must pass Ruff linting and formatting

**Configuration** (`pyproject.toml`):
```toml
[tool.ruff]
line-length = 130
target-version = "py310"
exclude = [
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".venv",
    "venv",
    "*.ipynb_checkpoints",
]

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "F",   # pyflakes
    "I",   # isort (import sorting)
    "N",   # pep8-naming
    "W",   # pycodestyle warnings
    "UP",  # pyupgrade (modern Python syntax)
]
ignore = []

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
line-ending = "auto"
```

**Rules**:
- **Line Length**: Maximum 130 characters
- **Import Sorting**: Automatic with isort rules
- **Naming**: PEP 8 conventions enforced
- **Modern Python**: Suggest Python 3.10+ patterns

**Commands**:
```bash
# Check for issues
ruff check .

# Fix auto-fixable issues
ruff check --fix .

# Format all Python files
ruff format .

# Check and format in one go
ruff check --fix . && ruff format .
```

**Acceptance Criteria**:
- [ ] `ruff check .` passes with zero errors
- [ ] All code formatted with `ruff format`
- [ ] Configuration in pyproject.toml
- [ ] Pre-commit hook recommended (optional)

### QR-004.2: Style Guidelines

**Requirement**: Consistent code style throughout project

**Imports**:
```python
# Standard library
import os
from pathlib import Path
from typing import Optional, Dict, List

# Third-party
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Local
from langchain_llm import get_api_key, setup_logging
```

**Order**: Standard library → Third-party → Local
**Sorting**: Alphabetical within each group
**Enforcement**: Ruff with isort rules

**Function Definitions**:
```python
def function_name(
    param1: str,
    param2: int,
    param3: Optional[str] = None,
) -> Dict[str, any]:
    """
    Docstring here.

    :param param1: Description
    :ptype param1: str
    ...
    """
    pass
```

**Long Lines**:
```python
# If function signature exceeds 130 chars, break it:
def very_long_function_name(
    parameter_one: str,
    parameter_two: int,
    parameter_three: Optional[str] = None,
    parameter_four: Dict[str, any] = None,
) -> bool:
    pass

# If string exceeds 130 chars, break it:
message = (
    "This is a very long message that would exceed the line length limit "
    "so we break it across multiple lines using parentheses."
)
```

**Acceptance Criteria**:
- [ ] Import order consistent across all files
- [ ] Function signatures follow pattern
- [ ] Long lines properly broken
- [ ] Ruff enforces automatically

---

## QR-005: Documentation Requirements

### QR-005.1: Sphinx Docstring Standard

**Requirement**: ALL Python code must use Sphinx-style docstrings

**Mandatory For**:
- All public functions
- All classes
- All modules (module-level docstring at top)
- All methods (including private if complex)

**NOT Allowed**:
- Google-style docstrings (Args:, Returns:)
- NumPy-style docstrings (Parameters, Returns sections)
- Plain docstrings without parameter documentation

**Enforcement**: Automated test scans all .py files

**Format Reference**:
```python
def function_name(param1: str, param2: int = 0) -> Optional[str]:
    """
    Brief one-line description.

    Longer description can go here. Multiple paragraphs are fine.
    Explain what the function does, not how it does it.

    :param param1: What param1 is used for
    :ptype param1: str
    :param param2: What param2 is used for
    :ptype param2: int
    :return: What the function returns
    :rtype: Optional[str]
    :raises ValueError: When param1 is empty
    :raises ConfigError: When configuration is invalid

    Example usage::

        result = function_name("test", 42)
        if result:
            print(result)

    .. note::
        Additional notes can go in special directives.

    .. warning::
        Warning about potential issues.
    """
    pass
```

**Acceptance Criteria**:
- [ ] All public functions have Sphinx docstrings
- [ ] All parameters documented with :param and :ptype
- [ ] All return values documented with :return and :rtype
- [ ] Exceptions documented with :raises
- [ ] Enforcement test validates format

### QR-005.2: Type Hints Requirement

**Requirement**: All function signatures must include type hints

**Required Type Hints**:
- All parameter types
- All return types
- Use `Optional[T]` or `T | None` for optional values
- Use generics for collections: `List[str]`, `Dict[str, int]`

**Example**:
```python
from typing import Optional, Dict, List, Any

def process_config(
    config_dict: Dict[str, Any],
    required_keys: List[str],
    default_value: Optional[str] = None,
) -> Dict[str, str]:
    """Process configuration dictionary."""
    pass
```

**Acceptance Criteria**:
- [ ] All parameters have type hints
- [ ] All return types specified
- [ ] Complex types use typing module
- [ ] Type hints match docstring documentation

### QR-005.3: Code Comments

**Requirement**: Comments where code intent isn't obvious

**When to Comment**:
- **Why**, not **what**: Explain reasoning, not implementation
- **Complex algorithms**: Help future maintainers
- **Workarounds**: Explain why workaround is needed
- **TODOs**: Mark future improvements

**When NOT to Comment**:
- Self-explanatory code
- Repeating function/variable names
- Obvious operations

**Good Comments**:
```python
# Search upward for .env file so examples can run from any directory
for parent in [current] + list(current.parents):
    env_path = parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        return

# Workaround for LangChain issue #1234 - remove when fixed
if hasattr(response, "_raw"):
    content = response._raw.get("content")
```

**Bad Comments**:
```python
# Get the API key
api_key = get_api_key("openai")  # Bad: obvious from code

# Set x to 5
x = 5  # Bad: redundant

# This function gets the configuration
def get_config():  # Bad: docstring is for this
    pass
```

**Acceptance Criteria**:
- [ ] Comments explain why, not what
- [ ] Complex logic has explanatory comments
- [ ] No redundant comments
- [ ] Comments are clear and helpful

---

## QR-006: Enforcement Tests

### QR-006.1: Sphinx Docstring Checker

**Requirement**: Automated test to enforce Sphinx-style docstrings

**Test**: `tests/enforcement/test_sphinx_docstrings.py`

**What It Checks**:
- All .py files in `src/` and `tests/` (except `__pycache__`)
- Detects Google-style docstrings (Args:, Returns:)
- Detects NumPy-style docstrings (Parameters, -------)
- Fails build if non-Sphinx docstrings found

**Implementation**:
```python
import pytest
from pathlib import Path
import re

def test_no_google_style_docstrings():
    """Ensure no Google-style docstrings (Args:, Returns:) exist."""
    src_dir = Path("src")
    violations = []

    for py_file in src_dir.rglob("*.py"):
        content = py_file.read_text()

        # Check for Google-style markers
        if re.search(r'^\s*(Args|Returns|Raises|Yields|Note):\s*$', content, re.MULTILINE):
            violations.append(str(py_file))

    assert not violations, f"Google-style docstrings found in: {violations}"

def test_no_numpy_style_docstrings():
    """Ensure no NumPy-style docstrings exist."""
    src_dir = Path("src")
    violations = []

    for py_file in src_dir.rglob("*.py"):
        content = py_file.read_text()

        # Check for NumPy-style markers
        if re.search(r'^\s*Parameters\s*\n\s*-+\s*$', content, re.MULTILINE):
            violations.append(str(py_file))

    assert not violations, f"NumPy-style docstrings found in: {violations}"
```

**Acceptance Criteria**:
- [ ] Test exists and runs automatically with pytest
- [ ] Detects Google-style docstrings
- [ ] Detects NumPy-style docstrings
- [ ] Fails with clear error message showing violating files
- [ ] Runs fast (< 1 second)

### QR-006.2: No Emoji Checker

**Requirement**: Automated test to prevent emojis in code

**Test**: `tests/enforcement/test_no_emojis.py`

**Rationale**:
- Emojis cause encoding issues
- Not professional for production code
- Can break on some systems
- Documentation and comments can use emojis (just not code)

**What It Checks**:
- All .py files in `src/`, `tests/`, `examples/`
- Detects emoji characters in code
- Excludes comments and docstrings (regex-based)
- Fails build if emojis found in code

**Implementation**:
```python
import pytest
from pathlib import Path
import re

# Emoji regex pattern
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags
    "]+",
    flags=re.UNICODE
)

def test_no_emojis_in_code():
    """Ensure no emoji characters in Python code."""
    src_dirs = [Path("src"), Path("examples")]
    violations = []

    for src_dir in src_dirs:
        for py_file in src_dir.rglob("*.py"):
            content = py_file.read_text()

            # Find emojis in code
            if EMOJI_PATTERN.search(content):
                violations.append(str(py_file))

    assert not violations, f"Emojis found in code files: {violations}"
```

**Acceptance Criteria**:
- [ ] Test exists and runs automatically
- [ ] Detects emoji characters
- [ ] Fails with clear error message
- [ ] Runs fast
- [ ] Can be updated if emoji patterns change

---

## QR-007: Continuous Quality

### QR-007.1: Pre-Commit Checklist

**Requirement**: All checks must pass before committing code

**Manual Checklist**:
```bash
# 1. Run all tests
pytest

# 2. Check test coverage
pytest --cov=src/langchain_llm --cov-report=term

# 3. Run Ruff linting
ruff check .

# 4. Run Ruff formatting
ruff format .

# 5. Run enforcement tests
pytest tests/enforcement/

# All must pass before committing!
```

**Automated Pre-Commit Hook** (optional enhancement):
```bash
# .git/hooks/pre-commit
#!/bin/bash
pytest && ruff check . && ruff format --check .
```

**Acceptance Criteria**:
- [ ] Checklist documented in CONTRIBUTING.md (if exists)
- [ ] All checks can be run locally
- [ ] Clear pass/fail indication
- [ ] Fast enough to run frequently (< 30 seconds total)

### QR-007.2: Quality Gates

**Requirement**: Define what "done" means for any code change

**Definition of Done**:
- [ ] **Tests Written**: All new code has tests (TDD)
- [ ] **Tests Pass**: `pytest` returns 0 failures
- [ ] **Coverage Met**: Coverage ≥80% for changed modules
- [ ] **Ruff Clean**: `ruff check .` returns 0 errors
- [ ] **Formatted**: `ruff format .` applied
- [ ] **Docstrings Added**: All new functions have Sphinx docstrings
- [ ] **Enforcement Passes**: No Google/NumPy docstrings, no emojis
- [ ] **Examples Updated**: If public API changed, examples reflect changes
- [ ] **Documentation Updated**: README and copilot-instructions.md if needed

**Acceptance Criteria**:
- [ ] Definition of Done documented
- [ ] All items checkable/verifiable
- [ ] Team follows Definition of Done
- [ ] Code review enforces

---

## QR-008: Performance Requirements

### QR-008.1: Test Execution Time

**Requirement**: Test suite must be fast enough to run frequently

**Targets**:
- Unit tests: < 10 seconds total
- Enforcement tests: < 5 seconds total
- Coverage report: < 15 seconds total
- **Total test time**: < 30 seconds

**Strategies**:
- Use mocks to avoid slow operations (file I/O, network calls)
- Parametrize tests to reduce duplication
- Parallel test execution (pytest-xdist, optional)

**Measurement**:
```bash
pytest --durations=10  # Show 10 slowest tests
```

**Acceptance Criteria**:
- [ ] Test suite completes in < 30 seconds
- [ ] No single test takes > 5 seconds
- [ ] Tests use appropriate fixtures
- [ ] Slow tests identified and optimized

### QR-008.2: Code Complexity

**Requirement**: Keep functions simple and testable

**Targets**:
- Cyclomatic complexity: < 10 per function
- Function length: < 50 lines (guideline, not hard rule)
- Class size: < 300 lines (guideline)

**Tools** (optional):
- radon (complexity metrics)
- pylint (code quality scores)

**Acceptance Criteria**:
- [ ] Functions are small and focused
- [ ] Complex functions refactored into smaller parts
- [ ] Easy to understand and test
- [ ] Code review catches overly complex code

---

## QR-009: Documentation Quality

### QR-009.1: README Completeness

**Requirement**: README must be comprehensive and up-to-date

**Required Sections**:
- [ ] Project description
- [ ] Features list
- [ ] Quick start (< 10 minutes to setup)
- [ ] Installation (Poetry and pip)
- [ ] Configuration (.env setup)
- [ ] Usage examples
- [ ] Project structure
- [ ] Testing instructions
- [ ] Contributing guidelines
- [ ] Troubleshooting

**Acceptance Criteria**:
- [ ] New user can set up project from README alone
- [ ] All code examples in README work
- [ ] Links to API key signup pages included
- [ ] Screenshots/examples where helpful
- [ ] Updated when functionality changes

### QR-009.2: Code Example Quality

**Requirement**: All code examples must be runnable and correct

**Requirements**:
- Examples actually run without modification
- Error handling shown where appropriate
- Clear comments explaining steps
- Realistic, useful scenarios (not just "foo/bar")
- Both Python scripts and Jupyter notebooks

**Acceptance Criteria**:
- [ ] Can copy-paste examples and they work
- [ ] Examples tested manually
- [ ] Jupyter notebooks have been executed (output cells present)
- [ ] Python scripts run successfully: `python examples/01_basic.py`

---

## QR-010: Security Quality

### QR-010.1: No Secrets in Code or Repo

**Requirement**: Zero tolerance for committed secrets

**Checks**:
- .env files in .gitignore
- No API keys in code
- No API keys in test files (use fixtures with fake keys)
- No secrets in git history

**Tools** (optional):
- git-secrets (scans for secrets)
- gitleaks (finds secrets in history)
- trufflehog (secret scanning)

**Acceptance Criteria**:
- [ ] .env in .gitignore
- [ ] No hardcoded API keys found
- [ ] Tests use mock/fake keys
- [ ] Git history clean (no secrets found)
- [ ] Code review catches hardcoded secrets

### QR-010.2: Dependency Safety

**Requirement**: Use only trusted, maintained dependencies

**Checks**:
- All dependencies from official PyPI
- No deprecated packages
- Pinned versions in poetry.lock
- Regular dependency updates

**Tools** (optional):
- `safety check` - Checks for known vulnerabilities
- `pip-audit` - Audits Python dependencies
- Dependabot (GitHub automation)

**Acceptance Criteria**:
- [ ] Dependencies from trusted sources
- [ ] poetry.lock committed (reproducible builds)
- [ ] No known vulnerabilities (if scanning enabled)
- [ ] Dependencies reviewed before adding

---

## Related Documents

- **Previous**: [003-environment-conventions.md](003-environment-conventions.md) - Configuration patterns
- **Next**: [designs/000-architecture-overview.md](../designs/000-architecture-overview.md) - System design
- **See Also**:
  - [designs/005-testing-strategy.md](../designs/005-testing-strategy.md) - Detailed testing design

## Document Metadata

- **Version**: 1.0
- **Status**: Active
- **Owner**: EAD LangChain Template Team
