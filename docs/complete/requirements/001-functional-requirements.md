# Requirements 001: Functional Requirements

## Document Purpose

This document defines the specific features and capabilities that the EAD LangChain Template must provide. Each requirement is tied to user stories and acceptance criteria.

## Overview

The template provides three main functional areas:
1. **Configuration Management** - Safe, namespaced API key and settings management
2. **Logging Utilities** - Standardized logging with enhanced context
3. **Progressive Examples** - Educational demonstrations from basic to advanced LLM usage

---

## FR-001: Configuration Management

### User Story
**As a** developer
**I want** simple, safe API key management
**So that** I can focus on learning LangChain without worrying about security or conflicts

### Functional Requirements

#### FR-001.1: Environment Variable Loading
- **Description**: Load configuration from `.env` files automatically
- **Priority**: MUST HAVE
- **Details**:
  - Search for `.env` file in current directory and parent directories
  - Support explicit path specification
  - Fall back to system environment variables if no `.env` found
  - Use `python-dotenv` for `.env` file parsing

**Acceptance Criteria**:
- [ ] `load_env_config()` loads `.env` from project root
- [ ] Can specify custom `.env` path: `load_env_config("custom.env")`
- [ ] Works when called from subdirectories (searches upward)
- [ ] System env vars work if no `.env` file exists
- [ ] No errors if `.env` file is missing

#### FR-001.2: API Key Retrieval
- **Description**: Retrieve API keys for supported LLM providers
- **Priority**: MUST HAVE
- **Supported Providers**: OpenAI, Anthropic, Google Gemini
- **Details**:
  - Map provider names to environment variable keys
  - Support case-insensitive provider names
  - Option to require API key or return None
  - Clear error messages when keys are missing

**Acceptance Criteria**:
- [ ] `get_api_key("openai")` returns OpenAI API key
- [ ] `get_api_key("anthropic")` returns Anthropic API key
- [ ] `get_api_key("gemini")` returns Gemini API key
- [ ] Case insensitive: `get_api_key("OpenAI")` works
- [ ] `get_api_key("openai", required=False)` returns None if not set
- [ ] `get_api_key("openai", required=True)` raises ConfigError if not set
- [ ] `get_api_key("invalid")` raises ValueError for unknown provider
- [ ] Error messages include environment variable name and provider

**Example Usage**:
```python
from langchain_llm import load_env_config, get_api_key

load_env_config()
openai_key = get_api_key("openai")  # raises ConfigError if not found
gemini_key = get_api_key("gemini", required=False)  # returns None if not found
```

#### FR-001.3: Multi-Provider Key Discovery
- **Description**: Check which providers are configured
- **Priority**: SHOULD HAVE
- **Details**:
  - Return dictionary of all supported providers and their keys
  - Include None for unconfigured providers
  - Enable conditional example execution

**Acceptance Criteria**:
- [ ] `get_all_api_keys()` returns dict with all provider names
- [ ] Returns actual key values (or None) for each provider
- [ ] Dict keys: "openai", "anthropic", "gemini"
- [ ] Can be used to check: `if keys["openai"]: run_openai_example()`

**Example Usage**:
```python
keys = get_all_api_keys()
# {'openai': 'sk-...', 'anthropic': None, 'gemini': 'AI...'}

if keys["openai"]:
    run_openai_example()
```

#### FR-001.4: Provider Validation
- **Description**: Validate that a provider is configured before use
- **Priority**: SHOULD HAVE
- **Details**:
  - Raise ConfigError if provider not configured
  - Used in examples to fail fast with clear error
  - Same error messages as `get_api_key(required=True)`

**Acceptance Criteria**:
- [ ] `validate_provider("openai")` raises ConfigError if not configured
- [ ] `validate_provider("openai")` succeeds silently if configured
- [ ] Error messages are identical to `get_api_key()` errors

#### FR-001.5: Default Model Configuration
- **Description**: Optionally configure default models per provider
- **Priority**: NICE TO HAVE
- **Details**:
  - Allow env vars like `EADLANGCHAIN_AI_OPENAI_MODEL=gpt-4o`
  - Return None if not configured (examples use their own defaults)
  - Enable per-user model preferences

**Acceptance Criteria**:
- [ ] `get_model_name("openai")` returns configured model or None
- [ ] Works for all supported providers
- [ ] Examples work whether or not model is configured
- [ ] Returns None for unknown providers

