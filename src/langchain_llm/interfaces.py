"""
Interface definitions for langchain_llm package.

This module contains protocol and ABC definitions that establish
contracts for configuration providers, log formatters, and other
extensibility points in the package.
"""

import logging
from abc import ABC, abstractmethod
from typing import Protocol


class ConfigProvider(Protocol):
    """
    Protocol for configuration providers.

    Protocol defines interface that all configuration providers must
    implement. Enables dependency injection and testability by allowing
    different config sources (environment variables, files, vaults, etc.).

    Example implementations:
    - EnvConfigProvider: From environment variables (default)
    - FileConfigProvider: From JSON/YAML files (future)
    - VaultConfigProvider: From HashiCorp Vault (future)
    """

    def get_key(self, provider: str, required: bool = True) -> str | None:
        """
        Get API key for specific provider.

        :param provider: Provider name ('openai', 'anthropic', or 'gemini')
        :ptype provider: str
        :param required: If True, raises ConfigError when key not found
        :ptype required: bool
        :return: API key string, or None if not found and not required
        :rtype: str | None
        :raises ConfigError: If required=True and key not found
        :raises ValueError: If provider name is not recognized
        """
        ...

    def get_all_keys(self) -> dict[str, str | None]:
        """
        Get all configured API keys.

        :return: Dict mapping provider names to API keys (or None)
        :rtype: dict[str, str | None]
        """
        ...

    def validate(self, provider: str) -> None:
        """
        Validate that provider is configured.

        :param provider: Provider name to validate
        :ptype provider: str
        :return: None
        :rtype: None
        :raises ConfigError: If provider is not configured
        """
        ...

    def get_model_name(self, provider: str) -> str | None:
        """
        Get default model name for provider from configuration.

        :param provider: Provider name
        :ptype provider: str
        :return: Model name string, or None if not configured
        :rtype: str | None
        """
        ...


class LogFormatter(ABC):
    """
    Abstract base class for log formatters.

    ABC defines interface that all log formatters must implement.
    Enables different formatting strategies (enhanced, JSON, cloud logging)
    while maintaining consistent interface.

    Example implementations:
    - CustomFormatter: Enhanced format with project context (default)
    - JSONFormatter: JSON structured logging (future)
    - CloudLogFormatter: Cloud-specific format (future)

    Why ABC instead of Protocol:
    - logging.Formatter is already class (inheritance expected)
    - Need to override specific methods from base Formatter
    - Clear inheritance hierarchy desirable
    """

    @abstractmethod
    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record into string.

        Subclasses must implement this method to define their
        formatting strategy. Typically, they will enhance
        LogRecord with additional attributes before calling
        parent format() method.

        :param record: Log record to format
        :ptype record: logging.LogRecord
        :return: Formatted log string
        :rtype: str
        """
        pass
