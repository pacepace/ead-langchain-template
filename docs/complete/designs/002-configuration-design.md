# Design 002: Configuration Management Design

## Document Purpose

This document specifies the complete design for configuration management in the EAD LangChain Template, including the ConfigProvider protocol, environment variable handling, and API key management.

---

## Overview

### Responsibilities

The configuration module handles:
1. **Environment Loading**: Read .env files and environment variables
2. **API Key Management**: Retrieve provider-specific API keys
3. **Configuration Validation**: Check that required configuration exists
4. **Provider Abstraction**: Interface for swappable config sources

### Design Philosophy

- **Explicit over Implicit**: No magic environment variable lookups
- **Interface-Driven**: Code to protocols, not concrete implementations
- **Namespaced**: All variables use `EADLANGCHAIN_` prefix
- **Fail-Fast**: Clear errors when configuration is missing

---

## ConfigProvider Protocol (Interface)

### Protocol Definition

**File**: `src/langchain_llm/interfaces.py`

```python
from typing import Protocol

class ConfigProvider(Protocol):
    """
    Protocol for configuration providers.

    This protocol defines the interface that all configuration
    providers must implement. It enables dependency injection
    and testability by allowing different config sources
    (environment variables, files, vaults, etc.).

    Example implementations:
    - EnvConfigProvider: From environment variables
    - FileConfigProvider: From JSON/YAML files (future)
    - VaultConfigProvider: From HashiCorp Vault (future)
    """

    def get_key(self, provider: str, required: bool = True) -> str | None:
        """
        Get API key for a specific provider.

        :param provider: Provider name ('openai', 'anthropic', 'gemini')
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
        Validate that a provider is configured.

        :param provider: Provider name to validate
        :ptype provider: str
        :return: None
        :rtype: None
        :raises ConfigError: If provider is not configured
        """
        ...

    def get_model_name(self, provider: str) -> str | None:
        """
        Get default model name for a provider from configuration.

        :param provider: Provider name
        :ptype provider: str
        :return: Model name string, or None if not configured
        :rtype: str | None
        """
        ...
```

### Why Protocol (Not ABC)?

**Structural Subtyping**:
- No need to inherit from ConfigProvider
- Any class with matching methods automatically conforms
- More flexible, more Pythonic (duck typing with type safety)

**Example**:
```python
# This class conforms to ConfigProvider without inheriting
class MyCustomConfig:
    def get_key(self, provider: str, required: bool = True) -> str | None:
        # Implementation
        pass

    def get_all_keys(self) -> dict[str, str | None]:
        # Implementation
        pass

    # ... other methods

# Type checker accepts this
def create_llm(config: ConfigProvider):
    api_key = config.get_key("openai")
    # ...

my_config = MyCustomConfig()
create_llm(my_config)  # Works! Type checker validates protocol conformance
```

**Benefits**:
- Can retrofit existing classes
- No inheritance requirement
- Better for interfaces (describes contract, not implementation)
- Modern Python best practice (PEP 544)

---

## EnvConfigProvider Implementation

### Class Design

**File**: `src/langchain_llm/config.py`

```python
import os
from pathlib import Path

from dotenv import load_dotenv

from langchain_llm.interfaces import ConfigProvider  # Import protocol


class ConfigError(Exception):
    """
    Raised when there's a configuration error.

    Used for missing API keys, invalid provider names, or
    other configuration issues.
    """
    pass


class EnvConfigProvider:
    """
    Configuration provider that reads from environment variables.

    This is the default implementation of the ConfigProvider protocol.
    It reads configuration from environment variables, which can be
    set directly in the shell or loaded from a .env file.

    All environment variables use the EADLANGCHAIN_ prefix to avoid
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
        "google": "EADLANGCHAIN_AI_GEMINI_API_KEY",  # Alias for gemini
    }

    # Provider name to model environment variable mapping
    MODEL_MAP = {
        "openai": "EADLANGCHAIN_AI_OPENAI_MODEL",
        "anthropic": "EADLANGCHAIN_AI_ANTHROPIC_MODEL",
        "gemini": "EADLANGCHAIN_AI_GEMINI_MODEL",
        "google": "EADLANGCHAIN_AI_GEMINI_MODEL",  # Alias
    }

    def get_key(self, provider: str, required: bool = True) -> str | None:
        """
        Get API key for a specific provider.

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
            valid_providers = set(self.PROVIDER_MAP.keys())
            raise ValueError(
                f"Unknown provider: {provider}. "
                f"Supported providers: {', '.join(sorted(valid_providers))}"
            )

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
        Validate that a provider is configured with an API key.

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
        Get default model name for a provider from environment variables.

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
```

