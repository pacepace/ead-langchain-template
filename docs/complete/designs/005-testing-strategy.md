# Design 005: Testing Strategy

## Document Purpose

This document specifies the complete testing strategy for the EAD LangChain Template, including Test-Driven Development (TDD) methodology, test organization, fixtures, coverage targets, and enforcement testing.

---

## Overview

### Testing Philosophy

**Test-Driven Development (TDD)**: Mandatory for all utility modules

**TDD Workflow**:
1. **RED**: Write tests first (they fail - code doesn't exist)
2. **GREEN**: Write minimal code to pass tests
3. **REFACTOR**: Improve code while tests stay green

**Coverage Goals**:
- Utility modules (src/): >80% coverage
- Examples: Manual testing (not unit tested)
- Documentation: No testing required

**Test Categories**:
1. **Unit Tests**: Test individual functions/classes (written in TDD)
2. **Integration Tests**: Test module interactions
3. **Enforcement Tests**: Code quality gates (meta-testing)

---

## Test-Driven Development (TDD) Process

### The Red-Green-Refactor Cycle

```
┌──────────────────────────────────────────────────────────┐
│ 1. RED: Write a Failing Test                             │
│    - Define expected behavior                             │
│    - Write test that will fail (feature doesn't exist)   │
│    - Run test, confirm it fails                          │
└──────────────────────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│ 2. GREEN: Write Minimal Code to Pass                     │
│    - Implement just enough to make test pass             │
│    - No extra features                                   │
│    - Run test, confirm it passes                         │
└──────────────────────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│ 3. REFACTOR: Improve Code While Keeping Tests Green      │
│    - Clean up code                                       │
│    - Remove duplication                                  │
│    - Improve names, structure                            │
│    - Run tests, confirm still passing                    │
└──────────────────────────────────────────────────────────┘
                         │
                         ▼
                    (Repeat for next feature)
```

### TDD Example Walkthrough

**Scenario**: Implementing `validate_provider()` function

**IMPORTANT**: In this template, tasks 006-007 follow TDD. Tests are written FIRST in the RED phase, implementation comes SECOND in GREEN phase.

#### Step 1: RED (Write Failing Test FIRST)

**Create the test file with failing tests:**

```python
# tests/unit/test_config.py

def test_validate_provider_with_valid_key(mock_env_vars):
    """Test that validate_provider succeeds when key is set."""
    from langchain_llm import load_env_config, validate_provider

    load_env_config()
    # Should not raise any exception
    validate_provider("openai")


def test_validate_provider_with_missing_key():
    """Test that validate_provider raises ConfigError when key is missing."""
    from langchain_llm import validate_provider, ConfigError
    import pytest

    with pytest.raises(ConfigError):
        validate_provider("openai")
```

**Run Test (MUST FAIL)**:
```bash
pytest tests/unit/test_config.py::test_validate_provider_with_valid_key -v
```

**Expected Result**: `FAILED` (ImportError or ModuleNotFoundError - code doesn't exist yet)

**This is correct!** Tests MUST fail in RED phase because implementation doesn't exist.

#### Step 2: GREEN (Minimal Implementation)

```python
# src/langchain_llm/config.py

def validate_provider(provider: str) -> None:
    """Validate that a provider is configured with an API key."""
    get_api_key(provider, required=True)
```

**Run Test**:
```bash
pytest tests/unit/test_config.py::test_validate_provider_with_valid_key -v
```

**Expected Result**: `PASSED`

#### Step 3: REFACTOR (Add Documentation, Improve)

```python
# src/langchain_llm/config.py

def validate_provider(provider: str) -> None:
    """
    Validate that a provider is configured with an API key.

    :param provider: Provider name to validate
    :ptype provider: str
    :return: None
    :rtype: None
    :raises ConfigError: If provider is not configured

    Example::

        >>> from langchain_llm import validate_provider
        >>> validate_provider("openai")  # Raises ConfigError if not configured
    """
    get_api_key(provider, required=True)
```

**Run All Tests**:
```bash
pytest tests/unit/test_config.py -v
```

**Expected Result**: All tests still `PASSED`

**Repeat**: Move to next feature, start with RED again

---

## Test Organization

### Directory Structure

```
tests/
├── conftest.py                # Shared fixtures
├── test_config.py             # Tests for config.py
├── test_logging.py            # Tests for logging_config.py
└── enforcement/               # Code quality enforcement
    ├── __init__.py
    ├── test_sphinx_docstrings.py
    └── test_no_emojis.py
```

### Test File Naming

**Pattern**: `test_<module_name>.py`

**Mapping**:
- `src/langchain_llm/config.py` → `tests/unit/test_config.py`
- `src/langchain_llm/logging_config.py` → `tests/unit/test_logging.py`
- `src/langchain_llm/interfaces.py` → `tests/unit/test_interfaces.py` (if needed)

### Test Function Naming

**Pattern**: `test_<function>_<scenario>`

**Examples**:
- `test_get_api_key_with_valid_key`
- `test_get_api_key_with_missing_key_required`
- `test_get_api_key_with_missing_key_optional`
- `test_get_api_key_case_insensitive`
- `test_get_api_key_invalid_provider`

**Benefits**:
- Descriptive, self-documenting
- Groups related tests together
- Easy to identify what failed

### Test Class Organization (Optional)

**Pattern**: Group related tests in classes

```python
class TestGetApiKey:
    """Tests for get_api_key function."""

    def test_with_valid_key(self, mock_env_vars):
        """Test with valid API key."""
        key = get_api_key("openai")
        assert key == "test-openai-key"

    def test_with_missing_key_required(self, clean_env):
        """Test that missing key raises ConfigError when required."""
        with pytest.raises(ConfigError):
            get_api_key("openai", required=True)

    def test_with_missing_key_optional(self, clean_env):
        """Test that missing key returns None when optional."""
        key = get_api_key("openai", required=False)
        assert key is None
```

**Benefits**:
- Logical grouping
- Shared setup via class-level fixtures
- Clear test organization

---

## pytest Configuration

### pyproject.toml Settings

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --strict-markers --tb=short"  # --tb=short for more readable test failures
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
]
```

**Settings Explained**:
- `testpaths`: Where to look for tests
- `python_files`: Test file pattern
- `python_classes`: Test class pattern (optional grouping)
- `python_functions`: Test function pattern
- `addopts`: Default command-line options
  - `-v`: Verbose output
  - `--strict-markers`: Fail on unknown markers
  - `--tb=short`: Shorter traceback format for more readable test failures
- `markers`: Custom test markers

### Running Tests

**All Tests**:
```bash
pytest
```

**Specific File**:
```bash
pytest tests/unit/test_config.py
```

**Specific Test**:
```bash
pytest tests/unit/test_config.py::test_get_api_key_with_valid_key
```

**Specific Class**:
```bash
pytest tests/unit/test_config.py::TestGetApiKey
```

**With Coverage**:
```bash
pytest --cov=src/langchain_llm --cov-report=term --cov-report=html
```

**Verbose Output**:
```bash
pytest -v
```

**Very Verbose (show output)**:
```bash
pytest -vv -s
```

**Only Fast Tests**:
```bash
pytest -m "not slow"
```

---

## Test Fixtures

### conftest.py - Shared Fixtures

**Purpose**: Reusable test setup/teardown

```python
# tests/conftest.py

import pytest
import os
from pathlib import Path


@pytest.fixture
def mock_env_vars(monkeypatch):
    """
    Mock environment variables for testing.

    Sets up test API keys for all providers.
    Uses monkeypatch for proper isolation.

    Usage::

        def test_something(mock_env_vars):
            # API keys are now set
            key = get_api_key("openai")
            assert key == "test-openai-key"
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

    Usage::

        def test_error_handling(clean_env):
            # No API keys set
            with pytest.raises(ConfigError):
                get_api_key("openai")
    """
    for key in list(os.environ.keys()):
        if key.startswith("EADLANGCHAIN_"):
            monkeypatch.delenv(key, raising=False)


@pytest.fixture
def temp_env_file(tmp_path):
    """
    Create a temporary .env file for testing.

    Returns path to the temp file.

    Usage::

        def test_env_loading(temp_env_file):
            load_env_config(str(temp_env_file))
            key = get_api_key("openai")
            assert key == "test-key-from-file"
    """
    env_file = tmp_path / ".env"
    env_file.write_text("""
EADLANGCHAIN_AI_OPENAI_API_KEY=test-key-from-file
EADLANGCHAIN_LOG_LEVEL=INFO
""")
    return env_file


@pytest.fixture
def temp_project_root(tmp_path, monkeypatch):
    """
    Create a temporary project root with pyproject.toml.

    Useful for testing project root detection.

    Usage::

        def test_project_detection(temp_project_root):
            # temp_project_root has pyproject.toml
            root = find_project_root()
            assert root == temp_project_root
    """
    (tmp_path / "pyproject.toml").touch()
    monkeypatch.chdir(tmp_path)
    return tmp_path


@pytest.fixture
def capture_logs():
    """
    Capture log output for testing.

    Returns a StringIO object containing captured logs.

    Usage::

        def test_logging(capture_logs):
            logger = get_logger(__name__)
            logger.info("Test message")
            output = capture_logs.getvalue()
            assert "Test message" in output
    """
    import logging
    from io import StringIO

    stream = StringIO()
    handler = logging.StreamHandler(stream)
    logger = logging.getLogger()
    original_level = logger.level
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    yield stream

    logger.removeHandler(handler)
    logger.setLevel(original_level)
```

### Fixture Scopes

**Function Scope** (default):
```python
@pytest.fixture  # Runs for each test function
def my_fixture():
    return "value"
```

**Module Scope**:
```python
@pytest.fixture(scope="module")  # Runs once per test module
def expensive_setup():
    # Expensive operation
    return result
```

**Session Scope**:
```python
@pytest.fixture(scope="session")  # Runs once per test session
def database():
    # One-time setup for all tests
    return db_connection
```

---

## Test Coverage Strategy

### Coverage Targets

**Minimum Coverage**:
- Overall: ≥80%
- `config.py`: ≥80%
- `logging_config.py`: ≥80%
- `interfaces.py`: ≥80%
- `__init__.py`: ≥80% (simple exports)

### Measuring Coverage

**Command**:
```bash
pytest --cov=src/langchain_llm --cov-report=term --cov-report=html
```

**Terminal Report**:
```
---------- coverage: platform darwin, python 3.10.12 -----------
Name                                  Stmts   Miss  Cover
---------------------------------------------------------
src/langchain_llm/__init__.py             4      0   100%
src/langchain_llm/config.py              45      3    93%
src/langchain_llm/interfaces.py          12      0   100%
src/langchain_llm/logging_config.py      38      2    95%
---------------------------------------------------------
TOTAL                                    99      5    95%
```

**HTML Report**:
- Opens `htmlcov/index.html` in browser
- Shows line-by-line coverage
- Highlights uncovered lines in red
- Interactive exploration

### What to Cover

**Must Cover**:
- All public functions
- All error paths (except/raise blocks)
- Edge cases (empty strings, None, invalid input)
- Configuration variations

**Can Skip**:
- `if __name__ == "__main__":` blocks
- Example scripts (manual testing)
- Documentation

### Coverage Example

**Function to Test**:
```python
def get_api_key(provider: str, required: bool = True) -> str | None:
    provider = provider.lower()

    if provider not in PROVIDER_MAP:
        raise ValueError(f"Unknown provider: {provider}")

    env_var = PROVIDER_MAP[provider]
    api_key = os.getenv(env_var)

    if required and not api_key:
        raise ConfigError(f"API key not found for provider '{provider}'")

    return api_key
```

**Tests Needed for 100% Coverage**:
```python
def test_get_api_key_valid(mock_env_vars):
    """Cover: normal path, key exists."""
    key = get_api_key("openai")
    assert key == "test-openai-key"


def test_get_api_key_case_insensitive(mock_env_vars):
    """Cover: provider.lower() line."""
    key = get_api_key("OpenAI")  # Mixed case
    assert key == "test-openai-key"


def test_get_api_key_invalid_provider():
    """Cover: ValueError path."""
    with pytest.raises(ValueError):
        get_api_key("invalid_provider")


def test_get_api_key_missing_required():
    """Cover: ConfigError path."""
    with pytest.raises(ConfigError):
        get_api_key("openai", required=True)


def test_get_api_key_missing_optional(clean_env):
    """Cover: return None path."""
    key = get_api_key("openai", required=False)
    assert key is None
```

**Result**: 100% coverage of `get_api_key()`

---

## Unit Testing Patterns

### Testing Functions

**Basic Pattern**:
```python
def test_function_name_with_valid_input():
    """Test function with valid input."""
    # Arrange: Set up test data
    input_value = "test"

    # Act: Call function
    result = function_name(input_value)

    # Assert: Check result
    assert result == expected_value
```

### Testing Exception Handling

**Pattern**: Use `pytest.raises`

```python
def test_function_raises_error_on_invalid_input():
    """Test that function raises ValueError for invalid input."""
    with pytest.raises(ValueError) as exc_info:
        function_name("invalid")

    # Optionally check error message
    assert "invalid" in str(exc_info.value)
```

### Testing with Fixtures

**Pattern**: Use fixtures for setup

```python
def test_with_mocked_environment(mock_env_vars):
    """Test using mock environment variables."""
    # mock_env_vars fixture has already set up environment
    result = function_that_reads_env()
    assert result is not None
```

### Parametrized Tests

**Pattern**: Test multiple inputs with one test

```python
@pytest.mark.parametrize("provider,env_var", [
    ("openai", "EADLANGCHAIN_AI_OPENAI_API_KEY"),
    ("anthropic", "EADLANGCHAIN_AI_ANTHROPIC_API_KEY"),
    ("gemini", "EADLANGCHAIN_AI_GEMINI_API_KEY"),
])
def test_provider_env_var_mapping(provider, env_var):
    """Test that each provider maps to correct env var."""
    result = get_env_var_name(provider)
    assert result == env_var
```

**Benefits**:
- Reduces test duplication
- Tests multiple scenarios
- Clear test names in output

---

## Enforcement Testing

### Purpose

Automated enforcement of code quality standards:
1. **Sphinx Docstrings**: Ensure all docstrings use Sphinx format
2. **No Emojis**: Prevent emoji characters in code

### test_sphinx_docstrings.py

**Purpose**: Detect non-Sphinx docstring styles

```python
# tests/enforcement/test_sphinx_docstrings.py

import pytest
from pathlib import Path
import re


def test_no_google_style_docstrings():
    """Ensure no Google-style docstrings (Args:, Returns:) exist."""
    src_dir = Path("src")
    violations = []

    for py_file in src_dir.rglob("*.py"):
        if "__pycache__" in str(py_file):
            continue

        content = py_file.read_text()

        # Check for Google-style markers
        google_pattern = r'^\s*(Args|Returns|Raises|Yields|Note):\s*$'
        if re.search(google_pattern, content, re.MULTILINE):
            violations.append(str(py_file))

    assert not violations, (
        f"Google-style docstrings found in:\n  " +
        "\n  ".join(violations) +
        "\n\nUse Sphinx-style docstrings instead. "
        "See .github/copilot-instructions.md for format."
    )


def test_no_numpy_style_docstrings():
    """Ensure no NumPy-style docstrings exist."""
    src_dir = Path("src")
    tests_dir = Path("tests")
    violations = []

    for directory in [src_dir, tests_dir]:
        for py_file in directory.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue

            content = py_file.read_text()

            # Check for NumPy-style markers (Parameters followed by dashes)
            numpy_pattern = r'^\s*Parameters\s*\n\s*-+\s*$'
            if re.search(numpy_pattern, content, re.MULTILINE):
                violations.append(str(py_file))

    assert not violations, (
        f"NumPy-style docstrings found in:\n  " +
        "\n  ".join(violations)
    )
```

**Run**:
```bash
pytest tests/enforcement/test_sphinx_docstrings.py -v
```

**Output on Failure**:
```
FAILED tests/enforcement/test_sphinx_docstrings.py::test_no_google_style_docstrings
AssertionError: Google-style docstrings found in:
  src/langchain_llm/config.py
  src/langchain_llm/logging_config.py

Use Sphinx-style docstrings instead. See .github/copilot-instructions.md for format.
```

### test_no_emojis.py

**Purpose**: Prevent emoji characters in code

```python
# tests/enforcement/test_no_emojis.py

import pytest
from pathlib import Path
import re


# Emoji regex pattern (comprehensive)
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U00002702-\U000027B0"  # dingbats
    "\U000024C2-\U0001F251"
    "]+",
    flags=re.UNICODE
)


