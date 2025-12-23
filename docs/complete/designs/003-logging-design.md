# Design 003: Logging System Design

## Document Purpose

This document specifies the complete design for the logging system in the EAD LangChain Template, including the LogFormatter ABC, custom formatting, and logging utilities.

---

## Overview

### Responsibilities

The logging module handles:
1. **Logging Setup**: Configure Python's logging system
2. **Custom Formatting**: Enhanced log format with project context
3. **Logger Creation**: Factory for module-specific loggers
4. **Formatter Interface**: ABC for swappable formatting strategies

### Design Philosophy

- **Extend, Don't Replace**: Build on Python's logging module
- **Project Context**: Add relative paths, class names, detailed location
- **Configurable**: Control via environment variables
- **Interface-Driven**: ABC allows multiple formatting strategies
- **Evidence-Based Troubleshooting**: Format optimized for debugging workflow
  - Every log entry maps to exact source code location (file.function.line)
  - Relative paths enable navigation across different environments
  - Supports both human developers and AI assistants in locating issues
  - Timestamps create execution timeline for understanding code flow
  - See `requirements/001-functional-requirements.md` FR-002.4 for complete rationale
  - See `.github/copilot-instructions.md` "Evidence-Based Troubleshooting" for workflow

---

## LogFormatter ABC (Interface)

### Abstract Base Class Definition

**File**: `src/langchain_llm/interfaces.py`

```python
from abc import ABC, abstractmethod
import logging


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

        Example::

            class MyFormatter(LogFormatter):
                def format(self, record: logging.LogRecord) -> str:
                    # Add custom attributes
                    record.custom_field = "value"

                    # Call parent formatter
                    return super().format(record)
        """
        pass
```

### Why ABC (Not Protocol)?

**Nominal Subtyping**:
- `logging.Formatter` is already a class in Python's standard library
- Formatters need to inherit to override behavior
- ABC provides clear inheritance chain
- Can use `@abstractmethod` decorator

**Example**:
```python
class MyLogFormatter(LogFormatter, logging.Formatter):
    """Custom log formatter."""

    def __init__(self, fmt: str):
        logging.Formatter.__init__(self, fmt)
        # ABC doesn't require __init__, but Formatter does

    def format(self, record: logging.LogRecord) -> str:
        # Implement required abstract method
        record.custom_attr = "value"
        return super().format(record)
```

**Benefits**:
- Clear that this inherits from logging.Formatter
- Can enforce required methods with @abstractmethod
- IDE autocomplete works well with ABCs
- Pythonic for class-based interfaces

---

## CustomFormatter Implementation

### Class Design

**File**: `src/langchain_llm/logging_config.py`

```python
import logging
import os
from pathlib import Path

from langchain_llm.interfaces import LogFormatter  # Import ABC


class CustomFormatter(LogFormatter, logging.Formatter):
    """
    Custom formatter that adds relative_path and metaclass_name to log records.

    This formatter enriches log records with:
    - relative_path: Path relative to the project root (dot notation)
    - metaclass_name: Class name if logging from within a class method
    - Enhanced timestamp and location information

    The result is detailed, informative logs that help with debugging
    while being readable and consistent.

    Format example::

        INFO     2025-01-15 10:30:45 examples.01_basic.basic_openai_example.27: Running OpenAI example

    Breakdown:
    - INFO: Log level (8 chars, left-aligned)
    - 2025-01-15 10:30:45: Timestamp
    - examples.01_basic: Relative path (dot notation)
    - basic_openai_example: Function name
    - 27: Line number
    - Running OpenAI example: Log message
    """

    def __init__(
        self,
        fmt: str | None = None,
        datefmt: str | None = None,
        project_root: Path | None = None,
    ):
        """
        Initialize CustomFormatter.

        :param fmt: Format string (uses default if None)
        :ptype fmt: str | None
        :param datefmt: Date format string
        :ptype datefmt: str | None
        :param project_root: Project root directory (auto-detected if None)
        :ptype project_root: Path | None
        """
        super().__init__(fmt, datefmt)
        self.project_root = project_root or self._find_project_root()

    @staticmethod
    def _find_project_root() -> Path:
        """
        Find the project root by looking for pyproject.toml or .git directory.

        Searches upward from current working directory until it finds
        a marker file/directory that indicates project root.

        :return: Path to the project root directory
        :rtype: Path

        Example::

            Current: /path/to/project/examples/
            Searches:
              1. /path/to/project/examples/ (no marker)
              2. /path/to/project/ (has pyproject.toml) ← FOUND
            Returns: /path/to/project
        """
        current = Path.cwd()
        for parent in [current] + list(current.parents):
            if (parent / "pyproject.toml").exists() or (parent / ".git").exists():
                return parent
        # Fallback to current directory if no marker found
        return current

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record with custom attributes.

        Adds:
        - relative_path: Path relative to project root (dot notation)
        - metaclass_name: Class name (if logging from class method) or empty string

        :param record: The log record to format
        :ptype record: logging.LogRecord
        :return: Formatted log string
        :rtype: str

        Implementation details:
        - Converts file path to project-relative path
        - Uses dot notation (examples.01_basic instead of examples/01_basic.py)
        - Detects class name via frame inspection
        - Falls back gracefully if detection fails
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
            # Fallback to module name if relative path fails
            record.relative_path = record.module

        # Try to extract class name from the stack
        # This is best-effort - looks for 'self' or 'cls' in caller's locals
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
            # If frame inspection fails, just skip class name
            pass

        # Add class name with trailing dot if present
        record.metaclass_name = f"{metaclass_name}." if metaclass_name else ""

        # Call parent formatter with enriched record
        return super().format(record)
```