### Implementation Notes

**Provider Mapping**:
- Centralized in `PROVIDER_MAP` class attribute
- Easy to add new providers
- "google" alias for "gemini" (user convenience)

**Error Handling**:
- `ValueError` for unknown providers (programmer error)
- `ConfigError` for missing configuration (user error)
- Clear, actionable error messages

**Environment Variable Names**:
- Follow `EADLANGCHAIN_AI_<PROVIDER>_API_KEY` pattern
- Documented in error messages
- Referenced in .env.example

---

## Public API Functions (Convenience Layer)

### load_env_config()

**Purpose**: Load .env file into environment

```python
def load_env_config(env_file: str | None = None) -> None:
    """
    Load environment variables from .env file.

    This function uses python-dotenv to load variables from a .env
    file into the environment. It automatically searches for .env
    in the current directory and parent directories up to the
    project root.

    :param env_file: Path to .env file. If None, auto-discovers.
    :ptype env_file: str | None
    :return: None
    :rtype: None

    Example::

        >>> from langchain_llm import load_env_config
        >>> load_env_config()  # Loads from .env in project root
        >>> load_env_config("custom.env")  # Loads from specific file
    """
    if env_file:
        # Explicit path provided
        load_dotenv(env_file)
    else:
        # Auto-discover .env file by searching upward
        current = Path.cwd()
        for parent in [current] + list(current.parents):
            env_path = parent / ".env"
            if env_path.exists():
                load_dotenv(env_path)
                return

        # No .env file found, still call load_dotenv()
        # to allow system environment variables to work
        load_dotenv()
```

**Design Decisions**:
- **Upward Search**: Finds .env even when running from subdirectories
- **Graceful Fallback**: Works without .env (uses system env vars)
- **Explicit Path Support**: Can override auto-discovery
- **Project Root Detection**: Stops at directory with pyproject.toml or .git

**Search Strategy**:
```
Current: /path/to/project/examples/
Search:
  1. /path/to/project/examples/.env (not found)
  2. /path/to/project/.env (FOUND - load this)
```

### get_api_key()

**Purpose**: Convenience wrapper for EnvConfigProvider.get_key()

```python
# Module-level instance (singleton pattern)
_default_config = EnvConfigProvider()


def get_api_key(provider: str, required: bool = True) -> str | None:
    """
    Get API key for a specific provider.

    This is a convenience function that uses the default
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
        >>> gemini_key = get_api_key("gemini", required=False)  # None if not set
    """
    return _default_config.get_key(provider, required)
```

**Design**: Simple delegation to default instance

**Why Singleton Pattern**:
- Common case: single config source (environment variables)
- Simpler API for users (`get_api_key()` vs creating instance)
- Advanced users can still create custom instances

### get_all_api_keys()

**Purpose**: Check which providers are configured

```python
def get_all_api_keys() -> dict[str, str | None]:
    """
    Get all configured API keys.

    Returns a dictionary showing which providers have API keys configured.
    Useful for conditional example execution or debugging configuration.

    :return: Dictionary mapping provider names to API keys (or None if not set)
    :rtype: Dict[str, Optional[str]]

    Example::

        >>> from langchain_llm import get_all_api_keys
        >>> keys = get_all_api_keys()
        >>> configured = [k for k, v in keys.items() if v]
        >>> print(f"Configured providers: {configured}")
        Configured providers: ['openai', 'anthropic']
    """
    return _default_config.get_all_keys()
```

### validate_provider()

**Purpose**: Validate provider before use

```python
def validate_provider(provider: str) -> None:
    """
    Validate that a provider is configured with an API key.

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
```

### get_model_name()

**Purpose**: Get optional model configuration

