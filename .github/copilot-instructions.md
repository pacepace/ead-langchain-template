# GitHub Copilot Instructions for EAD LangChain Template

This file provides guidance to GitHub Copilot (and other AI coding assistants) when working with this project.

## Project Overview

This is a template for building LLM applications using LangChain, built with Enforcement-Accelerated Development (EAD) methodology. The template provides:
- Clean project structure with proper packaging
- Standardized logging with custom formatting
- Configuration management for API keys
- Progressive examples from basic to advanced usage
- Test infrastructure with pytest

## EAD (Enforcement-Accelerated Development)

**Three Pillars:**
1. **Context Sharding** - ~500 LOC per task, fits in one AI context window
2. **Enforcement Tests** - AST-based, verify patterns not behavior, <15s, catch drift early
3. **Evidence-Based Debugging** - Logs have file:line:function. No guessing.

**Task Files** (`docs/complete/tasks/`):
- Self-contained, subagent finishes without questions
- Name = WHAT it does (`ConfigModule` not `Phase1Task1`)
- TDD: test code in task, written first
- Sections: Objective, Success Criteria, Research (file:line refs), Implementation, Test Plan, Files to Modify, Verification

## Environment Variables Convention

**IMPORTANT:** All environment variables in this project follow a strict naming convention:

```
EADLANGCHAIN_<TYPE>_<KEY>
```

**Structure:**
- **PREFIX:** `EADLANGCHAIN` - Identifies this project, prevents conflicts with other applications
- **TYPE:** Category of the setting (AI, LOG, DB, etc.)
- **KEY:** Specific configuration item

**Examples:**
```bash
EADLANGCHAIN_AI_OPENAI_API_KEY       # AI provider key
EADLANGCHAIN_AI_ANTHROPIC_API_KEY    # AI provider key
EADLANGCHAIN_AI_GEMINI_API_KEY       # AI provider key
EADLANGCHAIN_LOG_LEVEL               # Logging configuration
EADLANGCHAIN_LOG_FILE                # Logging configuration
EADLANGCHAIN_DB_CONNECTION_STRING    # Database setting (example)
```

**Why?**
- Prevents conflicts with system-wide or other project environment variables
- Makes it clear which variables belong to this project
- Follows enterprise best practices for environment variable management

**When adding new environment variables:**
1. Always use the `EADLANGCHAIN_<TYPE>_<KEY>` pattern
2. Update `.env.example` with the new variable and documentation
3. Update `README.md` if it's a user-facing configuration
4. Add helper functions in `src/langchain_llm/config.py` if needed

## Package Management

This project supports both Poetry (recommended) and pip for dependency management.

### Using Poetry (Recommended)

Poetry is the primary package manager for this project.

**Installation:**
```bash
# Install dependencies
poetry install

# Activate the virtual environment
poetry shell

# Add a new dependency
poetry add <package-name>

# Add a dev dependency
poetry add --group dev <package-name>

# Run a command in the poetry environment
poetry run python examples/01_basic.py
poetry run pytest
```

**Important Poetry Commands:**
- `poetry install` - Install all dependencies
- `poetry shell` - Activate the virtual environment
- `poetry add` - Add a dependency
- `poetry update` - Update dependencies
- `poetry export -f requirements.txt -o requirements.txt` - Export requirements.txt

### Using pip with venv

For users who prefer pip or can't use Poetry:

**Setup:**
```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package in editable mode
pip install -e .
```

**Important pip Commands:**
- `pip install -r requirements.txt` - Install dependencies
- `pip install -e .` - Install package in development mode
- `pip freeze > requirements.txt` - Update requirements (be careful!)

**Note:** When suggesting commands to users:
- Prefer Poetry commands (`poetry run pytest`) but provide pip equivalents
- Always mention virtual environment activation for pip users
- Remind users to activate their venv before running commands

## Test-Driven Development (TDD)

This project follows TDD methodology. **When adding new features:**

### TDD Workflow

1. **Write the Test First (Red)**
   ```python
   # tests/test_new_feature.py
   def test_new_feature():
       result = new_feature()
       assert result == expected_value
   ```

2. **Run the Test and See it Fail (Red)**
   ```bash
   poetry run pytest tests/unit/test_new_feature.py -v
   # OR
   pytest tests/unit/test_new_feature.py -v
   ```
   The test should fail because the feature doesn't exist yet.

