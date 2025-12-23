"""
LangChain LLM Utilities for EAD LangChain Template

A minimal utility package providing:
- Custom logging with standardized format
- Configuration helpers for managing API keys
- Clean patterns for working with LangChain providers

Example usage::

    from langchain_llm import setup_logging, get_logger, load_env_config, get_api_key

    # Setup
    setup_logging(level="INFO")
    load_env_config()

    # Use
    logger = get_logger(__name__)
    api_key = get_api_key("openai")
"""

from langchain_llm.config import (
    ConfigError,
    get_all_api_keys,
    get_api_key,
    get_model_name,
    load_env_config,
    validate_provider,
)
from langchain_llm.logging_config import get_logger, setup_logging

__version__ = "0.1.0"

__all__ = [
    "setup_logging",
    "get_logger",
    "load_env_config",
    "get_api_key",
    "get_all_api_keys",
    "get_model_name",
    "validate_provider",
    "ConfigError",
]