### Implementation Notes

**Relative Path Calculation**:
- Converts absolute file path to project-relative
- Uses dot notation (Python module style)
- Removes `.py` extension
- Fallback: Use `record.module` if relative path fails

**Class Name Detection**:
- Inspects stack frames for `self` or `cls`
- Best-effort (not always possible to detect)
- Graceful fallback (empty string if not found)
- Works for both instance methods and class methods

**Why Frame Inspection**:
- Python doesn't automatically include class context in LogRecords
- Need to inspect calling frame to find `self` or `cls`
- Alternative would be to require passing class name explicitly (less ergonomic)

---

## Logging Setup Functions

### setup_logging()

**Purpose**: Configure root logger with custom formatter

```python
def setup_logging(
    level: str | None = None,
    log_file: str | None = None,
    format_string: str | None = None,
) -> logging.Logger:
    """
    Set up logging with custom formatter.

    Configures the root logger with:
    - Custom formatter (enhanced with project context)
    - Console handler (always)
    - File handler (optional)
    - Specified log level (from param or env var)

    This function is idempotent - calling it multiple times
    reconfigures logging (clears existing handlers first).

    :param level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
                  Defaults to EADLANGCHAIN_LOG_LEVEL env var or INFO.
    :ptype level: str | None
    :param log_file: Optional file path to write logs to.
                     Defaults to EADLANGCHAIN_LOG_FILE env var.
    :ptype log_file: str | None
    :param format_string: Custom format string. Uses standard format if not provided.
    :ptype format_string: str | None
    :return: Configured root logger.
    :rtype: logging.Logger

    Example usage::

        >>> from langchain_llm import setup_logging
        >>> logger = setup_logging(level="DEBUG")
        >>> logger.info("Application started")
        INFO     2025-01-15 10:30:45 mymodule.main.15: Application started

        >>> # With file output
        >>> setup_logging(level="INFO", log_file="logs/app.log")

        >>> # From environment variables
        >>> # EADLANGCHAIN_LOG_LEVEL=DEBUG
        >>> # EADLANGCHAIN_LOG_FILE=logs/app.log
        >>> setup_logging()  # Uses env vars
    """
    # Get log level from env var if not provided
    if level is None:
        level = os.getenv("EADLANGCHAIN_LOG_LEVEL", "INFO")

    # Get log file from env var if not provided
    if log_file is None:
        log_file = os.getenv("EADLANGCHAIN_LOG_FILE")

    # Default format string
    if format_string is None:
        format_string = (
            "%(levelname)-8s %(asctime)s "
            "%(relative_path)s.%(metaclass_name)s%(funcName)s.%(lineno)d: "
            "%(message)s"
        )

    # Configure formatter
    formatter = CustomFormatter(
        fmt=format_string,
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))

    # Remove existing handlers (make this function idempotent)
    root_logger.handlers.clear()

    # Console handler (always added)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler (optional)
    if log_file:
        # Create directory if it doesn't exist
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        # Add file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    return root_logger
```

