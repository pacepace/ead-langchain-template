"""
Tests for the config module.

This demonstrates Test-Driven Development (TDD) patterns:
1. Write tests first
2. Run tests and see them fail
3. Write minimal code to make tests pass
4. Refactor as needed

Run these tests with: pytest tests/unit/test_config.py -v
"""

import os

import pytest

from langchain_llm.config import ConfigError, get_all_api_keys, get_api_key, get_model_name, load_env_config, validate_provider


class TestLoadEnvConfig:
    """Tests for load_env_config function."""

    def test_load_env_config_with_file(self, temp_env_file, clean_env):
        """
        Test loading config from specific .env file.

        :param temp_env_file: Pytest fixture providing temporary .env file
        :ptype temp_env_file: Path
        :param clean_env: Pytest fixture for clean environment
        :ptype clean_env: None
        """
        load_env_config(str(temp_env_file))
        assert os.getenv("EADLANGCHAIN_AI_OPENAI_API_KEY") == "test-key-openai"
        assert os.getenv("EADLANGCHAIN_LOG_LEVEL") == "DEBUG"

    def test_load_env_config_without_file(self, mock_env_vars):
        """
        Test loading config when env vars already exist.

        :param mock_env_vars: Pytest fixture providing mocked environment variables
        :ptype mock_env_vars: dict
        """
        load_env_config()
        # Should still have access to mocked env vars
        assert os.getenv("EADLANGCHAIN_AI_OPENAI_API_KEY") is not None

    def test_load_env_config_no_env_file_found(self, tmp_path, monkeypatch, clean_env):
        """
        Test loading config when no .env file exists in tree.
        Should not crash, just use system environment variables.

        :param tmp_path: Pytest fixture providing temporary directory
        :ptype tmp_path: Path
        :param monkeypatch: Pytest fixture for modifying environment
        :ptype monkeypatch: pytest.MonkeyPatch
        :param clean_env: Pytest fixture for clean environment
        :ptype clean_env: None
        """
        # Change to temp directory with no .env file
        monkeypatch.chdir(tmp_path)
        # Should not raise an exception - just falls back to system env vars
        load_env_config()
        # No assertions needed - test passes if no exception raised


class TestGetApiKey:
    """Tests for get_api_key function."""

    def test_get_openai_key(self, mock_env_vars):
        """
        Test retrieving OpenAI API key.

        :param mock_env_vars: Pytest fixture providing mocked environment variables
        :ptype mock_env_vars: dict
        """
        key = get_api_key("openai")
        assert key == "test-key-openai"

    def test_get_anthropic_key(self, mock_env_vars):
        """
        Test retrieving Anthropic API key.

        :param mock_env_vars: Pytest fixture providing mocked environment variables
        :ptype mock_env_vars: dict
        """
        key = get_api_key("anthropic")
        assert key == "test-key-anthropic"

    def test_get_gemini_key(self, mock_env_vars):
        """
        Test retrieving Gemini API key.

        :param mock_env_vars: Pytest fixture providing mocked environment variables
        :ptype mock_env_vars: dict
        """
        key = get_api_key("gemini")
        assert key == "test-key-gemini"

    def test_missing_key_required(self, clean_env):
        """
        Test that missing required key raises ConfigError.

        :param clean_env: Pytest fixture for clean environment
        :ptype clean_env: None
        """
        with pytest.raises(ConfigError) as exc_info:
            get_api_key("openai", required=True)
        assert "API key not found" in str(exc_info.value)
        assert "EADLANGCHAIN_AI_OPENAI_API_KEY" in str(exc_info.value)

    def test_missing_key_optional(self, clean_env):
        """
        Test that missing optional key returns None.

        :param clean_env: Pytest fixture for clean environment
        :ptype clean_env: None
        """
        key = get_api_key("openai", required=False)
        assert key is None

    def test_invalid_provider(self, mock_env_vars):
        """
        Test that invalid provider raises ValueError.

        :param mock_env_vars: Pytest fixture providing mocked environment variables
        :ptype mock_env_vars: dict
        """
        with pytest.raises(ValueError) as exc_info:
            get_api_key("invalid_provider")
        assert "Unknown provider" in str(exc_info.value)

    def test_case_insensitive_provider(self, mock_env_vars):
        """
        Test that provider names are case-insensitive.

        :param mock_env_vars: Pytest fixture providing mocked environment variables
        :ptype mock_env_vars: dict
        """
        key1 = get_api_key("OpenAI")
        key2 = get_api_key("OPENAI")
        key3 = get_api_key("openai")
        assert key1 == key2 == key3