3. **Write Minimal Code to Pass the Test (Green)**
   ```python
   # src/langchain_llm/new_module.py
   def new_feature():
       return expected_value
   ```

4. **Run the Test Again (Green)**
   ```bash
   poetry run pytest tests/unit/test_new_feature.py -v
   ```
   The test should now pass.

5. **Refactor (Refactor)**
   Clean up the code, improve structure, add documentation.
   Tests should still pass after refactoring.

### Testing Guidelines

**When writing tests:**
- Use descriptive test names: `test_get_api_key_returns_correct_value`
- Use pytest fixtures from `tests/conftest.py` to reduce duplication
- Test both success and failure cases
- Test edge cases (empty strings, None values, invalid inputs)
- Use `pytest.raises` for testing exceptions
- Group related tests in classes with descriptive names
- **Target code coverage: >80%** for all utility modules in `src/langchain_llm/`

**Example test structure:**
```python
class TestConfigModule:
    """Tests for configuration management."""

    def test_valid_input(self, mock_env_vars):
        """Test with valid input."""
        result = function_under_test("valid")
        assert result == expected

    def test_invalid_input(self):
        """Test with invalid input raises appropriate error."""
        with pytest.raises(ValueError):
            function_under_test("invalid")

    def test_edge_case_empty_string(self):
        """Test edge case with empty string."""
        result = function_under_test("")
        assert result is None
```

**Running tests:**
```bash
# Run all tests
poetry run pytest
# OR
pytest

# Run specific test file
poetry run pytest tests/unit/test_config.py

# Run with verbose output
poetry run pytest -v

# Run with coverage (target >80%)
poetry run pytest --cov=src/langchain_llm --cov-report=term

# Run specific test
poetry run pytest tests/unit/test_config.py::TestConfigModule::test_valid_input
```

## LangChain Usage

This project uses LangChain for LLM interactions. **Important guidelines:**

### Always Use LangChain's Built-in Features

**DON'T reinvent the wheel:**
```python
# ❌ WRONG - Custom provider wrapper
class MyCustomOpenAIWrapper:
    def call(self, prompt):
        # Custom implementation
        pass
```

**DO use LangChain directly:**
```python
# ✅ CORRECT - Use LangChain's providers
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(api_key=get_api_key("openai"))
response = llm.invoke("prompt")
```

### API Key Management

**Always use the config helpers:**
```python
# ✅ CORRECT
from langchain_llm import get_api_key, load_env_config

load_env_config()
api_key = get_api_key("openai")
llm = ChatOpenAI(api_key=api_key)
```

**DON'T use provider's default env vars:**
```python
# ❌ WRONG - Uses OPENAI_API_KEY
llm = ChatOpenAI()  # Will look for OPENAI_API_KEY
```

We use custom env var names (`EADLANGCHAIN_AI_OPENAI_API_KEY`) to avoid conflicts.

### Message History for Conversations

```python
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

history = [
    SystemMessage(content="You are a helpful assistant"),
    HumanMessage(content="Hello!"),
]

response = llm.invoke(history)
history.append(AIMessage(content=response.content))
```

### Callbacks for Advanced Features

Use LangChain callbacks for tracking, logging, and monitoring:
```python
from langchain_core.callbacks import BaseCallbackHandler

class CustomCallback(BaseCallbackHandler):
    def on_llm_end(self, response, **kwargs):
        # Handle LLM completion
        pass

llm = ChatOpenAI(api_key=api_key, callbacks=[CustomCallback()])
```

## Code Style

This project uses Ruff for linting and formatting.

### Ruff Configuration

- **Line length:** 130 characters
- **Target:** Python 3.10+
- **Format:** Double quotes, spaces for indentation

### Running Ruff

```bash
# Check for issues
poetry run ruff check .

# Fix auto-fixable issues
poetry run ruff check --fix .

# Format code
poetry run ruff format .

# Check and format
poetry run ruff check --fix . && poetry run ruff format .
```

### Code Style Guidelines

**Imports:**
```python
# Standard library
import os
from pathlib import Path

# Third-party
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Local
from langchain_llm import get_api_key, get_logger
```

**Docstrings - MANDATORY Sphinx Format:**

This project **REQUIRES** Sphinx-style docstrings. Google-style (Args:, Returns:) and NumPy-style are **NOT ALLOWED** and will cause enforcement tests to fail.

