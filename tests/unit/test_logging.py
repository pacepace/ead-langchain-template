"""
Tests for the logging_config module.

Demonstrates testing logging configuration and custom formatters.

Run these tests with: pytest tests/test_logging.py -v
"""

import logging
from pathlib import Path

from langchain_llm.logging_config import CustomFormatter, get_logger, setup_logging


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
        :ptype tmp_path: Path
        """
        formatter = CustomFormatter(project_root=tmp_path)
        assert formatter.project_root == tmp_path

    def test_find_project_root(self, project_root):
        """
        Test that _find_project_root locates project root.

        :param project_root: Pytest fixture providing project root path
        :ptype project_root: Path
        """
        formatter = CustomFormatter()
        # Should find project root with pyproject.toml
        assert (formatter.project_root / "pyproject.toml").exists() or (formatter.project_root / ".git").exists()

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

        logger = setup_logging(level="ERROR")
        assert logger.level == logging.ERROR

    def test_setup_logging_with_env_var(self, monkeypatch):
        """
        Test that setup_logging respects EADLANGCHAIN_LOG_LEVEL.

        :param monkeypatch: Pytest fixture for modifying environment
        :ptype monkeypatch: pytest.MonkeyPatch
        """
        monkeypatch.setenv("EADLANGCHAIN_LOG_LEVEL", "WARNING")
        logger = setup_logging()
        assert logger.level == logging.WARNING

    def test_setup_logging_with_file(self, tmp_path):
        """
        Test setting up logging with file output.

        :param tmp_path: Pytest fixture providing temporary directory
        :ptype tmp_path: Path
        """
        log_file = tmp_path / "test.log"

        logger = setup_logging(log_file=str(log_file))

        # Check that file handler was added
        file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
        assert len(file_handlers) > 0

        # Log something and check file
        logger.info("Test message")
        assert log_file.exists()
        assert "Test message" in log_file.read_text()

    def test_setup_logging_custom_format(self):
        """Test setting up logging with custom format."""
        custom_format = "%(levelname)s: %(message)s"
        logger = setup_logging(format_string=custom_format)

        # Get the formatter from console handler
        handler = logger.handlers[0]
        assert isinstance(handler.formatter, CustomFormatter)

    def test_setup_logging_clears_existing_handlers(self):
        """Test that setup_logging clears existing handlers."""
        # Set up logging twice
        logger1 = setup_logging()
        handler_count_1 = len(logger1.handlers)

        logger2 = setup_logging()
        handler_count_2 = len(logger2.handlers)

        # Should have same number of handlers (old ones cleared)
        assert handler_count_1 == handler_count_2


class TestGetLogger:
    """Tests for get_logger function."""

    def test_get_logger_returns_logger(self):
        """Test that get_logger returns logger instance."""
        logger = get_logger("test")
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test"

    def test_get_logger_with_name(self):
        """Test getting logger with __name__."""
        logger = get_logger(__name__)
        assert logger.name == __name__

    def test_multiple_get_logger_calls_return_same_instance(self):
        """Test that multiple calls return same logger instance."""
        logger1 = get_logger("test")
        logger2 = get_logger("test")
        assert logger1 is logger2


class TestLoggingIntegration:
    """Integration tests for logging functionality."""

    def test_full_logging_workflow(self, tmp_path):
        """
        Test complete logging workflow.

        :param tmp_path: Pytest fixture providing temporary directory
        :ptype tmp_path: Path
        """
        # Setup logging with file output
        log_file = tmp_path / "integration_test.log"
        setup_logging(level="INFO", log_file=str(log_file))

        # Get a logger
        logger = get_logger(__name__)

        # Log at different levels
        logger.debug("Debug message")  # Should not appear (level is INFO)
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")

        # Read log file
        log_content = log_file.read_text()

        # Check that appropriate messages appear
        assert "Info message" in log_content
        assert "Warning message" in log_content
        assert "Error message" in log_content
        assert "Debug message" not in log_content  # Below INFO level

    def test_logging_format_includes_all_fields(self, tmp_path, caplog):
        """
        Test that log format includes all required fields.

        :param tmp_path: Pytest fixture providing temporary directory
        :ptype tmp_path: Path
        :param caplog: Pytest fixture for capturing log output
        :ptype caplog: pytest.LogCaptureFixture
        """
        # Use a log file instead of caplog since setup_logging clears handlers
        log_file = tmp_path / "format_test.log"
        setup_logging(level="INFO", log_file=str(log_file))

        logger = get_logger(__name__)
        logger.info("Test message with all fields")

        # Read the log file and verify it contains expected format fields
        log_content = log_file.read_text()

        # Check that the formatted output includes our custom fields
        # Format: %(levelname)-8s %(asctime)s %(relative_path)s.%(metaclass_name)s%(funcName)s.%(lineno)d: %(message)s
        assert "INFO" in log_content
        assert "Test message with all fields" in log_content
        assert "test_logging" in log_content  # Should include relative_path with module name
        assert "test_logging_format_includes_all_fields" in log_content  # Should include function name

    def test_logging_with_class_method(self, tmp_path):
        """
        Test logging from within class method.

        :param tmp_path: Pytest fixture providing temporary directory
        :ptype tmp_path: Path
        """

        class TestClass:
            """Test class for logging from class methods."""

            def __init__(self):
                """
                Initialize test class instance.
                """
                self.logger = get_logger(__name__)

            def test_method(self):
                self.logger.info("Message from class method")

        # Setup logging
        log_file = tmp_path / "class_test.log"
        setup_logging(level="INFO", log_file=str(log_file))

        # Create instance and log
        test_instance = TestClass()
        test_instance.test_method()

        # Check log file
        log_content = log_file.read_text()
        assert "Message from class method" in log_content