**Design Decisions**:
- **Environment Variable Priority**: Check env vars if params not provided
- **Idempotent**: Clears existing handlers first
- **Creates Directories**: log_file parent directory auto-created
- **Always Console**: Console output always enabled
- **Optional File**: File output only if requested
- **Returns Logger**: For convenience (though root logger is global)

### get_logger()

**Purpose**: Factory for module-specific loggers

```python
def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.

    This is a thin wrapper around logging.getLogger() that
    makes the API consistent with the rest of the module.
    The returned logger inherits configuration from the
    root logger set up by setup_logging().

    :param name: Logger name (typically __name__)
    :ptype name: str
    :return: Logger instance.
    :rtype: logging.Logger

    Example usage::

        >>> from langchain_llm import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info("Processing data")
        INFO     2025-01-15 10:30:45 myapp.processor.process_data.42: Processing data

    Best practice::

        # At module level
        from langchain_llm import get_logger
        logger = get_logger(__name__)

        # Throughout module
        def my_function():
            logger.info("In my_function")
            logger.debug("Debug details")
    """
    return logging.getLogger(name)
```

**Design**: Simple delegation to `logging.getLogger()`

**Why Wrapper**:
- Consistent API (`from langchain_llm import get_logger`)
- Could add functionality later (custom logger class)
- Matches style of `setup_logging()`, `get_api_key()`, etc.

---

## Log Format Specification

### Default Format String

```python
format_string = (
    "%(levelname)-8s "              # Log level, 8 chars, left-aligned
    "%(asctime)s "                   # Timestamp
    "%(relative_path)s."             # Project-relative path (dot notation)
    "%(metaclass_name)s"             # Class name (with dot) or empty
    "%(funcName)s."                  # Function name
    "%(lineno)d: "                   # Line number
    "%(message)s"                    # Log message
)
```

### Format Breakdown

**%(levelname)-8s**:
- `-8s`: Left-aligned, 8 characters
- Examples: `DEBUG   `, `INFO    `, `WARNING `, `ERROR   `, `CRITICAL`
- Visual alignment in console

**%(asctime)s**:
- Format: `%Y-%m-%d %H:%M:%S`
- Example: `2025-01-15 10:30:45`
- Human-readable timestamp

**%(relative_path)s**:
- Custom attribute added by CustomFormatter
- Project-relative path in dot notation
- Examples: `examples.01_basic`, `src.langchain_llm.config`
- Removed `.py` extension

**%(metaclass_name)s**:
- Custom attribute added by CustomFormatter
- Class name with trailing dot, or empty string
- Examples: `MyClass.`, `` (empty if not in class)
- Seamlessly integrated (dot only appears if class present)
- Note: `relative_path` already includes module name, so no separate `%(module)s` needed

**%(funcName)s**:
- Built-in LogRecord attribute
- Function or method name
- Examples: `get_api_key`, `basic_openai_example`

**%(lineno)d**:
- Built-in LogRecord attribute
- Line number where log call was made
- Example: `42`

**%(message)s**:
- The actual log message
- Example: `Running OpenAI example`

### Example Output

```
INFO     2025-01-15 10:30:45 examples.01_basic.basic_openai_example.27: Running OpenAI example
DEBUG    2025-01-15 10:30:46 src.langchain_llm.config.get_api_key.75: Retrieved API key for provider: openai
WARNING  2025-01-15 10:30:47 tests.test_config.TestConfig.test_missing_key.42: Testing error condition
ERROR    2025-01-15 10:30:48 examples.02_streaming.main.15: API call failed
```

**Anatomy** (using first example):
- `INFO    ` - Level (8 chars)
- `2025-01-15 10:30:45` - Timestamp
- `examples.01_basic` - Relative path
- `` - No class name (logging from function, not method)
- `basic_openai_example` - Function name
- `27` - Line number
- `Running OpenAI example` - Message

---

## Usage Patterns

### Pattern 1: Basic Setup (Most Common)

**Scenario**: Simple script with console logging

```python
from langchain_llm import setup_logging, get_logger

# Setup logging (call once at start)
setup_logging()

# Get module logger
logger = get_logger(__name__)

# Use throughout module
logger.info("Starting application")
logger.debug("Debug information")
logger.warning("Something to be aware of")
logger.error("An error occurred")
```

**Output**:
```
INFO     2025-01-15 10:30:45 myapp.main.8: Starting application
DEBUG    2025-01-15 10:30:45 myapp.main.9: Debug information
WARNING  2025-01-15 10:30:45 myapp.main.10: Something to be aware of
ERROR    2025-01-15 10:30:45 myapp.main.11: An error occurred
```