class TestGetAllApiKeys:
    """Tests for get_all_api_keys function."""

    def test_get_all_keys_when_set(self, mock_env_vars):
        """
        Test getting all API keys when they are set.

        :param mock_env_vars: Pytest fixture providing mocked environment variables
        :ptype mock_env_vars: dict
        """
        keys = get_all_api_keys()
        assert keys["openai"] == "test-key-openai"
        assert keys["anthropic"] == "test-key-anthropic"
        assert keys["gemini"] == "test-key-gemini"
        assert len(keys) == 3

    def test_get_all_keys_when_missing(self, clean_env):
        """
        Test getting all API keys when none are set.

        :param clean_env: Pytest fixture for clean environment
        :ptype clean_env: None
        """
        keys = get_all_api_keys()
        assert keys["openai"] is None
        assert keys["anthropic"] is None
        assert keys["gemini"] is None


class TestValidateProvider:
    """Tests for validate_provider function."""

    def test_validate_configured_provider(self, mock_env_vars):
        """
        Test validating properly configured provider.

        :param mock_env_vars: Pytest fixture providing mocked environment variables
        :ptype mock_env_vars: dict
        """
        # Should not raise an exception
        validate_provider("openai")
        validate_provider("anthropic")
        validate_provider("gemini")

    def test_validate_unconfigured_provider(self, clean_env):
        """
        Test validating an unconfigured provider raises error.

        :param clean_env: Pytest fixture for clean environment
        :ptype clean_env: None
        """
        with pytest.raises(ConfigError):
            validate_provider("openai")


class TestGetModelName:
    """Tests for get_model_name function."""

    def test_get_model_name_when_set(self, monkeypatch):
        """
        Test getting model name when environment variable is set.

        :param monkeypatch: Pytest fixture for modifying environment
        :ptype monkeypatch: pytest.MonkeyPatch
        """
        monkeypatch.setenv("EADLANGCHAIN_AI_OPENAI_MODEL", "gpt-4o")
        model = get_model_name("openai")
        assert model == "gpt-4o"

    def test_get_model_name_when_not_set(self, clean_env):
        """
        Test getting model name when not configured.

        :param clean_env: Pytest fixture for clean environment
        :ptype clean_env: None
        """
        model = get_model_name("openai")
        assert model is None

    def test_get_model_name_invalid_provider(self, clean_env):
        """
        Test getting model name for invalid provider.

        :param clean_env: Pytest fixture for clean environment
        :ptype clean_env: None
        """
        model = get_model_name("invalid_provider")
        assert model is None


# Example of a TDD workflow:
# 1. Write this test first (it will fail)
# 2. Run: pytest tests/test_config.py::TestConfigIntegration::test_full_workflow -v
# 3. Implement the feature
# 4. Run the test again (it should pass)
class TestConfigIntegration:
    """Integration tests for config module."""

    def test_full_workflow(self, temp_env_file, clean_env):
        """
        Test full workflow of loading config and using it.
        Integration test that tests multiple functions together.

        :param temp_env_file: Pytest fixture providing temporary .env file
        :ptype temp_env_file: Path
        :param clean_env: Pytest fixture for clean environment
        :ptype clean_env: None
        """
        # Step 1: Load config from file
        load_env_config(str(temp_env_file))

        # Step 2: Validate providers are configured
        validate_provider("openai")
        validate_provider("anthropic")

        # Step 3: Get specific keys
        openai_key = get_api_key("openai")
        assert openai_key == "test-key-openai"

        # Step 4: Get all keys
        all_keys = get_all_api_keys()
        assert len(all_keys) == 3
        assert all([v is not None for v in all_keys.values()])