```python
def get_model_name(provider: str) -> str | None:
    """
    Get default model name for a provider from environment variables.

    This is optional configuration. If not set, examples use
    their own hardcoded defaults.

    :param provider: Provider name ('openai', 'anthropic', or 'gemini')
    :ptype provider: str
    :return: Model name string, or None if not configured
    :rtype: str | None

    Example::

        >>> from langchain_llm import get_model_name
        >>> model = get_model_name("openai")
        >>> print(f"Using model: {model or 'gpt-4o-mini'}")
        Using model: gpt-4o
    """
    return _default_config.get_model_name(provider)
```

---

## Usage Patterns

### Pattern 1: Basic Usage (Most Common)

**Scenario**: Simple script using one provider

```python
from langchain_openai import ChatOpenAI
from langchain_llm import load_env_config, get_api_key

# Step 1: Load environment
load_env_config()

# Step 2: Get API key
api_key = get_api_key("openai")

# Step 3: Use with LangChain
llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)
response = llm.invoke("Hello!")
print(response.content)
```

### Pattern 2: Conditional Provider Usage

**Scenario**: Example that tries multiple providers

```python
from langchain_llm import load_env_config, get_all_api_keys, get_api_key
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

load_env_config()
keys = get_all_api_keys()

# Try OpenAI if available
if keys["openai"]:
    api_key = get_api_key("openai")
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)
    print("Using OpenAI")

# Fall back to Anthropic
elif keys["anthropic"]:
    api_key = get_api_key("anthropic")
    llm = ChatAnthropic(model="claude-3-5-haiku", api_key=api_key)
    print("Using Anthropic")

else:
    print("No providers configured")
    exit(1)

response = llm.invoke("Hello!")
print(response.content)
```

### Pattern 3: Graceful Error Handling

**Scenario**: Skip unavailable providers

```python
from langchain_llm import load_env_config, get_api_key, ConfigError

load_env_config()

def try_provider(provider_name, create_llm_func):
    """Try to use a provider, skip if not configured."""
    try:
        api_key = get_api_key(provider_name)
        llm = create_llm_func(api_key)
        response = llm.invoke("Hello!")
        print(f"{provider_name}: {response.content}")
    except ConfigError as e:
        print(f"[SKIPPED] {provider_name}: {e}")

try_provider("openai", lambda key: ChatOpenAI(api_key=key))
try_provider("anthropic", lambda key: ChatAnthropic(api_key=key))
try_provider("gemini", lambda key: ChatGoogleGenerativeAI(google_api_key=key))
```

### Pattern 4: Advanced (Custom Config Provider)

**Scenario**: Testing with mocked configuration

```python
from typing import Optional, Dict

# Implement ConfigProvider protocol
class MockConfigProvider:
    """Mock configuration for testing."""

    def __init__(self, mock_keys: dict[str, str]):
        self.keys = mock_keys

    def get_key(self, provider: str, required: bool = True) -> str | None:
        key = self.keys.get(provider)
        if required and not key:
            raise ConfigError(f"No key for {provider}")
        return key

    def get_all_keys(self) -> dict[str, str | None]:
        return {"openai": self.keys.get("openai"),
                "anthropic": self.keys.get("anthropic"),
                "gemini": self.keys.get("gemini")}

    def validate(self, provider: str) -> None:
        self.get_key(provider, required=True)

    def get_model_name(self, provider: str) -> str | None:
        return None

# Use in tests
mock_config = MockConfigProvider({"openai": "test-key-123"})
api_key = mock_config.get_key("openai")
# api_key == "test-key-123"
```

---

## Environment Variable Specifications

### Required Variables (Provider API Keys)

```bash
# OpenAI
EADLANGCHAIN_AI_OPENAI_API_KEY=sk-proj-...

# Anthropic
EADLANGCHAIN_AI_ANTHROPIC_API_KEY=sk-ant-...

# Google Gemini
EADLANGCHAIN_AI_GEMINI_API_KEY=...
```

**Format**:
- OpenAI: Starts with `sk-` or `sk-proj-`
- Anthropic: Starts with `sk-ant-`
- Gemini: Alphanumeric string

**Validation**: Module doesn't validate format (providers do that)

### Optional Variables (Model Overrides)