---

## FR-002: Logging Utilities

### User Story
**As a** developer using this template
**I want** detailed, consistent logging
**So that** I can debug issues and understand application flow

### Functional Requirements

#### FR-002.1: Custom Log Formatting
- **Description**: Provide enhanced log format with project context
- **Priority**: MUST HAVE
- **Format Components**:
  - Log level (8 characters, left-aligned)
  - Timestamp (YYYY-MM-DD HH:MM:SS)
  - Relative file path from project root (dot-notation, no `.py` extension)
  - Class name if logged from within a class method
  - Module, function, and line number
  - Log message

**Format Example**:
```
INFO     2025-01-15 10:30:45 examples.01_basic.basic_openai_example.27: Running OpenAI example
DEBUG    2025-01-15 10:30:46 src.langchain_llm.config.get_api_key.75: Retrieved API key for provider: openai
```

**Acceptance Criteria**:
- [ ] Format matches: `%(levelname)-8s %(asctime)s %(relative_path)s.%(metaclass_name)s%(funcName)s.%(lineno)d: %(message)s`
- [ ] Relative path is computed from project root (detected via pyproject.toml or .git)
- [ ] Class name appears only when logging from instance/class methods
- [ ] File paths use dot notation: `examples.01_basic` not `examples/01_basic.py`
- [ ] All log levels display correctly (DEBUG, INFO, WARNING, ERROR, CRITICAL)

#### FR-002.2: Logging Setup Function
- **Description**: Simple function to configure logging globally
- **Priority**: MUST HAVE
- **Details**:
  - Configure root logger with custom formatter
  - Set log level (default: INFO, or from env var)
  - Optionally log to file
  - Clear existing handlers to avoid duplicates
  - Add console handler (always)
  - Add file handler (optional)

**Acceptance Criteria**:
- [ ] `setup_logging()` configures root logger with INFO level
- [ ] `setup_logging(level="DEBUG")` sets DEBUG level
- [ ] `setup_logging(log_file="logs/app.log")` writes to file
- [ ] Respects `EADLANGCHAIN_LOG_LEVEL` environment variable
- [ ] Respects `EADLANGCHAIN_LOG_FILE` environment variable
- [ ] Creates log file directory if it doesn't exist
- [ ] Clears existing handlers on each call (idempotent)
- [ ] Returns configured root logger

**Example Usage**:
```python
from langchain_llm import setup_logging

# Basic setup
setup_logging()

# With custom level
setup_logging(level="DEBUG")

# With file output
setup_logging(level="INFO", log_file="logs/app.log")
```

#### FR-002.3: Logger Factory
- **Description**: Get named loggers for modules
- **Priority**: MUST HAVE
- **Details**:
  - Thin wrapper around `logging.getLogger()`
  - Enables module-specific logging
  - Inherits configuration from root logger

**Acceptance Criteria**:
- [ ] `get_logger(__name__)` returns logger instance
- [ ] Logger inherits root logger configuration
- [ ] Multiple calls with same name return same logger
- [ ] Logger can be used immediately after `setup_logging()`

**Example Usage**:
```python
from langchain_llm import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)

logger.debug("Detailed debug info")
logger.info("Something happened")
logger.warning("Be careful")
logger.error("Something went wrong")
```

#### FR-002.4: Evidence-Based Troubleshooting Format
- **Description**: Log format must enable direct navigation from log entries to source code
- **Priority**: MUST HAVE
- **Details**:
  - Each log entry includes project-relative file path, function name, and line number
  - Format pattern: `file.function.line` enables immediate "log → source" navigation
  - Relative paths work across different environments and machines
  - Supports both human debugging and AI-assisted troubleshooting
  - Timestamps create execution timeline for understanding code flow

**Acceptance Criteria**:
- [ ] Log format includes project-relative file path (dot notation, no .py extension)
- [ ] Log format includes function/method name
- [ ] Log format includes exact line number
- [ ] Log format includes timestamp for execution sequence
- [ ] Format documented with navigation workflow examples
- [ ] Examples demonstrate evidence-based logging patterns