def test_no_emojis_in_code():
    """Ensure no emoji characters in Python code."""
    src_dirs = [Path("src"), Path("tests"), Path("examples")]
    violations = []

    for src_dir in src_dirs:
        if not src_dir.exists():
            continue

        for py_file in src_dir.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue

            content = py_file.read_text()

            # Find emojis
            if EMOJI_PATTERN.search(content):
                violations.append(str(py_file))

    assert not violations, (
        f"Emoji characters found in code files:\n  " +
        "\n  ".join(violations) +
        "\n\nEmojis can cause encoding issues. Use descriptive text instead."
    )
```

**Run**:
```bash
pytest tests/enforcement/ -v
```

---

## Integration Testing

### Testing Module Interactions

**Example**: Test config + logging integration

```python
def test_config_and_logging_integration(mock_env_vars, temp_project_root):
    """Test that config and logging work together."""
    from langchain_llm import setup_logging, load_env_config, get_api_key, get_logger

    # Setup both systems
    setup_logging(level="DEBUG")
    load_env_config()

    # Get logger and API key
    logger = get_logger(__name__)
    api_key = get_api_key("openai")

    # Log API key retrieval (safely)
    logger.debug(f"Retrieved API key for OpenAI (length: {len(api_key)})")

    # Verify both worked
    assert api_key == "test-openai-key"