### Pattern 2: With File Output

**Scenario**: Write logs to file in addition to console

```python
from langchain_llm import setup_logging, get_logger

# Setup with file output
setup_logging(level="DEBUG", log_file="logs/app.log")

logger = get_logger(__name__)
logger.info("Logs go to console AND file")
```

**Result**:
- Console: Shows log message
- File (`logs/app.log`): Same message written to file
- Directory created if needed (`logs/` directory)

### Pattern 3: Environment Variable Configuration

**Scenario**: Control logging via environment variables

```bash
# .env file
EADLANGCHAIN_LOG_LEVEL=DEBUG
EADLANGCHAIN_LOG_FILE=logs/app.log
```

```python
from langchain_llm import setup_logging, get_logger

# Reads from environment variables
setup_logging()

logger = get_logger(__name__)
logger.debug("Debug level from env var")
```

### Pattern 4: Class-Based Logging

**Scenario**: Logging from within a class

```python
from langchain_llm import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)


class DataProcessor:
    def process(self, data):
        logger.info("Processing data")
        # ... processing logic
        logger.debug(f"Processed {len(data)} items")
```

**Output**:
```
INFO     2025-01-15 10:30:45 myapp.processor.DataProcessor.process.10: Processing data
DEBUG    2025-01-15 10:30:45 myapp.processor.DataProcessor.process.12: Processed 42 items
```

**Notice**: `DataProcessor.` automatically detected and included

### Pattern 5: Custom Format

**Scenario**: Different log format for specific needs

```python
from langchain_llm import setup_logging, get_logger

# Simple format
custom_format = "%(levelname)s - %(message)s"
setup_logging(format_string=custom_format)

logger = get_logger(__name__)
logger.info("Simple message")
```

**Output**:
```
INFO - Simple message
```

---

## Configuration via Environment Variables

### EADLANGCHAIN_LOG_LEVEL

**Purpose**: Set logging level

**Valid Values**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

**Default**: `INFO` if not set

**Case**: Insensitive (`debug`, `Debug`, `DEBUG` all work)

**Example**:
```bash
# .env
EADLANGCHAIN_LOG_LEVEL=DEBUG
```

**Effect**:
```python
setup_logging()  # Uses DEBUG level from environment
```

### EADLANGCHAIN_LOG_FILE

**Purpose**: Write logs to file in addition to console

**Valid Values**: Any file path

**Default**: None (console only)

**Example**:
```bash
# .env
EADLANGCHAIN_LOG_FILE=logs/app.log
```

**Effect**:
- Creates `logs/` directory if it doesn't exist
- Writes logs to `logs/app.log`
- Also continues writing to console

---

## Testing Strategy

### Unit Tests (TDD)

**File**: `tests/unit/test_logging.py`

**Test Categories**:

1. **Formatter Tests**:
   - `test_custom_formatter_relative_path()`
   - `test_custom_formatter_class_name_detection()`
   - `test_custom_formatter_without_class()`
   - `test_custom_formatter_project_root_detection()`

2. **Setup Tests**:
   - `test_setup_logging_default()`
   - `test_setup_logging_with_level()`
   - `test_setup_logging_with_file()`
   - `test_setup_logging_from_env_vars()`
   - `test_setup_logging_idempotent()`

3. **Logger Tests**:
   - `test_get_logger_returns_logger()`
   - `test_get_logger_inherits_config()`
   - `test_multiple_loggers()`

4. **Format Output Tests**:
   - `test_log_format_includes_timestamp()`
   - `test_log_format_includes_location()`
   - `test_log_format_includes_message()`

**Test Helpers**:
```python
import pytest
import logging
from io import StringIO


@pytest.fixture
def capture_logs():
    """Capture log output for testing."""
    stream = StringIO()
    handler = logging.StreamHandler(stream)
    logger = logging.getLogger()
    logger.addHandler(handler)
    yield stream
    logger.removeHandler(handler)


def test_log_output(capture_logs):
    """Test that log output matches expected format."""
    from langchain_llm import setup_logging, get_logger

    setup_logging(level="INFO")
    logger = get_logger(__name__)
    logger.info("Test message")

    output = capture_logs.getvalue()
    assert "INFO" in output
    assert "Test message" in output
    assert __name__ in output
```

### ABC Conformance Test