**Key Requirements:**
- Use `:param:` and `:ptype:` for parameters (NOT `:type:`)
- Use `:return:` and `:rtype:` for return values
- Use modern type syntax: `str | None` not `Optional[str]`
- Capitalization: Follow standard PEP 257 (first letter capitalized for sentences)

**Required Format:**
```python
def function_name(param1: str, param2: int | None = None) -> str | None:
    """
    Brief description of function.

    Longer description if needed. Can span multiple paragraphs
    and include additional context about the function's purpose.

    :param param1: Description of param1
    :ptype param1: str
    :param param2: Description of param2
    :ptype param2: int | None
    :return: Description of return value
    :rtype: str | None
    :raises ValueError: When param1 is invalid
    :raises KeyError: When required key is missing

    Example usage::

        result = function_name("test", 42)
        print(result)
    """
    pass
```

**Class Docstrings:**
```python
class MyClass:
    """
    Brief description of class.

    Longer description of the class purpose and behavior.

    :param name: Name parameter
    :ptype name: str
    :param value: Value parameter
    :ptype value: int
    """

    def __init__(self, name: str, value: int):
        """
        Initialize MyClass.

        :param name: Name parameter
        :ptype name: str
        :param value: Value parameter
        :ptype value: int
        """
        self.name = name
        self.value = value

    def process(self, data: str) -> bool:
        """
        Process the data.

        :param data: Data to process
        :ptype data: str
        :return: True if successful
        :rtype: bool
        :raises ValueError: If data is empty
        """
        pass
```

**Module Docstrings:**
```python
"""
Module for handling configuration.

This module provides utilities for loading and managing
configuration from environment variables.
"""
```

**Important Sphinx Directives:**
- `:param name:` - Parameter description (required for each parameter)
- `:ptype name: type` - Parameter type (required for each parameter)
- `:return:` - Return value description (required if function returns)
- `:rtype: type` - Return type (required if function returns)
- `:raises ExceptionType:` - Exception that may be raised
- `:Example:` or `Example::` - Usage examples

**What NOT to use:**
```python
# ❌ WRONG - Google-style (will fail tests)
def bad_function(x):
    """
    Args:
        x: Some parameter

    Returns:
        Some value
    """
    pass

# ❌ WRONG - NumPy-style (will fail tests)
def bad_function(x):
    """
    Parameters
    ----------
    x : int
        Some parameter

    Returns
    -------
    int
        Some value
    """
    pass
```

**Enforcement:**
- All Python files are scanned by `tests/enforcement/test_sphinx_docstrings.py`
- Tests will fail if non-Sphinx docstrings are found
- Run `pytest tests/enforcement/` to check compliance

**Type Annotations (Python 3.10+ syntax):**
```python
# In code AND docstrings - use modern built-in types
def get_config(name: str, default: str | None = None) -> list[dict[str, int]]:
    """
    :param name: config name
    :ptype name: str
    :param default: default value
    :ptype default: str | None
    :return: config data
    :rtype: list[dict[str, int]]
    """
```
**Rule**: `str | None` not `Optional[str]`, `list` not `List`, `dict` not `Dict`, `tuple` not `Tuple`

## Project Structure

```
ead-langchain-template/
├── src/langchain_llm/       # Main package (thin utility layer)
│   ├── __init__.py
│   ├── config.py            # Environment variable management
│   └── logging_config.py    # Custom logging formatter
├── examples/                # Progressive examples (py + ipynb)
│   ├── 01_basic.*           # Simple usage
│   ├── 02_streaming.*       # Streaming responses
│   ├── 03_conversation.*    # Message history
│   └── 04_advanced.*        # Advanced features
├── tests/                   # Test suite
│   ├── conftest.py          # Pytest fixtures
│   ├── test_config.py
│   └── test_logging.py
├── .github/                 # This file!
├── pyproject.toml          # Poetry configuration
├── requirements.txt        # Pip dependencies
└── .env.example            # Environment variable template
```

**When adding new files:**
- Python modules go in `src/langchain_llm/`
- Examples go in `examples/` (both .py and .ipynb)
- Tests go in `tests/` with `test_` prefix
- Keep the package minimal - add utilities, not features

### Why We Use Interfaces (Protocols & ABCs)

This project uses `interfaces.py` to define contracts via Protocols and ABCs.

**Benefits for Testing**:
- Mock implementations for unit tests
- Dependency injection without complex frameworks
- Clear separation between contract and implementation