```bash
# Override default OpenAI model
EADLANGCHAIN_AI_OPENAI_MODEL=gpt-4o

# Override default Anthropic model
EADLANGCHAIN_AI_ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# Override default Gemini model
EADLANGCHAIN_AI_GEMINI_MODEL=gemini-1.5-pro
```

**Behavior**:
- If not set, examples use their hardcoded defaults
- If set, `get_model_name()` returns value
- Examples can choose to honor or ignore

---

## Error Handling Design

### ConfigError Exception

**Purpose**: Configuration-related errors

**When Raised**:
- Required API key not found
- Invalid provider configuration
- Environment not loaded

**Error Message Format**:
```
ConfigError: API key not found for provider '{provider}'.
Please set {env_var_name} in your .env file or environment variables.
See .env.example for template.
```

**Design Goals**:
- User-friendly (not technical jargon)
- Actionable (tells user what to do)
- Informative (includes exact variable name)
- References documentation (.env.example)

### ValueError for Invalid Input

**Purpose**: Programmer errors (invalid provider names)

**When Raised**:
- Unknown provider name passed
- Typos in provider names

**Error Message Format**:
```
ValueError: Unknown provider: foo.
Supported providers: anthropic, gemini, openai
```

**Design Goals**:
- List valid options
- Alphabetically sorted
- Excludes aliases from "supported" list (but still works)

---

## Testing Strategy

### Unit Tests (TDD)

**File**: `tests/unit/test_config.py`

**Test Categories**:

1. **Environment Loading**:
   - `test_load_env_config_with_explicit_path()`
   - `test_load_env_config_auto_discovery()`
   - `test_load_env_config_without_file()`

2. **API Key Retrieval**:
   - `test_get_api_key_with_valid_key()`
   - `test_get_api_key_with_missing_key_required()`
   - `test_get_api_key_with_missing_key_optional()`
   - `test_get_api_key_case_insensitive()`
   - `test_get_api_key_invalid_provider()`

3. **Provider Validation**:
   - `test_validate_provider_with_valid_key()`
   - `test_validate_provider_with_missing_key()`

4. **Multiple Keys**:
   - `test_get_all_api_keys()`
   - `test_get_all_api_keys_partial()`

5. **Model Names**:
   - `test_get_model_name_when_set()`
   - `test_get_model_name_when_not_set()`

**Fixtures** (from conftest.py):
```python
@pytest.fixture
def mock_env_vars(monkeypatch):
    """Set up test environment variables."""
    monkeypatch.setenv("EADLANGCHAIN_AI_OPENAI_API_KEY", "test-openai-key")
    monkeypatch.setenv("EADLANGCHAIN_AI_ANTHROPIC_API_KEY", "test-anthropic-key")
    monkeypatch.setenv("EADLANGCHAIN_AI_GEMINI_API_KEY", "test-gemini-key")

@pytest.fixture
def clean_env(monkeypatch):
    """Remove all EADLANGCHAIN environment variables."""
    import os
    for key in list(os.environ.keys()):
        if key.startswith("EADLANGCHAIN_"):
            monkeypatch.delenv(key, raising=False)
```

### Protocol Conformance Test

**Purpose**: Ensure EnvConfigProvider conforms to ConfigProvider protocol

```python
def test_env_config_provider_conforms_to_protocol():
    """Test that EnvConfigProvider implements ConfigProvider protocol."""
    from langchain_llm.interfaces import ConfigProvider
    from langchain_llm.config import EnvConfigProvider

    config = EnvConfigProvider()

    # Type checker validates this
    assert isinstance(config, ConfigProvider)

    # Runtime check: has all required methods
    assert hasattr(config, "get_key")
    assert hasattr(config, "get_all_keys")
    assert hasattr(config, "validate")
    assert hasattr(config, "get_model_name")
```

---

## Future Enhancements

### Vault Integration (Future)

**Scenario**: Production deployment with secrets in vault

```python
class VaultConfigProvider:
    """Configuration from HashiCorp Vault."""

    def __init__(self, vault_url: str, token: str):
        import hvac
        self.client = hvac.Client(url=vault_url, token=token)

    def get_key(self, provider: str, required: bool = True) -> str | None:
        path = f"secret/data/llm/{provider}"
        try:
            response = self.client.secrets.kv.v2.read_secret_version(path=path)
            return response["data"]["data"]["api_key"]
        except Exception:
            if required:
                raise ConfigError(f"Could not retrieve key for {provider} from Vault")
            return None

    # ... implement other methods
```

