# Task 007: Logging Module

## Task Context

**Phase**: 02 - Core Interfaces & Utilities
**Sequence**: Seventh task (second of Phase 02)
**Complexity**: High
**Output**: ~600 LOC (tests + fixtures + interfaces + implementation)

### Why This Task Exists

Standardized logging helps:
- Debug issues with detailed context (file, class, function, line)
- Understand application flow
- Track errors consistently
- Maintain professional code standards

This task follows **Test-Driven Development** (same process as task 006):
1. **RED**: Write tests first
2. **GREEN**: Write minimal implementation
3. **REFACTOR**: Improve quality

### Where This Fits

```
Task 006 → Task 007 (YOU ARE HERE) → Task 008
Config      Logging Module              Exports/Ruff
Module
```

---

## Prerequisites

### Completed Tasks

- [x] **Task 006**: Config module with TDD process complete

### Required Knowledge

**Python Logging**:
- `logging.Logger`, `logging.Handler`, `logging.Formatter`
- LogRecord attributes
- Root logger configuration

**Abstract Base Classes**:
- When to use ABC vs Protocol
- `@abstractmethod` decorator
- ABC inheritance

**Frame Inspection**:
- `inspect.currentframe()`
- Accessing caller locals
- Finding class context

---

## Research Required

### Code from Prior Tasks

**Study from Task 004**:
- `tests/conftest.py`: Basic fixture structure
- Purpose: Understand how to add new fixtures

**Study from Task 006**:
- `tests/unit/test_config.py`: Test organization pattern (classes, docstrings)
- `tests/conftest.py`: Existing fixtures (mock_env_vars, clean_env, temp_env_file)
- `src/langchain_llm/interfaces.py`: Protocol pattern (use for LogFormatter ABC)
- `src/langchain_llm/config.py`: Module structure, docstring examples
- Purpose: Follow same patterns for logging module

### No Forward References

- `src/langchain_llm/logging_config.py` doesn't exist yet (create in GREEN)
- `tests/unit/test_logging.py` doesn't exist yet (create in RED)
- LogFormatter ABC doesn't exist yet (create in GREEN)

### External Documentation

**Python Logging**:
- https://docs.python.org/3/library/logging.html
- LogRecord attributes
- Custom formatters

**Frame Inspection**:
- https://docs.python.org/3/library/inspect.html
- `currentframe()` usage

---

## Task Description

### Objective

Implement custom logging with enhanced formatting using Test-Driven Development: write tests first (RED), implement to pass (GREEN), refactor for quality (REFACTOR).

---

## STEP 1: RED - Write Failing Tests

### 1.1: Create Test File Structure

Create `tests/unit/test_logging.py`:

```python
"""
Tests for the logging_config module.

Demonstrates testing logging configuration and custom formatters.

Run these tests with: pytest tests/unit/test_logging.py -v
"""

import logging
from pathlib import Path

import pytest

from langchain_llm.logging_config import CustomFormatter, get_logger, setup_logging
```

### 1.2: Create Required Fixtures

Add these to `tests/conftest.py` (append to file from task 006):

**Fixture: capture_logs** (captures log output for testing):
```python
@pytest.fixture
def capture_logs():
    """
    Fixture that captures log output for testing.

    Creates a StringIO stream and adds it as a handler to the root logger.
    Automatically cleans up after the test completes.

    :return: StringIO stream containing captured log output
    :rtype: io.StringIO

    Usage::

        def test_logging_output(capture_logs):
            from langchain_llm import setup_logging, get_logger
            setup_logging(level="INFO")
            logger = get_logger(__name__)
            logger.info("Test message")

            output = capture_logs.getvalue()
            assert "Test message" in output
    """
    from io import StringIO

    # Create string buffer
    log_stream = StringIO()

    # Create and configure handler
    handler = logging.StreamHandler(log_stream)
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    handler.setFormatter(formatter)

    # Add to root logger
    root_logger = logging.getLogger()
    original_level = root_logger.level
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.DEBUG)

    yield log_stream

    # Cleanup
    root_logger.removeHandler(handler)
    root_logger.setLevel(original_level)
```