**Benefits for AI-Assisted Coding**:
- Interfaces enable AI assistants to understand contracts without reading implementations, making code navigation and suggestion generation more accurate. Clear boundaries between what and how prevent AI from suggesting changes that break abstractions.

**When to use**:
- Protocol: For configuration providers, data access (structural typing)
- ABC: For formatters, transformers that inherit from base classes (nominal typing)

## Common Patterns

### Adding a New Utility Function

1. **Write the test first:**
   ```python
   # tests/test_utils.py
   def test_new_utility():
       result = new_utility(input)
       assert result == expected
   ```

2. **Implement the function:**
   ```python
   # src/langchain_llm/utils.py
   def new_utility(param: str) -> str:
       """Brief description."""
       return processed_result
   ```

3. **Export in __init__.py:**
   ```python
   # src/langchain_llm/__init__.py
   from langchain_llm.utils import new_utility

   __all__ = ["setup_logging", "get_logger", "new_utility"]
   ```

### Adding a New Example

1. Create Python script: `examples/0X_name.py`
2. Run `poetry run python scripts/sync_notebooks.py` to generate `.ipynb`
3. Follow the progressive complexity pattern (basic → advanced)
4. Include error handling and informative output
5. Add section to README.md

### Syncing Notebooks from Python Files

```bash
poetry run python scripts/sync_notebooks.py
```

Converts `.py` example files to `.ipynb` notebooks. Source of truth is always the `.py` file.

### Adding a New Environment Variable

1. Add to `.env.example` with documentation
2. Follow `EADLANGCHAIN_<TYPE>_<KEY>` pattern
3. Add helper in `src/langchain_llm/config.py` if needed
4. Add test in `tests/unit/test_config.py`
5. Update README.md

## Common Pitfalls

**Don't:**
- Use generic env var names (`OPENAI_API_KEY`)
- Create custom LLM wrappers (use LangChain)
- Skip tests ("I'll add them later")
- Commit API keys or secrets
- Import from examples in package code
- **Use emoji characters in code** (will fail enforcement tests)
- **Use Google-style or NumPy-style docstrings** (Sphinx only)

**Do:**
- Use `EADLANGCHAIN_` prefixed env vars
- Use LangChain's built-in features
- Write tests first (TDD)
- Keep package code minimal and reusable
- **Document all functions with Sphinx-style docstrings**
- Run `pytest tests/enforcement/` before committing

## Code Content Guidelines

**IMPORTANT**: Code, comments, and docstrings must NOT reference phases, tasks, or project management scaffolding.

**Don't use**: "Phase 02", "Task 005", "step 3", "sprint", "milestone"
**Do use**: "configuration module", "logging system", "API key management"

**Bad**:
```python
# Phase 02: Configuration implementation
# TODO: Task 015
```

**Good**:
```python
# Configuration management using environment variables
# TODO: Implement advanced callback features
```

**Why**: Code is permanent, project organization is temporary

## Evidence-Based Troubleshooting

When debugging issues, use the enhanced logging format to locate problems efficiently:

**Log Format Breakdown:**
```
INFO     2025-10-15 10:30:45 examples.04_advanced.token_tracking_example.92: Running token tracking example
```

**Navigation Strategy:**
1. **File location**: `examples.04_advanced` → `examples/04_advanced.py`
2. **Function**: `token_tracking_example` → Go to function definition
3. **Line**: `92` → Exact line that logged the message
4. **Context**: Timestamps show sequence of events

**Troubleshooting Workflow:**
1. Reproduce issue
2. Check logs for error/warning messages
3. Use file path + line number to locate source
4. Read the complete function/method where error occurred
5. Identify related methods (functions this one calls, or that call this one)
6. Check prior logs to understand execution flow before error
7. Load relevant function definitions into context

**Why This Works:**
- Relative paths prevent navigation confusion
- Line numbers eliminate guessing
- Function names show call stack context
- Timestamps reveal execution order
- Loading complete functions (not arbitrary line ranges) provides actual context
- Focused loading prevents token limit issues

Use logging output as a map: each log line points to the exact function containing the issue.

## Getting Help

- Check `README.md` for setup instructions
- Review examples in `examples/` directory
- Check LangChain documentation: https://python.langchain.com/
- EAD Whitepaper: https://doi.org/10.5281/zenodo.17968797

For contributors:
- Review this file before making changes
- Follow TDD methodology
- Run tests and linting before committing
- Keep the template minimal and focused