**Usage** (no changes to examples needed):
```python
# Instead of EnvConfigProvider
config = VaultConfigProvider(vault_url, token)
api_key = config.get_key("openai")
```

### AWS Secrets Manager (Future)

```python
class AWSSecretsConfigProvider:
    """Configuration from AWS Secrets Manager."""

    def __init__(self, region: str):
        import boto3
        self.client = boto3.client("secretsmanager", region_name=region)

    def get_key(self, provider: str, required: bool = True) -> str | None:
        secret_name = f"llm/{provider}/api_key"
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
            return response["SecretString"]
        except Exception:
            if required:
                raise ConfigError(f"Could not retrieve key for {provider} from AWS")
            return None

    # ... implement other methods
```

### File-Based Configuration (Future)

```python
class FileConfigProvider:
    """Configuration from JSON/YAML file."""

    def __init__(self, config_file: str):
        import json
        with open(config_file) as f:
            self.config = json.load(f)

    def get_key(self, provider: str, required: bool = True) -> str | None:
        key = self.config.get("providers", {}).get(provider, {}).get("api_key")
        if required and not key:
            raise ConfigError(f"No API key for {provider} in config file")
        return key

    # ... implement other methods
```

**Config File** (config.json):
```json
{
  "providers": {
    "openai": {
      "api_key": "sk-...",
      "model": "gpt-4o"
    },
    "anthropic": {
      "api_key": "sk-ant-...",
      "model": "claude-3-5-sonnet-20241022"
    }
  }
}
```

---

## Security Considerations

### No Logging of Secrets

```python
# GOOD: Log that we retrieved a key, not the key itself
logger.info(f"Retrieved API key for provider: {provider}")

# BAD: Logs the actual secret
logger.debug(f"API key: {api_key}")  # NEVER DO THIS
```

### Key Masking (Optional Enhancement)

```python
def mask_key(key: str, visible_chars: int = 7) -> str:
    """
    Mask API key for safe logging.

    :param key: API key to mask
    :ptype key: str
    :param visible_chars: Number of characters to show
    :ptype visible_chars: int
    :return: Masked key string
    :rtype: str

    Example::

        >>> mask_key("sk-proj-abcdefghijklmnop")
        'sk-proj...***'
    """
    if len(key) <= visible_chars:
        return "***"
    return f"{key[:visible_chars]}...***"
```

### Environment Isolation in Tests

```python
# Use monkeypatch to ensure test isolation
def test_something(monkeypatch):
    """Test with isolated environment."""
    # Clear all env vars
    for key in list(os.environ.keys()):
        if key.startswith("EADLANGCHAIN_"):
            monkeypatch.delenv(key, raising=False)

    # Set only what this test needs
    monkeypatch.setenv("EADLANGCHAIN_AI_OPENAI_API_KEY", "test-key")

    # Test runs in isolation
    # ...
```

---

## Module Organization

### File: `src/langchain_llm/config.py`

**Contents**:
1. Imports
2. `ConfigError` exception class
3. `EnvConfigProvider` class (implements protocol)
4. `load_env_config()` function
5. Module-level `_default_config` instance
6. Public API functions (`get_api_key`, `get_all_api_keys`, etc.)

**Size**: ~150-200 lines

**Dependencies**:
- Standard library: `os`, `pathlib`
- Third-party: `python-dotenv`
- Local: `langchain_llm.interfaces.ConfigProvider`

---

## Related Documents

- **Previous**: [001-project-structure.md](001-project-structure.md) - Project layout
- **Next**: [003-logging-design.md](003-logging-design.md) - Logging module design
- **See Also**:
  - [requirements/003-environment-conventions.md](../requirements/003-environment-conventions.md) - Env var conventions
  - [000-architecture-overview.md](000-architecture-overview.md) - Architecture decisions

## Document Metadata

- **Version**: 1.0
- **Status**: Active
- **Owner**: EAD LangChain Template Team