**Rationale**:
When debugging production issues, logs create an "evidence trail" showing exactly
what code executed and in what order. The enhanced format maps each log entry
directly to source code location, enabling developers and AI assistants to:
1. See error in log output
2. Navigate immediately to exact source file and line
3. Load complete function context (not arbitrary line ranges)
4. Understand execution flow from timestamps
5. Identify related code without searching

**Example Log Entry**:
```
ERROR    2025-10-15 10:30:45 examples.04_advanced.token_tracking_example.276: Token tracking example failed: API timeout
```

**Navigation from Log**:
- **File**: `examples.04_advanced` → `examples/04_advanced.py`
- **Function**: `token_tracking_example` → Jump to function definition
- **Line**: `276` → Exact line that logged the error
- **Action**: Load complete function to understand context

**See Also**:
- README.md "Evidence-Based Logging" section
- .github/copilot-instructions.md "Evidence-Based Troubleshooting" workflow
- examples/04_advanced.py for production logging patterns

---

## FR-003: Progressive Examples

### User Story
**As a** developer
**I want** working examples that progressively teach LangChain
**So that** I can learn by doing, from simple to advanced

### Functional Requirements

#### FR-003.1: Example 01 - Basic Usage
- **Description**: Simplest possible LLM usage with three providers
- **Priority**: MUST HAVE
- **Learning Objectives**:
  - Understand basic LLM invocation pattern
  - See how provider switching works
  - Learn configuration setup (load_env_config, get_api_key)
  - Recognize similarity across providers

**Acceptance Criteria**:
- [ ] Works with OpenAI (gpt-5-nano)
- [ ] Works with Anthropic (claude-3-haiku-20240307)
- [ ] Works with Google Gemini (gemini-2.0-flash-lite)
- [ ] Each provider example is separate function
- [ ] All examples use same prompt: "What is machine learning in one sentence?"
- [ ] Graceful handling if API key is missing (skip provider, show warning)
- [ ] Output clearly shows which provider generated each response
- [ ] Demonstrates temperature parameter usage

**Code Structure**:
```python
# Setup (all examples use this pattern)
from langchain_llm import load_env_config, get_api_key, setup_logging
setup_logging()
load_env_config()

# Provider-specific example
def basic_openai_example():
    api_key = get_api_key("openai")
    # NOTE: GPT-5 models (gpt-5-nano, gpt-5-mini, gpt-5) require temperature=1.0
    # Only gpt-5-chat-latest and gpt-4o models support custom temperature values
    llm = ChatOpenAI(model="gpt-5-nano", api_key=api_key, temperature=1.0)
    response = llm.invoke("What is machine learning in one sentence?")
    print(response.content)
```

**OpenAI Temperature Constraint**:
GPT-5 family models (gpt-5-nano, gpt-5-mini, gpt-5) have an API requirement that `temperature` must be set to `1.0`. This is an OpenAI API constraint as of October 2025. Only gpt-5-chat-latest and GPT-4o models support custom temperature values (0.0-2.0).

#### FR-003.2: Example 02 - Streaming Responses
- **Description**: Display tokens as they're generated (streaming)
- **Priority**: MUST HAVE
- **Learning Objectives**:
  - Understand streaming vs batch responses
  - Learn when streaming is appropriate (long responses, user experience)
  - See identical streaming patterns across providers
  - Handle streaming output correctly (flush, end markers)

**Acceptance Criteria**:
- [ ] Demonstrates streaming with all three providers
- [ ] Uses `llm.stream()` method
- [ ] Prints tokens immediately as received (flush=True)
- [ ] Uses longer prompt to show streaming effect clearly
- [ ] Explains use case for streaming in comments
- [ ] Shows how to process chunks (chunk.content)
- [ ] Graceful error handling for streaming failures

**Code Pattern**:
```python
prompt = "Explain the history of artificial intelligence in 3 paragraphs"
for chunk in llm.stream(prompt):
    print(chunk.content, end="", flush=True)
print()  # Newline after stream completes
```

#### FR-003.3: Example 03 - Conversations
- **Description**: Multi-turn conversations with message history
- **Priority**: MUST HAVE
- **Learning Objectives**:
  - Understand message history concept
  - Learn different message types (System, Human, AI)
  - See how context affects responses
  - Build conversational applications

**Acceptance Criteria**:
- [ ] Demonstrates SystemMessage, HumanMessage, AIMessage
- [ ] Shows multi-turn conversation (at least 3 turns)
- [ ] Explains role of system message (personality/instructions)
- [ ] Appends AI responses to history correctly
- [ ] Demonstrates context retention across turns
- [ ] Shows how to initialize empty conversation
- [ ] Works with all three providers

