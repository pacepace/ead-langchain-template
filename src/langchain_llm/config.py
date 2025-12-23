"""
Configuration management for EAD LangChain Template.

Handles loading environment variables with the EADLANGCHAIN_ prefix
and provides convenient access to API keys and other configuration.
"""

import os
from pathlib import Path

from dotenv import load_dotenv


class ConfigError(Exception):
    """Raised when there is configuration error."""

    pass


class EnvConfigProvider:
    """
    Configuration provider that reads from environment variables.

    Default implementation of ConfigProvider protocol.
    Reads configuration from environment variables, which can be
    set directly in shell or loaded from .env file.

    All environment variables use EADLANGCHAIN_ prefix to avoid
    conflicts with other tools and system variables.

    Example usage::

        config = EnvConfigProvider()
        api_key = config.get_key("openai")
        all_keys = config.get_all_keys()
    """

    # Provider name to environment variable mapping
    PROVIDER_MAP = {
        "openai": "EADLANGCHAIN_AI_OPENAI_API_KEY",
        "anthropic": "EADLANGCHAIN_AI_ANTHROPIC_API_KEY",
        "gemini": "EADLANGCHAIN_AI_GEMINI_API_KEY",
    }

    # Provider name to model environment variable mapping
    MODEL_MAP = {
        "openai": "EADLANGCHAIN_AI_OPENAI_MODEL",
        "anthropic": "EADLANGCHAIN_AI_ANTHROPIC_MODEL",
        "gemini": "EADLANGCHAIN_AI_GEMINI_MODEL",
    }

    def get_key(self, provider: str, required: bool = True) -> str | None:
        """
        Get API key for specific provider.

        :param provider: Provider name ('openai', 'anthropic', or 'gemini')
        :ptype provider: str
        :param required: If True, raises ConfigError if key is missing
        :ptype required: bool
        :return: API key string, or None if not found and not required
        :rtype: str | None
        :raises ConfigError: If required=True and API key is not found
        :raises ValueError: If provider is not recognized

        Example::

            >>> config = EnvConfigProvider()
            >>> key = config.get_key("openai")
            >>> print(f"Key starts with: {key[:7]}")
            Key starts with: sk-proj
        """
        provider = provider.lower()

        if provider not in self.PROVIDER_MAP:
            valid_providers = sorted(self.PROVIDER_MAP.keys())
            raise ValueError(f"Unknown provider: {provider}. " f"Supported providers: {', '.join(valid_providers)}")

        env_var = self.PROVIDER_MAP[provider]
        api_key = os.getenv(env_var)

        if required and not api_key:
            raise ConfigError(
                f"API key not found for provider '{provider}'. "
                f"Please set {env_var} in your .env file or environment variables. "
                f"See .env.example for template."
            )

        return api_key

    def get_all_keys(self) -> dict[str, str | None]:
        """
        Get all configured API keys.

        :return: Dictionary mapping provider names to API keys (or None if not set)
        :rtype: dict[str, str | None]

        Example::

            >>> config = EnvConfigProvider()
            >>> keys = config.get_all_keys()
            >>> configured = [k for k, v in keys.items() if v]
            >>> print(f"Configured providers: {configured}")
            Configured providers: ['openai', 'gemini']
        """
        return {
            "openai": os.getenv("EADLANGCHAIN_AI_OPENAI_API_KEY"),
            "anthropic": os.getenv("EADLANGCHAIN_AI_ANTHROPIC_API_KEY"),
            "gemini": os.getenv("EADLANGCHAIN_AI_GEMINI_API_KEY"),
        }

    def validate(self, provider: str) -> None:
        """
        Validate that provider is configured with API key.

        :param provider: Provider name to validate
        :ptype provider: str
        :return: None
        :rtype: None
        :raises ConfigError: If provider is not configured

        Example::

            >>> config = EnvConfigProvider()
            >>> config.validate("openai")  # Raises ConfigError if not configured
        """
        self.get_key(provider, required=True)

    def get_model_name(self, provider: str) -> str | None:
        """
        Get default model name for provider from environment variables.

        :param provider: Provider name ('openai', 'anthropic', or 'gemini')
        :ptype provider: str
        :return: Model name string, or None if not configured
        :rtype: str | None

        Example::

            >>> config = EnvConfigProvider()
            >>> model = config.get_model_name("openai")
            >>> print(f"Default OpenAI model: {model or 'gpt-4o-mini'}")
            Default OpenAI model: gpt-4o
        """
        provider = provider.lower()

        if provider not in self.MODEL_MAP:
            return None

        return os.getenv(self.MODEL_MAP[provider])


def load_env_config(env_file: str | None = None) -> None:
    """
    Load environment variables from .env file.

    :param env_file: Path to .env file. If None, looks for .env in current directory
                     and parent directories up to project root.
    :ptype env_file: str | None
    :return: None
    :rtype: None

    Example::

        >>> from langchain_llm import load_env_config
        >>> load_env_config()  # Loads from .env in project root
    """
    if env_file:
        load_dotenv(env_file)
    else:
        # Try to find .env file in current directory or parent directories
        current = Path.cwd()
        for parent in [current] + list(current.parents):
            env_path = parent / ".env"
            if env_path.exists():
                load_dotenv(env_path)
                return

        # If no .env file found, still try to load (will use system env vars)
        load_dotenv()


# Module-level singleton instance for convenience API
_default_config = EnvConfigProvider()


def get_api_key(provider: str, required: bool = True) -> str | None:
    """
    Get API key for specific provider.

    Convenience function that uses default
    EnvConfigProvider instance. For more control, create
    your own ConfigProvider instance.

    :param provider: Provider name ('openai', 'anthropic', or 'gemini')
    :ptype provider: str
    :param required: If True, raises ConfigError if key is missing
    :ptype required: bool
    :return: API key string, or None if not found and not required
    :rtype: str | None
    :raises ConfigError: If required=True and API key is not found
    :raises ValueError: If provider is not recognized

    Example::

        >>> from langchain_llm import get_api_key
        >>> openai_key = get_api_key("openai")
        >>> # Use with LangChain
        >>> from langchain_openai import ChatOpenAI
        >>> llm = ChatOpenAI(api_key=openai_key)
    """
    return _default_config.get_key(provider, required)


def get_all_api_keys() -> dict[str, str | None]:
    """
    Get all configured API keys.

    :return: Dictionary mapping provider names to API keys (or None if not set)
    :rtype: dict[str, str | None]

    Example::

        >>> from langchain_llm import get_all_api_keys
        >>> keys = get_all_api_keys()
        >>> print(f"Configured providers: {[k for k, v in keys.items() if v]}")
    """
    return _default_config.get_all_keys()


def validate_provider(provider: str) -> None:
    """
    Validate that provider is configured with API key.

    :param provider: Provider name to validate
    :ptype provider: str
    :return: None
    :rtype: None
    :raises ConfigError: If provider is not configured

    Example::

        >>> from langchain_llm import validate_provider
        >>> validate_provider("openai")  # Raises ConfigError if not configured
    """
    _default_config.validate(provider)


def get_model_name(provider: str) -> str | None:
    """
    Get default model name for provider from environment variables.

    Convenience function that uses default
    EnvConfigProvider instance.

    :param provider: Provider name ('openai', 'anthropic', or 'gemini')
    :ptype provider: str
    :return: Model name string, or None if not configured
    :rtype: str | None

    Example::

        >>> from langchain_llm import get_model_name
        >>> model = get_model_name("openai")
        >>> print(f"Default OpenAI model: {model or 'gpt-4o'}")
    """
    return _default_config.get_model_name(provider)
