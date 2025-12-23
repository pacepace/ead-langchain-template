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


class CustomFormatter(logging.Formatter, LogFormatter):
    """
    Custom formatter that adds relative_path and metaclass_name to log records.

    Formatter enriches log records with:
    - relative_path: Path relative to project root
    - metaclass_name: Class name if log is called from within class method

    Dual Inheritance Explanation:
    This class inherits from both logging.Formatter (Python's built-in) and
    LogFormatter (our custom ABC). This is intentional:
    - logging.Formatter provides base formatting functionality we extend
    - LogFormatter is our ABC interface contract for all custom formatters

    This pattern enables us to build on Python's logging while maintaining our own
    abstraction for future formatter implementations (e.g., JSONFormatter, CloudFormatter).
    """

    def __init__(self, fmt: str | None = None, datefmt: str | None = None, project_root: Path | None = None):
        """
        Initialize custom formatter.

        :param fmt: Log format string (uses default if None)
        :ptype fmt: str | None
        :param datefmt: Date format string (uses default if None)
        :ptype datefmt: str | None
        :param project_root: Project root directory (auto-detected if None)
        :ptype project_root: Path | None
        """
        super().__init__(fmt, datefmt)
        self.project_root = project_root or self._find_project_root()

    @staticmethod
    def _find_project_root() -> Path:
        """
        Find project root by looking for pyproject.toml or .git directory.
        Falls back to current working directory if not found.

        :return: Path to project root directory
        :rtype: Path
        """
        current = Path.cwd()
        for parent in [current] + list(current.parents):
            if (parent / "pyproject.toml").exists() or (parent / ".git").exists():
                return parent
        return current

    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record with custom attributes.

        Adds:
        - relative_path: Path relative to project root
        - metaclass_name: Class name or empty string if not in class

        :param record: Log record to format
        :ptype record: logging.LogRecord
        :return: Formatted log string
        :rtype: str
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
        # This is a best-effort approach - it looks for 'self' or 'cls' in the caller's locals
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


def setup_logging(
    level: str | None = None,
    log_file: str | None = None,
    format_string: str | None = None,
) -> logging.Logger:
    """
    Set up logging with custom formatter.

    :param level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
                  Defaults to EADLANGCHAIN_LOG_LEVEL env var or INFO.
    :ptype level: str | None
    :param log_file: Optional file path to write logs to.
                     Defaults to EADLANGCHAIN_LOG_FILE env var.
    :ptype log_file: str | None
    :param format_string: Custom format string. Uses standard format if not provided.
    :ptype format_string: str | None
    :return: Configured root logger
    :rtype: logging.Logger

    Example::

        >>> from langchain_llm import setup_logging
        >>> logger = setup_logging(level="DEBUG")
        >>> logger.info("Application started")
    """
    # Get log level from env var if not provided
    if level is None:
        level = os.getenv("EADLANGCHAIN_LOG_LEVEL", "INFO")

    # Get log file from env var if not provided
    if log_file is None:
        log_file = os.getenv("EADLANGCHAIN_LOG_FILE")

    # Default format string
    if format_string is None:
        format_string = "%(levelname)-8s %(asctime)s %(relative_path)s.%(metaclass_name)s%(funcName)s.%(lineno)d: %(message)s"

    # Configure formatter
    formatter = CustomFormatter(fmt=format_string, datefmt="%Y-%m-%d %H:%M:%S")

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))

    # Remove existing handlers
    root_logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler (optional)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Get logger with specified name.

    :param name: Logger name (typically __name__)
    :ptype name: str
    :return: Logger instance
    :rtype: logging.Logger

    Example::

        >>> from langchain_llm import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info("Processing data")
    """
    return logging.getLogger(name)