**Code Pattern**:
```python
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

history = [
    SystemMessage(content="You are a helpful AI assistant"),
    HumanMessage(content="What is Python?"),
]

response = llm.invoke(history)
history.append(AIMessage(content=response.content))

# Continue conversation
history.append(HumanMessage(content="What are its main uses?"))
response = llm.invoke(history)
```

#### FR-003.4: Example 04 - Advanced Features
- **Description**: Production features (callbacks, batching, cost tracking)
- **Priority**: MUST HAVE
- **Learning Objectives**:
  - Understand LangChain callbacks system
  - Learn batch processing for efficiency
  - Track token usage and costs
  - Handle errors in production scenarios

**Acceptance Criteria**:
- [ ] Implements custom callback handler (BaseCallbackHandler)
- [ ] Tracks tokens, timing, or costs in callback
- [ ] Demonstrates batch processing with `llm.batch()`
- [ ] Shows error handling patterns
- [ ] Compares batch vs sequential performance
- [ ] Explains when to use each feature
- [ ] Production-ready error messages

**Code Pattern**:
```python
from langchain_core.callbacks import BaseCallbackHandler

class TokenCounterCallback(BaseCallbackHandler):
    def __init__(self):
        self.total_tokens = 0

    def on_llm_end(self, response, **kwargs):
        # Track usage
        pass

callback = TokenCounterCallback()
llm = ChatOpenAI(api_key=api_key, callbacks=[callback])

# Batch processing
prompts = ["Question 1", "Question 2", "Question 3"]
responses = llm.batch(prompts)
```

#### FR-003.5: Dual Format Examples
- **Description**: Provide both Python scripts and Jupyter notebooks
- **Priority**: MUST HAVE
- **Details**:
  - Every example exists as `.py` and `.ipynb`
  - Python scripts for running from CLI
  - Jupyter notebooks for interactive exploration
  - Content should be identical (code and explanations)

**Acceptance Criteria**:
- [ ] 01_basic exists as both .py and .ipynb
- [ ] 02_streaming exists as both .py and .ipynb
- [ ] 03_conversation exists as both .py and .ipynb
- [ ] 04_advanced exists as both .py and .ipynb
- [ ] Notebooks can run cell-by-cell without errors
- [ ] Scripts can run standalone: `python examples/01_basic.py`
- [ ] Both formats produce same output

---

## FR-004: Example Execution Behavior

### User Story
**As a** developer
**I want** examples to run gracefully even if I don't have all API keys
**So that** I can try the examples I can access without errors

### Functional Requirements

#### FR-004.1: Graceful Provider Skipping
- **Description**: Skip provider examples if API key is missing
- **Priority**: MUST HAVE
- **Details**:
  - Try each provider in sequence
  - Catch ConfigError for missing keys
  - Print warning message (not error)
  - Continue with next provider
  - Complete successfully even if all providers fail

**Acceptance Criteria**:
- [ ] Example runs without errors if some keys are missing
- [ ] Warning message clearly states which provider was skipped
- [ ] Warning includes hint about setting up API key
- [ ] At least one provider must run to demonstrate functionality
- [ ] Exit code 0 even if some providers skipped

**Code Pattern**:
```python
try:
    basic_openai_example()
except Exception as e:
    logger.error(f"OpenAI example failed: {e}")
    print(f"[WARNING] OpenAI example skipped: {e}\n")
```

#### FR-004.2: Provider Independence
- **Description**: Examples don't depend on specific provider
- **Priority**: MUST HAVE
- **Details**:
  - All three providers demonstrate same concept
  - User can comment out providers they don't have
  - Learning objectives achievable with any single provider
  - Provider-specific quirks handled transparently

**Acceptance Criteria**:
- [ ] Can run example with only OpenAI key
- [ ] Can run example with only Anthropic key
- [ ] Can run example with only Gemini key
- [ ] Can comment out provider blocks without breaking code
- [ ] Core learning objective clear from any single provider

---

## FR-005: Package Installation

### User Story
**As a** developer or developer
**I want** to install the package easily
**So that** I can import utilities in my own code

### Functional Requirements

