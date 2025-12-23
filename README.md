# EAD LangChain Template

A comprehensive template for building LLM applications with LangChain, built using [Enforcement-Accelerated Development (EAD)](https://doi.org/10.5281/zenodo.17968797) methodology. This template provides clean project structure, proper configuration management, and progressive examples from basic to advanced usage.

## About EAD

This template demonstrates the EAD methodology in practice. EAD treats errors as enforceable contracts, not afterthoughts - using automated tests as quality gates that run with every build.

- **EAD Whitepaper:** [https://doi.org/10.5281/zenodo.17968797](https://doi.org/10.5281/zenodo.17968797)
- **Author:** [Mark Pace](https://pace.org)

## Features

- **Clean Project Structure**: Professional Python package layout with proper organization
- **LangChain Integration**: Ready-to-use examples for OpenAI, Anthropic, and Google Gemini
- **Custom Logging**: Standardized logging format with detailed context
- **Configuration Management**: Namespaced environment variables to avoid conflicts
- **Progressive Examples**: Learn step-by-step from basic to advanced features
- **Test Infrastructure**: Complete pytest setup with fixtures and TDD examples
- **Dual Package Management**: Support for both Poetry (recommended) and pip

## Quick Start

### Prerequisites

- Python 3.10 or higher
- API keys for at least one provider (OpenAI, Anthropic, or Google Gemini)

### Installation

#### Option 1: Poetry (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/ead-langchain-template.git
cd ead-langchain-template

# Install dependencies
poetry install

# Activate the virtual environment
poetry shell
```

#### Option 2: pip with venv

```bash
# Clone the repository
git clone https://github.com/yourusername/ead-langchain-template.git
cd ead-langchain-template

# Create and activate virtual environment
python -m venv .venv

# Activate (macOS/Linux)
source .venv/bin/activate
# Activate (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

### Configuration

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` and add your API keys:**
   ```bash
   EADLANGCHAIN_AI_OPENAI_API_KEY=your-openai-api-key-here
   EADLANGCHAIN_AI_ANTHROPIC_API_KEY=your-anthropic-api-key-here
   EADLANGCHAIN_AI_GEMINI_API_KEY=your-google-api-key-here
   ```

### Run Your First Example

```bash
# With Poetry
poetry run python examples/01_basic.py

# With pip (ensure venv is activated)
python examples/01_basic.py
```

## Core Concepts

This template teaches four methodologies through hands-on implementation:

### Test-Driven Development (TDD)
Write tests first, then implement to pass them. All utility code (`src/langchain_llm/`) follows RED-GREEN-REFACTOR:
1. **RED**: Write tests (they fail - code doesn't exist)
2. **GREEN**: Implement to pass tests
3. **REFACTOR**: Improve while keeping tests green

### Enforcement Testing
Automated quality gates prevent common issues:
- **Sphinx Docstrings**: `:param`, `:ptype`, `:return`, `:rtype` format required
- **No Emojis**: Professional, cross-platform code

**These tests run automatically** with `pytest` (no separate command needed). The `testpaths = ["tests"]` configuration includes all subdirectories, so enforcement tests are part of the standard test suite. Quality gates are enforced by default.

Run explicitly: `pytest tests/enforcement/` (optional - already runs with main test suite)

### Context Sharding
Documentation and code sized for human review and AI processing. Each task produces ~500 LOC - small enough to review in one sitting, debug in one AI session. Tasks reference only prior tasks, creating sequential dependencies. Navigate: `docs/complete/requirements/` → `designs/` → `tasks/`

### Evidence-Based Logging
Strategic logging creates an evidence trail for debugging. Log at decision points, before/after operations, and on errors. The enhanced format (file.function.line) maps each log entry directly to source code. Example 04 demonstrates logging for production troubleshooting.

## Project Structure

```
ead-langchain-template/
├── src/langchain_llm/       # Core utility package
│   ├── __init__.py
│   ├── config.py            # Configuration and API key management
│   └── logging_config.py    # Custom logging formatter
├── examples/                # Progressive examples (Python + Jupyter)
│   ├── 01_basic.*           # Simple LLM invocation
│   ├── 02_streaming.*       # Streaming responses
│   ├── 03_conversation.*    # Multi-turn conversations
│   └── 04_advanced.*        # Advanced features (callbacks, batching)
├── tests/                   # Test suite with pytest
│   ├── conftest.py          # Shared test fixtures
│   ├── unit/                # Unit tests for core modules
│   │   ├── test_config.py   # Configuration tests
│   │   ├── test_examples.py # Example tests (mocked LLM calls)
│   │   ├── test_interfaces.py  # Protocol/ABC tests
│   │   └── test_logging.py  # Logging tests
│   ├── integration/         # Integration tests
│   │   └── test_sync_notebooks.py  # Notebook sync tests
│   └── enforcement/         # Code quality enforcement
│       ├── test_no_emojis.py  # Emoji detection
│       └── test_sphinx_docstrings.py  # Docstring format
├── .github/
│   └── copilot-instructions.md  # AI coding assistant guidelines
├── pyproject.toml           # Poetry configuration
├── requirements.txt         # pip dependencies
├── .env.example             # Environment variable template
└── README.md                # This file
```

### Why src-layout?

The `src/langchain_llm/` structure prevents accidental imports of uninstalled code.

**Without src-layout:**
```python
# Accidentally imports from working directory, not installed package
import langchain_llm  # May work locally but break in production
```

**With src-layout:**
- Forces proper installation (`pip install -e .` or `poetry install`)
- Tests run against installed version
- Catches packaging issues early
- Matches Python Packaging Authority recommendation

**What goes where:**
- `src/langchain_llm/`: Installable package code only
- `examples/`, `tests/`, `docs/`: Project scaffolding (not installed)

Installation is mandatory - the package won't import until installed. This ensures consistent behavior across development and production.

## Documentation Structure

The `docs/complete/` directory uses **Context Sharding** - work units sized for human and AI review:

```
docs/complete/
├── requirements/    # High-level goals (what/why)
├── designs/        # Architecture (how)
├── tasks/          # Implementation steps (each produces ~500 LOC of code)
└── phases/         # Task groupings
```

**Context Sharding Explained:**

**For Task Documents:**
- Each task describes work that produces ~500 lines of code (implementation + tests)
- Task documents themselves are kept digestible for review (typically <1500 lines)
- This sizing allows tasks to be reviewed in one sitting and implemented in one AI session

**For Other Documentation:**
- Documentation files are sized for optimal readability by both humans and AI
- Target: Under 25,000 tokens and <1500 lines per document
- These limits are model-dependent and based on practical experience with AI context windows
- Right-sizing documentation is part art (readability), part science (token limits)

**How to Navigate:**
1. Requirements → understand goals
2. Designs → architectural approach
3. Tasks → sequential implementation (each references only prior tasks)

**Why This Works:**
- **For humans**: Each document = digestible in one review session
- **For AI**: Complete context available without hitting token limits or processing degradation
- **No forward dependencies**: Task 007 never references Task 008
- **Prevents context overload**: AI assistants can process task + dependencies in single session

Context Sharding ensures work units fit human attention spans and AI token limits.

## Examples

The `examples/` directory contains progressive tutorials available in both Python scripts and Jupyter notebooks. All examples have comprehensive test coverage (>80%) demonstrating how to test LLM application code without making actual API calls.

### 01: Basic Usage
Learn the simplest way to use LangChain with different providers.

```python
from langchain_openai import ChatOpenAI
from langchain_llm import get_api_key, load_env_config, setup_logging

setup_logging()
load_env_config()

llm = ChatOpenAI(model="gpt-5-nano", api_key=get_api_key("openai"))
response = llm.invoke("What is machine learning?")
print(response.content)
```

**Key concepts:** Configuration, basic invocation, provider switching

### 02: Streaming Responses
See responses token-by-token as they're generated.

```python
for chunk in llm.stream("Explain streaming in LLMs"):
    print(chunk.content, end="", flush=True)
```

**Key concepts:** Real-time responses, streaming API

### 03: Conversations
Build multi-turn conversations with message history.

```python
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

history = [
    SystemMessage(content="You are a helpful assistant"),
    HumanMessage(content="What is Python?"),
]
response = llm.invoke(history)
history.append(AIMessage(content=response.content))
```

**Key concepts:** Message history, system prompts, conversation context

### 04: Advanced Features
Production-ready features for serious applications.

```python
# Token tracking with callbacks
from langchain_core.callbacks import BaseCallbackHandler

class TokenCounterCallback(BaseCallbackHandler):
    def on_llm_end(self, response, **kwargs):
        # Track usage, costs, etc.
        pass

llm = ChatOpenAI(api_key=api_key, callbacks=[TokenCounterCallback()])
```

**Key concepts:** Callbacks, cost tracking, batch processing, error handling

## Environment Variables

This project uses a **namespaced environment variable convention** to avoid conflicts:

```
EADLANGCHAIN_<TYPE>_<KEY>
```

### Examples

```bash
# AI Provider Keys
EADLANGCHAIN_AI_OPENAI_API_KEY=sk-...
EADLANGCHAIN_AI_ANTHROPIC_API_KEY=sk-ant-...
EADLANGCHAIN_AI_GEMINI_API_KEY=...

# Logging Configuration
EADLANGCHAIN_LOG_LEVEL=INFO
EADLANGCHAIN_LOG_FILE=logs/app.log

# Optional: Default Models (Most cost-effective as of October 2025)
EADLANGCHAIN_AI_OPENAI_MODEL=gpt-5-nano
EADLANGCHAIN_AI_ANTHROPIC_MODEL=claude-3-haiku-20240307
EADLANGCHAIN_AI_GEMINI_MODEL=gemini-2.0-flash-lite
```

### Why Namespaced Variables?

- **Prevents conflicts** with system-wide or other project variables
- **Clear ownership** - immediately obvious which project owns the variable
- **Best practice** for production applications
- **Explicit configuration** - no hidden dependencies on default env vars

## Development

### Running Tests

This project follows Test-Driven Development (TDD) practices. All code (utilities and examples) has >80% test coverage.

```bash
# Run all tests (utilities + examples + enforcement)
poetry run pytest
# OR (with activated venv)
pytest

# Run with verbose output
pytest -v

# Run specific test files
pytest tests/unit/test_config.py      # Config module tests
pytest tests/unit/test_examples.py    # Example tests (mocked LLM calls)
pytest tests/enforcement/             # Quality enforcement

# Run with coverage
pytest --cov=src/langchain_llm        # Utility coverage
pytest --cov=examples                  # Example coverage
pytest --cov=src/langchain_llm --cov=examples  # Combined coverage
```

**Example Test Coverage:**
- 01_basic.py: ~94%
- 02_streaming.py: ~87%
- 03_conversation.py: ~84%
- 04_advanced.py: ~92%

Tests use mocked LLM responses to avoid API calls, demonstrating best practices for testing code that depends on external services.

### Code Quality

The project uses Ruff for linting and formatting (130 character line length).

```bash
# Check for issues
poetry run ruff check .

# Auto-fix issues
poetry run ruff check --fix .

# Format code
poetry run ruff format .
```

### Test-Driven Development (TDD)

This project demonstrates TDD. All utility code was built test-first.

**The TDD Cycle:**

**1. RED - Write Failing Test**
```python
# tests/unit/test_new_feature.py
def test_new_feature():
    result = new_feature("input")
    assert result == "expected"
```
Run test - MUST fail (ImportError/test failure):
```bash
pytest tests/unit/test_new_feature.py
```

**2. GREEN - Minimal Implementation**
```python
# src/langchain_llm/module.py
def new_feature(input: str) -> str:
    return "expected"  # Just enough to pass
```
Run test - MUST pass:
```bash
pytest tests/unit/test_new_feature.py  # ✓ PASSED
```

**3. REFACTOR - Improve Quality**
- Add Sphinx docstrings
- Improve error handling
- Run tests after EACH change (stay green)

**4. Validate**
```bash
pytest tests/enforcement/  # Docstrings, no emojis
ruff check src/           # Code quality
```

**See Full Example:** `docs/complete/tasks/task-006-config-module.md` walks through complete TDD cycle.

## Using the Package

Import utilities from the package in your code:

```python
from langchain_llm import (
    setup_logging,      # Configure logging
    get_logger,         # Get a logger instance
    load_env_config,    # Load environment variables
    get_api_key,        # Get API keys safely
)

# Setup
setup_logging(level="INFO")
load_env_config()
logger = get_logger(__name__)

# Use API keys
openai_key = get_api_key("openai")
anthropic_key = get_api_key("anthropic")
gemini_key = get_api_key("gemini")
```

## Evidence-Based Logging

Logging creates an evidence trail for understanding what happened when code runs. This template demonstrates strategic logging patterns for production applications.

### Strategic Logging Points

Log at:
- **Decision points**: "Choosing provider: openai"
- **Before operations**: "Starting batch processing of 10 items"
- **After operations**: "Batch complete: 10/10 successful"
- **Errors**: "API call failed: rate limit exceeded"

### Why Evidence-Based Logging Matters

Logs create a timeline of execution. When errors occur, logs show what the code was doing immediately before failure. The enhanced log format (file.function.line) maps each log entry directly to source code, enabling fast navigation to the exact location that generated each message.

**See it in action:** `examples/04_advanced.py` uses logging throughout to demonstrate production debugging patterns.

## Logging

The template includes a custom logging system with detailed formatting. Examples use both `print()` for user-facing output and `logger.*()` for diagnostic information. This demonstrates the dual approach recommended for production applications.

### Basic Logging Setup

```python
from langchain_llm import setup_logging, get_logger

# Set up logging with desired level
setup_logging(level="INFO")  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL

# Get a logger for your module
logger = get_logger(__name__)

# Use it
logger.info("Application started")
logger.debug("Detailed debug information")
logger.warning("Something to be aware of")
logger.error("An error occurred")
```

### Custom Log Format

Enhanced format provides precise navigation to code:

```
INFO     2025-10-15 10:30:45 examples.04_advanced.token_tracking_example.92: Running token tracking example
```

**Format:**
- `INFO`: Level (8 chars, aligned)
- `2025-10-15 10:30:45`: Timestamp
- `examples.04_advanced`: Relative path (dot notation, no `.py`)
- `token_tracking_example`: Function name
- `92`: Line number
- Message content

**Why This Format:**
- **Human navigation**: `examples.04_advanced` → `examples/04_advanced.py`
- **AI troubleshooting**: File path + line number = exact code location
- **Class context**: Shows class name when logging from methods
- **Execution sequence**: Timestamps reveal call order

**For AI Debugging:** Logs provide direct paths to source code. No searching - each log line maps to exact file:line. Load complete functions, not arbitrary line ranges. See `.github/copilot-instructions.md` "Evidence-Based Troubleshooting" for AI workflow.

### Configuration via Environment Variables

Control logging through environment variables:

```bash
# .env file
EADLANGCHAIN_LOG_LEVEL=DEBUG          # Set log level
EADLANGCHAIN_LOG_FILE=logs/app.log   # Optional: write logs to file
```

### Using Logging in Examples

Examples use both approaches:
- **`print()`**: User-facing output (results, status messages)
- **`logger.info()`, `logger.error()`, etc.**: Diagnostic logging (debugging, troubleshooting)

To see diagnostic logging output, run with DEBUG level:

```bash
# Set log level before running
export EADLANGCHAIN_LOG_LEVEL=DEBUG
poetry run python examples/01_basic.py
```

This will show diagnostic log messages alongside the printed output, demonstrating how both work together.

## Jupyter Notebooks

All examples are available as Jupyter notebooks in the `examples/` directory.

### Using with Poetry

```bash
# Make sure ipykernel is installed
poetry install

# Launch Jupyter
poetry run jupyter notebook examples/
```

### Using with pip

```bash
# Install jupyter (if not already installed)
pip install jupyter

# Launch Jupyter
jupyter notebook examples/
```

## Adding Dependencies

### With Poetry

```bash
# Add a runtime dependency
poetry add <package-name>

# Add a development dependency
poetry add --group dev <package-name>

# Update requirements.txt for pip users
poetry export -f requirements.txt -o requirements.txt --without-hashes
```

### With pip

```bash
# Install a new package
pip install <package-name>

# Update requirements.txt
pip freeze > requirements.txt
```

## Common Tasks

### Syncing Python Examples to Notebooks

Examples are maintained as `.py` files and converted to `.ipynb` for Jupyter:

```bash
# Install jupytext (one-time setup)
pip install jupytext
# OR
poetry add --group dev jupytext

# Sync all examples (.py → .ipynb)
python scripts/sync_notebooks.py

# Check sync status without converting
python scripts/sync_notebooks.py --check
```

**Workflow:**
1. Edit the `.py` file (easier to test/lint)
2. Run sync script to generate `.ipynb`
3. Test both versions before committing

**Troubleshooting:**

**Problem:** Script fails with "jupytext not found"

**Solution:**
```bash
# Install jupytext
pip install jupytext
# OR with Poetry
poetry add --group dev jupytext
```

**Problem:** Notebook appears out of sync or has conflicts

**Solution:**
- The `.py` file is always the source of truth
- Manual edits to `.ipynb` files will be overwritten by sync
- If you edited the notebook directly, copy changes back to the `.py` file first
- Run `python scripts/sync_notebooks.py` to regenerate `.ipynb` from `.py`

**Problem:** Sync script shows errors about cell format

**Solution:**
- Ensure the `.py` file is valid Python (run `python examples/XX_name.py` to test)
- Check that the file has proper docstring at the top
- Jupytext requires standard Python formatting (no special syntax)

### Adding a New Example

1. Create `examples/0X_name.py` (Python script)
2. Run `python scripts/sync_notebooks.py` to generate `.ipynb`
3. Follow the progressive complexity pattern
4. Include error handling and informative output

### Adding a New Utility Function

1. Add the function to appropriate module in `src/langchain_llm/`
2. Write tests in `tests/unit/test_<module>.py`
3. Export in `src/langchain_llm/__init__.py`
4. Document with docstrings

### Adding a New Provider

LangChain supports many providers out of the box:

1. Install the provider package:
   ```bash
   poetry add langchain-<provider>
   ```

2. Add API key to `.env.example`:
   ```bash
   EADLANGCHAIN_AI_<PROVIDER>_API_KEY=your-key-here
   ```

3. Add helper in `src/langchain_llm/config.py`
4. Create example in `examples/`

## Troubleshooting

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'langchain_llm'`

**Solution:**
```bash
# With Poetry
poetry install

# With pip
pip install -e .
```

### API Key Errors

**Problem:** `ConfigError: API key not found for provider 'openai'`

**Solution:**
1. Ensure `.env` file exists (copy from `.env.example`)
2. Check that your API key is set: `EADLANGCHAIN_AI_OPENAI_API_KEY=sk-...`
3. Verify `load_env_config()` is called before using API keys

### Virtual Environment Issues

**Problem:** Commands not found or using wrong Python version

**Solution:**
```bash
# Poetry - ensure shell is activated
poetry shell

# pip - ensure venv is activated
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### Common LLM API Errors

**Problem:** `AuthenticationError` when running examples

**Solution:**
1. Check that your API key is correctly set in `.env`
2. Verify the API key format matches the provider's requirements:
   - OpenAI: starts with `sk-proj-` or `sk-`
   - Anthropic: starts with `sk-ant-`
   - Google: alphanumeric string
3. Ensure `load_env_config()` is called before using API keys

**Problem:** `RateLimitError` when calling LLM

**Solution:**
1. You've exceeded your API quota or rate limit
2. Wait for the rate limit window to reset (usually 1 minute)
3. Check your provider's dashboard for usage limits
4. Consider upgrading your API plan if you need higher limits

**Problem:** `APIConnectionError` or network timeout

**Solution:**
1. Check your internet connection
2. Verify you can reach the provider's API endpoint
3. Check if the provider is experiencing an outage (status pages):
   - OpenAI: https://status.openai.com/
   - Anthropic: https://status.anthropic.com/
   - Google: https://status.cloud.google.com/

**Problem:** `InvalidRequestError` or validation errors

**Solution:**
1. Check that your prompt is not empty
2. Verify model name is correct and available for your account
3. Check if you're exceeding token limits for the model
4. Review the error message for specific parameter issues

### LangChain API Changes

**Problem:** Examples fail after updating dependencies with `AttributeError` or `ImportError`

**Solution:**

LangChain APIs evolve frequently. If examples break after updates:

1. **Check the changelog:**
   - Visit: https://python.langchain.com/docs/changelog
   - Look for breaking changes in your version range

2. **Pin working versions** (temporary fix):
   ```bash
   # In pyproject.toml, use exact versions:
   langchain-openai = "0.2.0"  # Instead of "^0.2.0"

   # Then reinstall:
   poetry install
   ```

3. **Update examples** (permanent fix):
   - Read migration guides in changelog
   - Update import statements and API calls
   - Test all examples after changes
   - Update model names if deprecated

4. **Check provider-specific docs:**
   - OpenAI: https://platform.openai.com/docs
   - Anthropic: https://docs.anthropic.com/
   - Google: https://ai.google.dev/docs

## Resources

- **LangChain Documentation:** https://python.langchain.com/
- **OpenAI API Docs:** https://platform.openai.com/docs
- **Anthropic API Docs:** https://docs.anthropic.com/
- **Google Gemini Docs:** https://ai.google.dev/docs
- **Poetry Documentation:** https://python-poetry.org/docs/
- **pytest Documentation:** https://docs.pytest.org/

## Contributing

When contributing:

1. Follow the TDD workflow
2. Run tests and linting before committing
3. Update documentation for new features
4. Follow the environment variable naming convention (`EADLANGCHAIN_<TYPE>_<KEY>`)
5. Keep examples simple and progressive
6. Review `.github/copilot-instructions.md` for coding guidelines

## License

MIT

## Support

- Check the examples in `examples/` directory
- Review `.github/copilot-instructions.md` for detailed guidance
- Read the [EAD Whitepaper](https://doi.org/10.5281/zenodo.17968797) for methodology background

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions

---

**Happy coding!**