**Fixture: reset_logging** (auto-cleanup, already exists from research - verify it's in conftest.py):
```python
@pytest.fixture(autouse=True)
def reset_logging():
    """
    Automatically reset logging configuration after each test.
    This prevents test pollution from logging setup.
    """
    yield

    # Clear all handlers from root logger
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(logging.WARNING)
```

**Note**: `project_root` and `temp_project_root` fixtures may already exist from task 006. If not, add them:
```python
@pytest.fixture
def project_root():
    """
    Fixture that provides the project root directory.

    :return: Path to project root
    :rtype: Path
    """
    # Go up from tests/ to project root
    return Path(__file__).parent.parent


@pytest.fixture
def temp_project_root(tmp_path, monkeypatch):
    """
    Fixture that creates a temporary project root with markers.

    :param tmp_path: Pytest fixture providing temporary directory
    :param monkeypatch: Pytest fixture for modifying environment
    :return: Path to temporary project root
    :rtype: Path
    """
    # Create pyproject.toml marker
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text('[tool.poetry]\nname = "test-project"\n')

    # Change to temp directory
    monkeypatch.chdir(tmp_path)

    return tmp_path
```

### 1.3: Write All Test Functions

Create comprehensive tests in `tests/unit/test_logging.py`:

**Tests for CustomFormatter**:
```python
class TestCustomFormatter:
    """Tests for CustomFormatter class."""

    def test_formatter_initialization(self):
        """Test that formatter initializes correctly."""
        formatter = CustomFormatter()
        assert formatter is not None
        assert isinstance(formatter.project_root, Path)

    def test_formatter_with_custom_project_root(self, tmp_path):
        """
        Test formatter with custom project root.

        :param tmp_path: Pytest fixture providing temporary directory
        """
        formatter = CustomFormatter(project_root=tmp_path)
        assert formatter.project_root == tmp_path

    def test_find_project_root(self, project_root):
        """
        Test that _find_project_root locates the project root.

        :param project_root: Pytest fixture providing project root path
        """
        formatter = CustomFormatter()
        # Should find project root with pyproject.toml
        assert (formatter.project_root / "pyproject.toml").exists() or (
            formatter.project_root / ".git"
        ).exists()

    def test_format_adds_relative_path(self):
        """Test that format adds relative_path to log record."""
        formatter = CustomFormatter(fmt="%(relative_path)s - %(message)s")

        # Create a log record
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname=__file__,
            lineno=1,
            msg="Test message",
            args=(),
            exc_info=None,
        )

        # Format the record
        formatter.format(record)

        # Check that relative_path was added
        assert hasattr(record, "relative_path")
        assert "test_logging" in record.relative_path

    def test_format_adds_metaclass_name(self):
        """Test that format adds metaclass_name to log record."""
        formatter = CustomFormatter(fmt="%(metaclass_name)s%(message)s")

        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname=__file__,
            lineno=1,
            msg="Test message",
            args=(),
            exc_info=None,
        )

        formatter.format(record)

        # Check that metaclass_name was added (may be empty string)
        assert hasattr(record, "metaclass_name")
        assert isinstance(record.metaclass_name, str)

    def test_format_removes_py_extension(self):
        """Test that .py extension is removed from relative_path."""
        formatter = CustomFormatter(fmt="%(relative_path)s")

        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname=__file__,
            lineno=1,
            msg="Test",
            args=(),
            exc_info=None,
        )

        formatted = formatter.format(record)
        assert ".py" not in formatted
```

**Tests for setup_logging()**:
```python
class TestSetupLogging:
    """Tests for setup_logging function."""

    def test_setup_logging_default(self):
        """Test setting up logging with defaults."""
        logger = setup_logging()
        assert logger is not None
        assert logger == logging.getLogger()
        assert len(logger.handlers) > 0

    def test_setup_logging_with_level(self):
        """Test setting up logging with specific level."""
        logger = setup_logging(level="DEBUG")
        assert logger.level == logging.DEBUG

    def test_setup_logging_with_log_file(self, tmp_path):
        """
        Test setting up logging with file output.

        :param tmp_path: Pytest fixture providing temporary directory
        """
        log_file = tmp_path / "test.log"
        setup_logging(log_file=str(log_file))

        # Check that file handler was added
        root_logger = logging.getLogger()
        file_handlers = [h for h in root_logger.handlers if isinstance(h, logging.FileHandler)]
        assert len(file_handlers) > 0

    def test_setup_logging_from_env_var(self, monkeypatch):
        """Test reading log level from environment variable."""
        monkeypatch.setenv("EADLANGCHAIN_LOG_LEVEL", "ERROR")
        logger = setup_logging()
        assert logger.level == logging.ERROR

    def test_setup_logging_creates_log_directory(self, tmp_path):
        """
        Test that setup_logging creates parent directories for log file.

        :param tmp_path: Pytest fixture
        """
        log_file = tmp_path / "logs" / "nested" / "test.log"
        setup_logging(log_file=str(log_file))

        assert log_file.parent.exists()

    def test_setup_logging_idempotent(self):
        """Test that calling setup_logging multiple times doesn't duplicate handlers."""
        setup_logging()
        handler_count = len(logging.getLogger().handlers)

        setup_logging()
        new_handler_count = len(logging.getLogger().handlers)

        assert new_handler_count == handler_count
```

**Tests for get_logger()**:
```python
class TestGetLogger:
    """Tests for get_logger function."""

    def test_get_logger_returns_logger(self):
        """Test that get_logger returns a Logger instance."""
        logger = get_logger(__name__)
        assert isinstance(logger, logging.Logger)

    def test_get_logger_with_same_name(self):
        """Test that loggers with same name return same instance."""
        logger1 = get_logger("test")
        logger2 = get_logger("test")
        assert logger1 is logger2

    def test_get_logger_inherits_root_config(self, capture_logs):
        """
        Test that get_logger inherits config from root logger.

        :param capture_logs: Pytest fixture
        """
        setup_logging(level="INFO")
        logger = get_logger(__name__)
        logger.info("Test message")

        output = capture_logs.getvalue()
        assert "Test message" in output
```

**Integration Tests**:
```python
class TestLoggingIntegration:
    """Integration tests for logging module."""

    def test_logging_output_format(self, capture_logs):
        """
        Test the complete logging format.

        :param capture_logs: Pytest fixture
        """
        setup_logging(level="INFO")
        logger = get_logger(__name__)
        logger.info("Integration test message")

        output = capture_logs.getvalue()
        assert "Integration test message" in output
        assert "INFO" in output

    def test_logging_with_config_module(self, mock_env_vars):
        """
        Test logging integrates with config module.

        :param mock_env_vars: Pytest fixture from task 006
        """
        from langchain_llm import load_env_config

        load_env_config()
        setup_logging()  # Should read EADLANGCHAIN_LOG_LEVEL

        logger = get_logger(__name__)
        assert logger.level == logging.INFO  # From mock_env_vars
```

### 1.4: Run Tests - Expect FAILURE

RED phase - tests MUST fail:

```bash
pytest tests/unit/test_logging.py -v
```

**Expected**: ImportError or ModuleNotFoundError (logging_config doesn't exist)

---

## STEP 2: GREEN - Implement to Pass Tests

### 2.1: Add LogFormatter ABC to interfaces.py

Open `src/langchain_llm/interfaces.py` and add LogFormatter ABC:

```python
import logging
from abc import ABC, abstractmethod

# ... existing ConfigProvider protocol ...


class LogFormatter(ABC):
    """
    Abstract base class for log formatters.

    This ABC defines the interface that all log formatters must implement.
    It enables different formatting strategies (enhanced, JSON, cloud logging)
    while maintaining a consistent interface.

    Example implementations:
    - CustomFormatter: Enhanced format with project context (default)
    - JSONFormatter: JSON structured logging (future)
    - CloudLogFormatter: Cloud-specific format (future)

    Why ABC instead of Protocol:
    - logging.Formatter is already a class (inheritance expected)
    - Need to override specific methods from base Formatter
    - Clear inheritance hierarchy desirable
    """

    @abstractmethod
    def format(self, record: logging.LogRecord) -> str:
        """
        Format a log record into a string.

        Subclasses must implement this method to define their
        formatting strategy. Typically, they will enhance the
        LogRecord with additional attributes before calling
        the parent format() method.

        :param record: The log record to format
        :ptype record: logging.LogRecord
        :return: Formatted log string
        :rtype: str
        """
        pass
```

### 2.2: Create Logging Module

Create `src/langchain_llm/logging_config.py`:

**Module Docstring and Imports**:
```python
"""
Custom logging configuration for EAD LangChain Template.

Provides a standardized logging format that includes:
- Log level
- Timestamp
- Relative path from project root
- Class name (if applicable)
- Module, function, and line number
- Log message

Format: %(levelname)-8s %(asctime)s %(relative_path)s.%(metaclass_name)s%(funcName)s.%(lineno)d: %(message)s
"""

import logging
import os
from pathlib import Path

from langchain_llm.interfaces import LogFormatter
```

**CustomFormatter Class**:
```python
class CustomFormatter(logging.Formatter, LogFormatter):
    """
    Custom formatter that adds relative_path and metaclass_name to log records.

    This formatter enriches log records with:
    - relative_path: Path relative to the project root
    - metaclass_name: Class name if the log is called from within a class method
    """

    def __init__(
        self, fmt: str | None = None, datefmt: str | None = None, project_root: Path | None = None
    ):
        """Initialize formatter with optional project root."""
        super().__init__(fmt, datefmt)
        self.project_root = project_root or self._find_project_root()

    @staticmethod
    def _find_project_root() -> Path:
        """
        Find the project root by looking for pyproject.toml or .git directory.
        Falls back to current working directory if not found.
        """
        current = Path.cwd()
        for parent in [current] + list(current.parents):
            if (parent / "pyproject.toml").exists() or (parent / ".git").exists():
                return parent
        return current

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record with custom attributes.

        Adds:
        - relative_path: Path relative to project root
        - metaclass_name: Class name or empty string if not in a class
        """
        # Calculate relative path
        try:
            file_path = Path(record.pathname)
            relative_path = file_path.relative_to(self.project_root)
            record.relative_path = str(relative_path).replace(os.sep, ".")
            # Remove .py extension
            if record.relative_path.endswith(".py"):
                record.relative_path = record.relative_path[:-3]
        except (ValueError, AttributeError):
            record.relative_path = record.module

        # Try to extract class name from the stack
        metaclass_name = ""
        try:
            import inspect

            frame = inspect.currentframe()
            if frame and frame.f_back and frame.f_back.f_back:
                caller_frame = frame.f_back.f_back
                caller_locals = caller_frame.f_locals

                # Check if 'self' exists (instance method)
                if "self" in caller_locals:
                    metaclass_name = caller_locals["self"].__class__.__name__
                # Check if 'cls' exists (class method)
                elif "cls" in caller_locals:
                    metaclass_name = caller_locals["cls"].__name__
        except Exception:
            pass

        record.metaclass_name = f"{metaclass_name}." if metaclass_name else ""

        return super().format(record)
```

**setup_logging() Function**:
```python
def setup_logging(
    level: str | None = None,
    log_file: str | None = None,
    format_string: str | None = None,
) -> logging.Logger:
    """
    Set up logging with custom formatting.

    :param level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    :param log_file: Optional path to log file
    :param format_string: Optional custom format string
    :return: Configured root logger
    """
    # Determine log level
    if level is None:
        level = os.getenv("EADLANGCHAIN_LOG_LEVEL", "INFO")

    # Default format string
    if format_string is None:
        format_string = (
            "%(levelname)-8s %(asctime)s "
            "%(relative_path)s.%(metaclass_name)s%(funcName)s.%(lineno)d: "
            "%(message)s"
        )

    # Create formatter
    formatter = CustomFormatter(fmt=format_string, datefmt="%Y-%m-%d %H:%M:%S")

    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))

    # Clear existing handlers (idempotent)
    root_logger.handlers.clear()

    # Add console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Add file handler if requested
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    return root_logger
```

**get_logger() Function**:
```python
def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.

    This is a simple wrapper around logging.getLogger() for convenience.
    The logger will inherit configuration from the root logger.

    :param name: Logger name (typically __name__)
    :return: Logger instance
    """
    return logging.getLogger(name)
```

### 2.3: Run Tests - Expect SUCCESS

GREEN phase - tests should PASS:

```bash
pytest tests/unit/test_logging.py -v
```

**Expected**: All tests PASSED

---

## STEP 3: REFACTOR - Improve Quality

### 3.1: Add Comprehensive Docstrings

Add complete Sphinx docstrings to all functions (same pattern as task 006). Refer to `src/langchain_llm/config.py` from task 006 for docstring examples.

**Update CustomFormatter methods**:
```python
def __init__(self, fmt: str | None = None, datefmt: str | None = None, project_root: Path | None = None):
    """
    Initialize the custom formatter.

    :param fmt: Format string for log messages
    :ptype fmt: Optional[str]
    :param datefmt: Date format string
    :ptype datefmt: Optional[str]
    :param project_root: Project root directory for relative paths
    :ptype project_root: Optional[Path]
    """
    # ... implementation
```

Add complete docstrings to all other methods and functions.

### 3.2: Run Tests After Each Change

After EVERY refactoring change:

```bash
pytest tests/unit/test_logging.py -v
```

Must stay GREEN.

### 3.3: Run Enforcement Tests

```bash
pytest tests/enforcement/ -v
```

All must PASS (Sphinx docstrings, no emojis).

### 3.4: Check Coverage

```bash
pytest tests/unit/test_logging.py --cov=src/langchain_llm/logging_config --cov-report=term
```

**Target**: >80% coverage

---

## Success Criteria

### Functional

- [ ] All tests in test_logging.py pass
- [ ] Coverage >80% for logging_config.py
- [ ] Can manually test:
  ```python
  from langchain_llm import setup_logging, get_logger
  setup_logging(level="DEBUG")
  logger = get_logger(__name__)
  logger.info("Test")
  # Should show enhanced format
  ```

### Quality

- [ ] All functions have Sphinx docstrings
- [ ] All parameters documented
- [ ] Enforcement tests pass
- [ ] `ruff check src/langchain_llm/` passes

### TDD Process

- [ ] Tests written FIRST (RED)
- [ ] Implementation SECOND (GREEN)
- [ ] Refactoring THIRD (REFACTOR)
- [ ] Tests stayed green throughout

---

## Constraints

- Frame inspection must not crash (try/except)
- Project root detection must have fallback (cwd)
- Format string must be customizable
- Line length ≤130 chars
- No emojis

---

## Troubleshooting

**Issue**: Tests fail after refactoring
**Solution**: Revert changes, ensure tests pass, refactor more carefully

**Issue**: Frame inspection crashes tests
**Solution**: Wrap in try/except, return empty string on failure

**Issue**: Relative path calculation fails
**Solution**: Check project root detection, add fallback to module name

---

## Next Steps

1. **Validate**:
   ```bash
   pytest tests/unit/test_logging.py -v
   pytest --cov=src/langchain_llm/logging_config --cov-report=term
   pytest tests/enforcement/ -v
   ```

2. **Move to Task 008**:
   - Package exports and ruff configuration

---

## Related Documents

**Design**: [003-logging-design.md](../designs/003-logging-design.md)
**Phase**: [phase-02-core-interfaces-utilities.md](../phases/phase-02-core-interfaces-utilities.md)
**Previous**: [task-006-config-module.md](task-006-config-module.md)
**Next**: [task-008-create-exports-configure-ruff.md](task-008-create-exports-configure-ruff.md)

---

## Document Metadata

- **Task ID**: 007
- **Phase**: 02 - Core Interfaces & Utilities
- **LOC Output**: ~600 lines
- **Complexity**: High
- **Prerequisites**: Tasks 001-006 complete
- **Validates**: TDD process, logging functionality, test coverage