#### FR-005.1: Poetry Installation
- **Description**: Install package and dependencies via Poetry
- **Priority**: MUST HAVE
- **Commands**:
  - `poetry install` - Install all dependencies and package
  - `poetry shell` - Activate virtual environment
  - `poetry run <command>` - Run command in Poetry venv

**Acceptance Criteria**:
- [ ] `poetry install` completes without errors
- [ ] Creates virtual environment with correct Python version
- [ ] Installs all dependencies from pyproject.toml
- [ ] Installs langchain_llm package in editable mode
- [ ] Can import: `from langchain_llm import setup_logging`
- [ ] Examples run via `poetry run python examples/01_basic.py`

#### FR-005.2: pip Installation
- **Description**: Install package and dependencies via pip
- **Priority**: MUST HAVE
- **Commands**:
  - `pip install -r requirements.txt` - Install dependencies
  - `pip install -e .` - Install package in editable mode

**Acceptance Criteria**:
- [ ] `pip install -r requirements.txt` completes without errors
- [ ] requirements.txt kept in sync with pyproject.toml
- [ ] `pip install -e .` makes package importable
- [ ] Can import: `from langchain_llm import setup_logging`
- [ ] Examples run via `python examples/01_basic.py`
- [ ] Works in venv created by `python -m venv`

#### FR-005.3: Package Exports
- **Description**: Clean public API from package root
- **Priority**: MUST HAVE
- **Exported Functions**:
  - `setup_logging` - Configure logging
  - `get_logger` - Get named logger
  - `load_env_config` - Load .env file
  - `get_api_key` - Get provider API key

**Acceptance Criteria**:
- [ ] All exported functions importable from package root
- [ ] `from langchain_llm import *` exports only public API
- [ ] `__all__` defined in `__init__.py`
- [ ] No implementation details exposed (internal modules private)
- [ ] Type hints available for all public functions

---

## FR-006: Error Handling

### User Story
**As a** developer
**I want** helpful error messages
**So that** I can fix issues quickly without frustration

### Functional Requirements

#### FR-006.1: ConfigError Messages
- **Description**: Clear, actionable configuration errors
- **Priority**: MUST HAVE
- **Details**:
  - Include provider name in error
  - Include environment variable name
  - Reference .env.example
  - Suggest next action

**Example Error**:
```
ConfigError: API key not found for provider 'openai'.
Please set EADLANGCHAIN_AI_OPENAI_API_KEY in your .env file or environment variables.
See .env.example for template.
```

**Acceptance Criteria**:
- [ ] Error mentions provider name
- [ ] Error includes exact env var name
- [ ] Error references .env.example
- [ ] Error is easy to understand for beginners

#### FR-006.2: LangChain Error Pass-Through
- **Description**: Don't hide LangChain errors
- **Priority**: MUST HAVE
- **Details**:
  - Catch and re-raise with context
  - Add hints for common issues (invalid API key, rate limits)
  - Log error details
  - Preserve original traceback

**Acceptance Criteria**:
- [ ] Invalid API key errors clearly indicate authentication problem
- [ ] Rate limit errors suggest waiting/retrying
- [ ] Network errors suggest checking connection
- [ ] Original LangChain error visible in traceback

---

## Non-Functional Requirements (Summary)

### Performance
- Package import time < 1 second
- Example execution time < 10 seconds (excluding LLM API calls)
- Logging overhead < 5% of total execution time

### Usability
- New user can set up project in < 10 minutes
- Examples are self-explanatory within 5 minutes of reading
- Error messages actionable without external documentation

### Compatibility
- Python 3.10, 3.11, 3.12 support
- Cross-platform (macOS, Linux, Windows)
- Works with Poetry 1.5+ and pip 23+

### Security
- No API keys in code or logs
- No secrets in repository
- All credentials via .env (gitignored)

---

## Related Documents

- **Previous**: [000-overview.md](000-overview.md) - Project vision and goals
- **Next**: [002-technical-requirements.md](002-technical-requirements.md) - Tech stack details
- **See Also**:
  - [003-environment-conventions.md](003-environment-conventions.md) - Configuration patterns
  - [designs/002-configuration-design.md](../designs/002-configuration-design.md) - Config implementation

## Document Metadata

- **Version**: 1.0
- **Status**: Active
- **Owner**: EAD LangChain Template Team
