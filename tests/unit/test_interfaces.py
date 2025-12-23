"""
Tests for the interfaces module.

Tests protocol and ABC conformance for the langchain_llm package interfaces.

Run these tests with: pytest tests/test_interfaces.py -v
"""

import logging

import pytest

from langchain_llm.config import EnvConfigProvider
from langchain_llm.interfaces import ConfigProvider, LogFormatter
from langchain_llm.logging_config import CustomFormatter


class TestConfigProviderProtocol:
    """Tests for ConfigProvider protocol conformance."""

    def test_env_config_provider_has_all_methods(self):
        """
        Test that EnvConfigProvider has all required protocol methods.

        :ptype: None
        """
        config = EnvConfigProvider()

        # Protocol conformance - structural subtyping
        assert hasattr(config, "get_key")
        assert hasattr(config, "get_all_keys")
        assert hasattr(config, "validate")
        assert hasattr(config, "get_model_name")

    def test_env_config_provider_methods_callable(self):
        """
        Test that all protocol methods are callable.

        :ptype: None
        """
        config = EnvConfigProvider()

        assert callable(config.get_key)
        assert callable(config.get_all_keys)
        assert callable(config.validate)
        assert callable(config.get_model_name)

    def test_env_config_provider_works_with_protocol_type(self, mock_env_vars):
        """
        Test that EnvConfigProvider works in protocol-typed functions.

        :param mock_env_vars: Pytest fixture providing mocked environment variables
        :ptype mock_env_vars: dict
        """

        def use_config_provider(provider: ConfigProvider) -> dict[str, str | None]:
            """
            Function that accepts ConfigProvider protocol.

            :param provider: Configuration provider
            :ptype provider: ConfigProvider
            :return: All API keys
            :rtype: dict[str, str | None]
            """
            return provider.get_all_keys()

        # Should work without type errors
        config = EnvConfigProvider()
        result = use_config_provider(config)

        # Verify it actually works
        assert isinstance(result, dict)
        assert "openai" in result
        assert "anthropic" in result
        assert "gemini" in result

    def test_protocol_get_key_signature(self, mock_env_vars):
        """
        Test that get_key has correct signature and behavior.

        :param mock_env_vars: Pytest fixture providing mocked environment variables
        :ptype mock_env_vars: dict
        """
        config = EnvConfigProvider()

        # Test with required=True (default)
        key = config.get_key("openai")
        assert key is not None
        assert isinstance(key, str)

        # Test with required=False
        key_optional = config.get_key("openai", required=False)
        assert key_optional is not None
        assert isinstance(key_optional, str)

    def test_protocol_get_all_keys_signature(self, mock_env_vars):
        """
        Test that get_all_keys returns dict[str, str | None].

        :param mock_env_vars: Pytest fixture providing mocked environment variables
        :ptype mock_env_vars: dict
        """
        config = EnvConfigProvider()
        result = config.get_all_keys()

        assert isinstance(result, dict)
        for key, value in result.items():
            assert isinstance(key, str)
            assert value is None or isinstance(value, str)

    def test_protocol_validate_signature(self, mock_env_vars):
        """
        Test that validate has correct signature.

        :param mock_env_vars: Pytest fixture providing mocked environment variables
        :ptype mock_env_vars: dict
        """
        config = EnvConfigProvider()

        # Should not raise with valid provider
        result = config.validate("openai")
        assert result is None  # Returns None on success

    def test_protocol_get_model_name_signature(self, clean_env):
        """
        Test that get_model_name returns str | None.

        :param clean_env: Pytest fixture for clean environment
        :ptype clean_env: None
        """
        config = EnvConfigProvider()
        result = config.get_model_name("openai")

        # Should return None when not configured
        assert result is None or isinstance(result, str)


class TestLogFormatterABC:
    """Tests for LogFormatter ABC conformance."""

    def test_custom_formatter_inherits_from_abc(self):
        """
        Test that CustomFormatter inherits from LogFormatter ABC.

        :ptype: None
        """
        formatter = CustomFormatter()

        # Check inheritance
        assert isinstance(formatter, LogFormatter)

    def test_custom_formatter_inherits_from_logging_formatter(self):
        """
        Test that CustomFormatter also inherits from logging.Formatter.

        :ptype: None
        """
        formatter = CustomFormatter()

        # Should also be a logging.Formatter
        assert isinstance(formatter, logging.Formatter)

    def test_format_method_exists_and_callable(self):
        """
        Test that format method is implemented and callable.

        :ptype: None
        """
        formatter = CustomFormatter()

        assert hasattr(formatter, "format")
        assert callable(formatter.format)

    def test_format_method_signature(self):
        """
        Test that format method accepts LogRecord and returns str.

        :ptype: None
        """
        formatter = CustomFormatter(fmt="%(message)s")

        # Create a test log record
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname=__file__,
            lineno=1,
            msg="Test message",
            args=(),
            exc_info=None,
        )

        # Call format
        result = formatter.format(record)

        # Should return string
        assert isinstance(result, str)
        assert "Test message" in result

    def test_abc_prevents_incomplete_implementation(self):
        """
        Test that LogFormatter ABC prevents incomplete implementations.

        :ptype: None
        """
        # This test verifies the ABC is working correctly
        # by attempting to create an incomplete implementation

        # Cannot instantiate ABC directly
        with pytest.raises(TypeError):
            LogFormatter()  # type: ignore

    def test_custom_formatter_can_be_used_as_log_formatter(self):
        """
        Test that CustomFormatter works in logging system.

        :ptype: None
        """
        formatter = CustomFormatter(fmt="%(levelname)s: %(message)s")

        # Create handler with our formatter
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        # Should work without errors
        assert handler.formatter is formatter
        assert isinstance(handler.formatter, LogFormatter)


class TestInterfacesIntegration:
    """Integration tests for interfaces working together."""

    def test_both_interfaces_can_be_imported(self):
        """
        Test that both protocol and ABC can be imported together.

        :ptype: None
        """
        from langchain_llm.interfaces import ConfigProvider, LogFormatter

        # Should not cause any import errors
        assert ConfigProvider is not None
        assert LogFormatter is not None

    def test_implementations_conform_to_their_interfaces(self, mock_env_vars):
        """
        Test that implementations properly conform to their interfaces.

        :param mock_env_vars: Pytest fixture providing mocked environment variables
        :ptype mock_env_vars: dict
        """
        # Config implementation
        config = EnvConfigProvider()
        assert hasattr(config, "get_key")

        # Formatter implementation
        formatter = CustomFormatter()
        assert isinstance(formatter, LogFormatter)

        # Both should work together
        api_key = config.get_key("openai")
        assert api_key is not None

        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname=__file__, lineno=1, msg="Test", args=(), exc_info=None
        )
        formatted = formatter.format(record)
        assert isinstance(formatted, str)