```

### Testing Protocol Conformance

**Example**: Test that implementation conforms to protocol

```python
def test_env_config_provider_implements_protocol():
    """Test that EnvConfigProvider conforms to ConfigProvider protocol."""
    from langchain_llm.interfaces import ConfigProvider
    from langchain_llm.config import EnvConfigProvider

    # Create instance
    config = EnvConfigProvider()

    # Check protocol conformance (type checker validates this)
    def use_config(provider: ConfigProvider):
        """Function that expects ConfigProvider protocol."""
        return provider.get_key("openai", required=False)

    # Should work without type errors
    result = use_config(config)

    # Runtime checks
    assert hasattr(config, "get_key")
    assert hasattr(config, "get_all_keys")
    assert hasattr(config, "validate")
    assert hasattr(config, "get_model_name")
```

---

## Test Execution Strategy

### Local Development

**Quick Check** (run frequently):
```bash
pytest -v
```

**With Coverage** (before commit):
```bash
pytest --cov=src/langchain_llm --cov-report=term
```

**Full Check** (before push):
```bash
# Run all tests with coverage and HTML report
pytest --cov=src/langchain_llm --cov-report=term --cov-report=html

# Run enforcement tests
pytest tests/enforcement/ -v

# Run ruff checks
ruff check .
```

### Continuous Integration (Future)

**GitHub Actions** (future enhancement):
```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install poetry
          poetry install
      - name: Run tests
        run: poetry run pytest --cov
      - name: Run enforcement tests
        run: poetry run pytest tests/enforcement/
```

---

## Related Documents

- **Previous**: [004-examples-design.md](004-examples-design.md) - Examples design
- **Next**: [006-documentation-strategy.md](006-documentation-strategy.md) - Documentation strategy
- **See Also**:
  - [requirements/004-quality-requirements.md](../requirements/004-quality-requirements.md) - Quality requirements
  - [000-architecture-overview.md](000-architecture-overview.md) - TDD principle

## Document Metadata

- **Version**: 1.0
- **Status**: Active
- **Owner**: EAD LangChain Template Team