**Purpose**: Ensure CustomFormatter conforms to LogFormatter ABC

```python
def test_custom_formatter_conforms_to_abc():
    """Test that CustomFormatter implements LogFormatter ABC."""
    from langchain_llm.interfaces import LogFormatter
    from langchain_llm.logging_config import CustomFormatter

    formatter = CustomFormatter()

    # Check inheritance
    assert isinstance(formatter, LogFormatter)
    assert isinstance(formatter, logging.Formatter)

    # Check method exists
    assert hasattr(formatter, "format")
    assert callable(formatter.format)
```

---

## Future Enhancements

### JSON Formatter (Future)

**Scenario**: Structured logging for log aggregation systems

```python
import json
from langchain_llm.interfaces import LogFormatter


class JSONLogFormatter(LogFormatter, logging.Formatter):
    """Format logs as JSON for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record as JSON.

        :param record: Log record to format
        :ptype record: logging.LogRecord
        :return: JSON-formatted string
        :rtype: str
        """
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "message": record.getMessage(),
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)
```

**Usage**:
```python
# Use JSON formatter instead of CustomFormatter
formatter = JSONLogFormatter()
handler = logging.StreamHandler()
handler.setFormatter(formatter)
```

**Output**:
```json
{"timestamp": "2025-01-15 10:30:45", "level": "INFO", "logger": "myapp", "module": "main", "function": "process", "line": 42, "message": "Processing started"}
```

### Cloud Logging Formatter (Future)

**Scenario**: Integration with Google Cloud Logging, AWS CloudWatch

```python
class CloudLogFormatter(LogFormatter, logging.Formatter):
    """Format logs for cloud logging platforms."""

    def format(self, record: logging.LogRecord) -> str:
        """
        Format for cloud platforms.

        Includes:
        - Severity level (mapped to cloud platform levels)
        - Structured metadata
        - Trace IDs (if available)
        """
        severity = self._map_severity(record.levelname)
        # ... format for specific cloud platform
        return formatted_string

    def _map_severity(self, level: str) -> str:
        """Map Python log levels to cloud platform levels."""
        mapping = {
            "DEBUG": "DEBUG",
            "INFO": "INFO",
            "WARNING": "WARNING",
            "ERROR": "ERROR",
            "CRITICAL": "CRITICAL",
        }
        return mapping.get(level, "DEFAULT")
```

### Colored Console Output (Future)

**Scenario**: Color-coded logs for better readability

```python
class ColoredFormatter(LogFormatter, logging.Formatter):
    """Add ANSI colors to console output."""

    COLORS = {
        "DEBUG": "\033[36m",    # Cyan
        "INFO": "\033[32m",     # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",    # Red
        "CRITICAL": "\033[35m", # Magenta
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        """Format with ANSI colors."""
        colored_level = (
            f"{self.COLORS.get(record.levelname, '')}"
            f"{record.levelname}"
            f"{self.RESET}"
        )
        record.levelname = colored_level
        return super().format(record)
```

**Output** (in terminal):
```
[32mINFO[0m     2025-01-15 10:30:45 myapp.main.10: Processing
[31mERROR[0m    2025-01-15 10:30:46 myapp.main.15: Failed
```

---

## Performance Considerations

### Frame Inspection Overhead

**Cost**: ~0.01ms per log call (frame inspection)

**Mitigation**:
- Only inspect when formatting (not on every log statement)
- Caching not needed (overhead minimal)
- Skip gracefully if inspection fails

**Measurement**:
```python
import time

start = time.time()
for _ in range(10000):
    logger.info("Test message")
elapsed = time.time() - start
print(f"10000 logs: {elapsed:.2f}s")  # ~0.5s total = 0.05ms per log
```

### Relative Path Calculation

**Cost**: One path calculation per log call

**Mitigation**:
- Project root cached in CustomFormatter instance
- Path.relative_to() is fast (C implementation)
- Only calculate when actually logging (level check happens first)

---

## Related Documents

- **Previous**: [002-configuration-design.md](002-configuration-design.md) - Config module
- **Next**: [004-examples-design.md](004-examples-design.md) - Examples design
- **See Also**:
  - [000-architecture-overview.md](000-architecture-overview.md) - Architecture
  - [requirements/004-quality-requirements.md](../requirements/004-quality-requirements.md) - Quality standards

## Document Metadata

- **Version**: 1.0
- **Status**: Active
- **Owner**: EAD LangChain Template Team
