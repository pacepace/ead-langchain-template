"""
Pytest configuration and shared fixtures.

This file contains pytest configuration and fixtures that can be used
across all test files. Fixtures help reduce code duplication in tests.
"""

import logging
import os
from collections.abc import Callable
from io import StringIO
from pathlib import Path

import pytest
from _pytest.monkeypatch import MonkeyPatch


@pytest.fixture
def mock_env_vars(monkeypatch: MonkeyPatch) -> None:
    """
    Fixture that provides mock environment variables for testing.

    Uses pytest's monkeypatch for consistent isolation across all fixtures.

    :param monkeypatch: Pytest fixture for modifying environment
    :ptype monkeypatch: MonkeyPatch
    :return: None
    :rtype: None

    Usage:
        def test_something(mock_env_vars):
            # Environment variables are already set
            assert os.getenv("EADLANGCHAIN_AI_OPENAI_API_KEY") == "test-key-openai"
    """
    monkeypatch.setenv("EADLANGCHAIN_AI_OPENAI_API_KEY", "test-key-openai")
    monkeypatch.setenv("EADLANGCHAIN_AI_ANTHROPIC_API_KEY", "test-key-anthropic")
    monkeypatch.setenv("EADLANGCHAIN_AI_GEMINI_API_KEY", "test-key-gemini")
    monkeypatch.setenv("EADLANGCHAIN_LOG_LEVEL", "INFO")
    yield


@pytest.fixture
def clean_env() -> None:
    """
    Fixture that provides clean environment (removes EADLANGCHAIN_ vars).

    :return: None
    :rtype: None

    Usage:
        def test_missing_key(clean_env):
            # All EADLANGCHAIN_ vars are removed
            from langchain_llm import get_api_key
            with pytest.raises(ConfigError):
                get_api_key("openai")
    """
    # Save original environment
    original_env = os.environ.copy()

    # Remove all EADLANGCHAIN_ vars
    for key in list(os.environ.keys()):
        if key.startswith("EADLANGCHAIN_"):
            del os.environ[key]

    yield

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def temp_env_file(tmp_path: Path) -> Path:
    """
    Fixture that creates temporary .env file for testing.

    :param tmp_path: Pytest fixture providing temporary directory
    :ptype tmp_path: Path
    :return: Path to temporary .env file
    :rtype: Path

    Usage:
        def test_env_loading(temp_env_file):
            # temp_env_file is Path object pointing to .env file
            from langchain_llm import load_env_config
            load_env_config(str(temp_env_file))
    """
    env_content = """
# Test environment file
EADLANGCHAIN_AI_OPENAI_API_KEY=test-key-openai
EADLANGCHAIN_AI_ANTHROPIC_API_KEY=test-key-anthropic
EADLANGCHAIN_AI_GEMINI_API_KEY=test-key-gemini
EADLANGCHAIN_LOG_LEVEL=DEBUG
"""
    env_file = tmp_path / ".env"
    env_file.write_text(env_content)
    return env_file


@pytest.fixture
def mock_llm_response() -> Callable[[str | None], "MockResponse"]:
    """
    Fixture that provides mock LLM response for testing without API calls.

    :return: Function to create mock responses
    :rtype: Callable[[str | None], MockResponse]

    Usage:
        def test_llm_interaction(mock_llm_response):
            # Use mock_llm_response instead of real LLM
            response = mock_llm_response("test prompt")
            assert "content" in response
    """

    class MockResponse:
        """
        Mock LLM response object for testing.

        :param content: Response content text
        :ptype content: str
        :param metadata: Optional response metadata
        :ptype metadata: dict | None
        """

        def __init__(self, content: str = "Mock response content", metadata: dict | None = None):
            """
            Initialize mock response object.

            :param content: Response content text
            :ptype content: str
            :param metadata: Optional response metadata
            :ptype metadata: dict | None
            :return: None
            :rtype: None
            """
            self.content = content
            self.response_metadata = metadata or {"model": "mock-model", "usage": {"total_tokens": 10}}

    def create_response(prompt: str | None = None) -> MockResponse:
        """
        Create mock LLM response.

        :param prompt: Optional prompt text
        :ptype prompt: str | None
        :return: Mock response object
        :rtype: MockResponse
        """
        return MockResponse(content=f"Mock response to: {prompt}" if prompt else "Mock response")

    return create_response


@pytest.fixture(autouse=True)
def reset_logging():
    """
    Automatically reset logging configuration after each test.
    This prevents test pollution from logging setup.
    """
    import logging

    yield

    # Clear all handlers from root logger
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(logging.WARNING)


@pytest.fixture
def project_root() -> Path:
    """
    Fixture that provides project root directory.

    :return: Path to project root
    :rtype: Path

    Usage:
        def test_file_location(project_root):
            config_file = project_root / "pyproject.toml"
            assert config_file.exists()
    """
    # Go up from tests/ to project root
    return Path(__file__).parent.parent


@pytest.fixture
def temp_project_root(tmp_path: Path, monkeypatch: MonkeyPatch) -> Path:
    """
    Fixture that creates temporary project root with markers.

    Creates temporary directory, adds pyproject.toml marker file,
    and changes to that directory for duration of test.

    :param tmp_path: Pytest fixture providing temporary directory
    :ptype tmp_path: Path
    :param monkeypatch: Pytest fixture for modifying environment
    :ptype monkeypatch: MonkeyPatch
    :return: Path to temporary project root
    :rtype: Path

    Usage:
        def test_project_detection(temp_project_root):
            # Current directory is now temp_project_root
            # pyproject.toml exists in this directory
            assert (Path.cwd() / "pyproject.toml").exists()
    """
    # Create pyproject.toml marker
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text('[tool.poetry]\nname = "test-project"\n')

    # Change to temp directory
    monkeypatch.chdir(tmp_path)

    return tmp_path


@pytest.fixture
def capture_logs() -> StringIO:
    """
    Fixture that captures log output for testing.

    Creates StringIO stream and adds it as handler to root logger.
    Automatically cleans up after test completes.

    :return: String stream containing captured log output
    :rtype: StringIO

    Usage:
        def test_logging_output(capture_logs):
            from langchain_llm import setup_logging, get_logger
            setup_logging(level="INFO")
            logger = get_logger(__name__)
            logger.info("Test message")

            output = capture_logs.getvalue()
            assert "Test message" in output
    """
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
