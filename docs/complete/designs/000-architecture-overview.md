# Design 000: Architecture Overview

## Document Purpose

This document provides the high-level architectural vision for the EAD LangChain Template. It establishes design principles, architectural patterns, and the overall system structure that guides all implementation decisions.

---

## System Vision

### What This Is
A **thin utility layer** providing clean patterns for LLM applications, not a framework or application.

### What This Is NOT
- Not a framework (doesn't control your application flow)
- Not an abstraction over LangChain (we USE LangChain, not wrap it)
- Not a production application (it's a template and learning tool)
- Not feature-complete (intentionally minimal)

---

## Core Design Principles

### DP-001: Thin Utility Layer

**Principle**: Provide utilities, not business logic

**What This Means**:
- Configuration management (loading env vars, getting API keys)
- Logging setup (standardized format, easy initialization)
- Common patterns (not custom implementations)
- Educational examples (showing how to use LangChain)

**What This Avoids**:
- Custom LLM wrappers
- Business logic
- Application state management
- Complex abstractions

**Benefits**:
- Easy to understand
- Easy to extend
- Easy to adopt incrementally
- No vendor lock-in to our patterns

### DP-002: LangChain First

**Principle**: Use LangChain's built-in features, don't reinvent

**Examples**:
```python
# RIGHT: Use LangChain directly
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)
response = llm.invoke("prompt")

# WRONG: Custom wrapper
class MyLLM:
    def __init__(self, provider):
        # Custom implementation
        pass
```

**Rationale**:
- LangChain is well-maintained and feature-rich
- Users learn portable skills (LangChain knowledge transfers)
- We benefit from LangChain improvements automatically
- Less code to maintain

**When We Add Utilities**:
- Only for cross-cutting concerns (config, logging)
- Only when LangChain doesn't provide it
- Only when it benefits all use cases

### DP-003: Interface-Driven Design

**Principle**: Define interfaces (protocols/ABCs), code to interfaces

**Why Interfaces**:
- **Testability**: Can mock/stub implementations easily
- **Flexibility**: Multiple implementations possible (env vars, files, vaults)
- **Documentation**: Interface IS the contract
- **Type Safety**: Python type checkers understand protocols

**Key Interfaces**:
1. **`ConfigProvider` Protocol**: Configuration access abstraction
2. **`LogFormatter` ABC**: Custom log formatting

**Example**:
```python
# Define interface
from typing import Protocol, Optional

class ConfigProvider(Protocol):
    def get_key(self, provider: str, required: bool = True) -> str | None:
        """Get API key for provider."""
        ...

# Implement interface
class EnvConfigProvider:
    def get_key(self, provider: str, required: bool = True) -> str | None:
        # Actual implementation
        pass

# Use interface
def create_llm(config: ConfigProvider, provider: str):
    api_key = config.get_key(provider)
    # ... create LLM
```

**Benefits**:
- Tests can inject mock config
- Can swap env vars for vault/secrets manager later
- Clear contract for implementers
- Type hints work correctly
- **AI Assistance**: Interfaces enable AI assistants to understand contracts without reading implementations, making code navigation and suggestion generation more accurate. Clear boundaries between what and how prevent AI from suggesting changes that break abstractions.

### DP-004: Explicit Over Implicit

**Principle**: Make configuration and dependencies explicit

**Examples**:
```python
# RIGHT: Explicit API key
api_key = get_api_key("openai")
llm = ChatOpenAI(api_key=api_key)

# WRONG: Implicit (relies on global env var)
llm = ChatOpenAI()  # Looks for OPENAI_API_KEY globally
```

**Benefits**:
- No magic or hidden behavior
- Clear data flow
- Easy to test (inject dependencies)
- No surprises

**Applies To**:
- API keys (always passed explicitly)
- Configuration (load_env_config() called explicitly)
- Logging (setup_logging() called explicitly)
- Model names (specified in code, not hidden defaults)

### DP-005: Progressive Disclosure

**Principle**: Teach from simple to complex, gradually

**Example Progression**:
1. **01_basic.py**: Simplest possible usage (one function call)
2. **02_streaming.py**: Add streaming (one new concept)
3. **03_conversation.py**: Add message history (one new concept)
4. **04_advanced.py**: Add callbacks, batching (production features)

**Each Example**:
- Builds on previous examples
- Introduces ONE new concept
- Works independently (not required to run previous examples)
- Includes explanation of WHY this feature matters

**Benefits**:
- Gentle learning curve
- Reinforces fundamentals
- Clear progression path
- Reduced cognitive load

### DP-006: Test-Driven Development

**Principle**: Tests first, implementation second

**TDD Cycle**:
1. **Red**: Write failing test
2. **Green**: Minimal code to pass
3. **Refactor**: Improve while keeping tests green

**Benefits**:
- Forces thinking about interfaces first
- Ensures code is testable
- Documents expected behavior
- Catches regressions
- Enables confident refactoring

**Scope**:
- ALL code in `src/langchain_llm/` follows TDD
- Examples SHOULD have tests but TDD not required
- Documentation doesn't need tests

---

## System Architecture

### High-Level Structure

```
┌─────────────────────────────────────────────────────────────┐
│                      User Application                        │
│                  (Examples or Custom Code)                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ imports
                              ▼
┌─────────────────────────────────────────────────────────────┐
│               langchain_llm Package (Thin Layer)             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Config     │  │   Logging    │  │  Interfaces  │      │
│  │  Management  │  │    Setup     │  │  (Protocol)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ uses
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   LangChain Ecosystem                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  langchain-  │  │  langchain-  │  │  langchain-  │      │
│  │   openai     │  │  anthropic   │  │ google-genai │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ API calls
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      LLM Providers                           │
│        OpenAI          Anthropic         Google Gemini       │
└─────────────────────────────────────────────────────────────┘
```

### Layers Explained

#### Layer 1: User Application / Examples
- **Responsibility**: Business logic, application flow
- **Examples**: `examples/01_basic.py`, custom user code
- **Dependencies**: imports from langchain_llm and LangChain

#### Layer 2: langchain_llm Package (Our Code)
- **Responsibility**: Cross-cutting utilities
- **Components**:
  - Configuration management
  - Logging setup
  - Interfaces/protocols
- **Dependencies**: Standard library, dotenv, LangChain core
- **Size**: Small (<500 lines total)

#### Layer 3: LangChain Ecosystem
- **Responsibility**: LLM abstractions, provider integration
- **Packages**: langchain-core, langchain-openai, langchain-anthropic, langchain-google-genai
- **Dependencies**: Provider SDKs (openai, anthropic, google-generativeai)

#### Layer 4: LLM Providers
- **Responsibility**: Actual AI models
- **Providers**: OpenAI, Anthropic, Google
- **Interface**: REST APIs

---

## Component Architecture

### Configuration Module

**Purpose**: Manage API keys and settings via environment variables

**Interface**:
```python
# Protocol (interface definition)
class ConfigProvider(Protocol):
    def get_key(self, provider: str, required: bool = True) -> str | None: ...
    def get_all_keys(self) -> dict[str, str | None]: ...
    def validate(self, provider: str) -> None: ...
    def get_model_name(self, provider: str) -> str | None: ...

# Implementation
class EnvConfigProvider:
    """Configuration from environment variables."""
    # Implements ConfigProvider protocol
    pass

# Public API functions (convenience wrappers)
def load_env_config(env_file: str | None = None) -> None: ...
def get_api_key(provider: str, required: bool = True) -> str | None: ...
```

**Data Flow**:
```
.env file → load_dotenv() → os.environ → get_api_key() → User Code
```

**Design Decisions**:
- Use python-dotenv for .env parsing
- Namespaced variables (EADLANGCHAIN_*)
- Environment variables as source of truth
- Protocol allows future vault/secrets manager integration

### Logging Module

**Purpose**: Standardized logging with enhanced context

**Interface**:
```python
# Abstract Base Class (interface)
class LogFormatter(ABC):
    @abstractmethod
    def format(self, record: logging.LogRecord) -> str: ...

# Implementation
class CustomFormatter(LogFormatter):
    """Enhanced formatter with relative paths and class names."""
    def format(self, record: logging.LogRecord) -> str:
        # Add relative_path, metaclass_name
        return super().format(record)

# Public API functions
def setup_logging(level: str | None = None, ...) -> logging.Logger: ...
def get_logger(name: str) -> logging.Logger: ...
```

**Data Flow**:
```
Logger Call → CustomFormatter → Enhanced LogRecord → Console/File
```

**Design Decisions**:
- Extend Python's logging (don't replace it)
- Custom formatter for enhanced context
- Project-relative paths (not absolute)
- Class name detection via frame inspection

### Interfaces Module (NEW)

**Purpose**: Define protocols and ABCs for the package

**Contents**:
```python
# src/langchain_llm/interfaces.py

from typing import Protocol
from abc import ABC, abstractmethod
import logging

# Configuration Protocol
class ConfigProvider(Protocol):
    """Protocol for configuration providers."""
    def get_key(self, provider: str, required: bool = True) -> str | None: ...
    def get_all_keys(self) -> dict[str, str | None]: ...
    def validate(self, provider: str) -> None: ...
    def get_model_name(self, provider: str) -> str | None: ...

# Logging ABC
class LogFormatter(ABC):
    """Abstract base for log formatters."""
    @abstractmethod
    def format(self, record: logging.LogRecord) -> str:
        """Format a log record."""
        pass
```

**Why Separate File**:
- Clear interface documentation
- Avoid circular imports
- Easy to find all interfaces
- Can import just interfaces for type hints

---

## Data Flow Patterns

### Configuration Loading Pattern

```
┌──────────┐
│  Start   │
└────┬─────┘
     │
     ▼
┌─────────────────────┐
│ load_env_config()   │  ← Loads .env file
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Environment Vars    │  ← EADLANGCHAIN_AI_OPENAI_API_KEY=...
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ get_api_key("openai")│  ← Retrieve specific key
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Create LLM          │  ← ChatOpenAI(api_key=key)
└─────────────────────┘
```

### Logging Setup Pattern

```
┌──────────┐
│  Start   │
└────┬─────┘
     │
     ▼
┌─────────────────────┐
│ setup_logging()     │  ← Configure root logger
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ CustomFormatter     │  ← Enhance log records
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ get_logger(__name__) │  ← Get module logger
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ logger.info(...)    │  ← Log with enhanced format
└─────────────────────┘
```

### Example Execution Pattern

```
┌──────────┐
│  Start   │
└────┬─────┘
     │
     ▼
┌─────────────────────┐
│ setup_logging()     │  Step 1: Configure logging
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ load_env_config()   │  Step 2: Load environment
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ get_api_key()       │  Step 3: Get credentials
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Create LLM (LangChain)│  Step 4: Use LangChain
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ llm.invoke() or     │  Step 5: Call LLM
│ llm.stream()        │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Print/Process       │  Step 6: Handle response
│ Response            │
└─────────────────────┘
```

---

## Extensibility Points

### Adding New Providers

**Current**: OpenAI, Anthropic, Gemini

**To Add New Provider** (e.g., Cohere):
1. Install provider package: `poetry add langchain-cohere`
2. Add env var to .env.example: `EADLANGCHAIN_AI_COHERE_API_KEY=...`
3. Add mapping in config.py:
   ```python
   provider_map = {
       "openai": "EADLANGCHAIN_AI_OPENAI_API_KEY",
       "anthropic": "EADLANGCHAIN_AI_ANTHROPIC_API_KEY",
       "gemini": "EADLANGCHAIN_AI_GEMINI_API_KEY",
       "cohere": "EADLANGCHAIN_AI_COHERE_API_KEY",  # NEW
   }
   ```
4. Add example: `examples/01_basic.py` → add `basic_cohere_example()`

**No changes needed**: Logging, testing infrastructure, project structure

### Adding New Configuration Sources

**Current**: Environment variables via .env files

**Future**: Vault, AWS Secrets Manager, GCP Secret Manager

**How to Add** (thanks to ConfigProvider protocol):
```python
# New implementation
class VaultConfigProvider:
    """Configuration from HashiCorp Vault."""
    def __init__(self, vault_url: str, token: str):
        self.client = VaultClient(vault_url, token)

    def get_key(self, provider: str, required: bool = True) -> str | None:
        path = f"secret/llm/{provider}/api_key"
        return self.client.read(path)

# Usage (no changes to examples)
config = VaultConfigProvider(url, token)
api_key = config.get_key("openai")
```

**Interface makes this possible**: Code depends on protocol, not implementation

### Adding New Log Formatters

**Current**: CustomFormatter with relative paths

**Future**: JSON formatter, Cloud logging formatter

**How to Add**:
```python
class JSONLogFormatter(LogFormatter):
    """Format logs as JSON for structured logging."""
    def format(self, record: logging.LogRecord) -> str:
        return json.dumps({
            "level": record.levelname,
            "message": record.getMessage(),
            "timestamp": record.created,
            "module": record.module,
        })

# Usage
setup_logging(formatter_class=JSONLogFormatter)
```

---

## Non-Functional Architecture Decisions

### Performance
- **Import Time**: Package loads in <1s (lightweight imports)
- **Runtime Overhead**: Logging adds <5% overhead
- **Test Execution**: < 30 seconds for full suite

**Strategies**:
- Lazy imports where possible
- Minimal computation during module import
- Efficient log formatting (cache project root)

### Security
- **No Secrets in Code**: All credentials via environment
- **No Logging of Secrets**: API keys never logged
- **Dependency Trust**: Only official PyPI packages

**Patterns**:
- .env files in .gitignore
- Explicit vs implicit configuration
- Key masking in debug output (future)

### Maintainability
- **Small Surface Area**: <500 lines in src/
- **High Test Coverage**: >80% for utilities
- **Clear Interfaces**: Protocols define contracts
- **Documentation**: Every function has Sphinx docstring

**Goals**:
- Easy to understand in one sitting
- Easy to modify without breaking
- Easy to extend with new features

---

## Architecture Decision Records (ADRs)

### ADR-001: Use Python Protocols Instead of ABCs for ConfigProvider

**Status**: Accepted

**Context**: Need interface for configuration access, can use ABC or Protocol

**Decision**: Use Protocol (structural subtyping)

**Rationale**:
- No need to inherit (more flexible)
- Better type checker support
- Pythonic (duck typing with type safety)
- Can retrofit existing classes

**Consequences**:
- ConfigProvider doesn't need to be inherited
- Type checkers validate implementations
- More flexible for users

### ADR-002: Use ABC for LogFormatter

**Status**: Accepted

**Context**: Need interface for log formatters

**Decision**: Use ABC (nominal subtyping)

**Rationale**:
- logging.Formatter is already a class (inheritance expected)
- Need to override specific methods
- ABC provides clear inheritance chain

**Consequences**:
- Must inherit from LogFormatter ABC
- Clear inheritance hierarchy
- Can use ABC features (abstractmethod)

### ADR-003: Don't Abstract Over LangChain

**Status**: Accepted

**Context**: Should we create wrapper layer over LangChain?

**Decision**: NO, use LangChain directly

**Rationale**:
- Thin utility layer philosophy
- LangChain is well-designed
- Users should learn LangChain, not our abstraction
- Less code to maintain

**Consequences**:
- Examples show LangChain directly
- Breaking changes in LangChain affect us
- But: Users learn transferable skills

### ADR-004: Namespaced Environment Variables

**Status**: Accepted

**Context**: Should we use generic variable names (OPENAI_API_KEY) or custom?

**Decision**: Use EADLANGCHAIN_* prefix for all variables

**Rationale**:
- Prevents conflicts with other tools
- Clear ownership
- Professional pattern
- Explicit vs implicit

**Consequences**:
- Must pass API keys explicitly to LangChain
- No reliance on provider defaults
- More verbose but clearer

### ADR-005: Src-Layout Package Structure

**Status**: Accepted

**Context**: Where should package code live? Root vs src/?

**Decision**: Use src/ layout (src/langchain_llm/)

**Rationale**:
- Prevents accidental imports of uninstalled package
- Forces proper package installation
- Industry best practice
- Cleaner separation

**Consequences**:
- Must install package to use it
- Slightly more complex setup
- But: Catches packaging issues early

---

## Future Architecture Considerations

### Potential Additions (Out of Current Scope)
- **Caching Layer**: Cache LLM responses for cost savings
- **Rate Limiting**: Automatic retry/backoff for API limits
- **Cost Tracking**: Token usage and cost monitoring
- **Multi-Provider Fallback**: Try alternative providers if one fails
- **Prompt Templates**: Reusable prompt patterns
- **Response Validation**: Schema validation for LLM outputs

**Why Not Now**:
- Maintain thin utility layer philosophy
- Avoid feature creep
- Let users implement business logic
- Focus on educational value

**When to Add**:
- If multiple developers need same feature
- If it's truly cross-cutting (benefits all use cases)
- If it doesn't add significant complexity
- If it aligns with thin utility layer philosophy

---

## Related Documents

- **Previous**: [requirements/004-quality-requirements.md](../requirements/004-quality-requirements.md) - Quality standards
- **Next**: [001-project-structure.md](001-project-structure.md) - Directory layout
- **See Also**:
  - [002-configuration-design.md](002-configuration-design.md) - Config module design
  - [003-logging-design.md](003-logging-design.md) - Logging module design

## Document Metadata

- **Version**: 1.0
- **Status**: Active
- **Owner**: EAD LangChain Template Team
