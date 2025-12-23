# Task 008: Create Package Exports and Configure Ruff

## Task Context

**Phase**: 02 - Core Interfaces & Utilities
**Sequence**: Eighth task (completes Phase 02)
**Complexity**: Low-Medium
**Output**: ~100 LOC (package __init__.py + pyproject.toml additions)

### Why This Task Exists

Users need:
- Clean imports (`from langchain_llm import setup_logging`)
- Code quality enforcement (consistent style)
- Clear public API definition

This task:
- Exports public API from package root
- Configures Ruff for linting and formatting
- Finalizes Phase 02 core utilities

### Where This Fits

```
Task 007 → Task 008 (YOU ARE HERE) → Task 009 → ...
Logging    Package Exports + Ruff     Basic Examples
Module
```

Completes Phase 02 (Core Interfaces & Utilities).

---

## Prerequisites

### Completed Tasks

- [x] **Task 006**: Config module (interfaces, config.py)
- [x] **Task 007**: Logging module (logging_config.py)

### Required Knowledge

**Python Packaging**:
- `__init__.py` purpose
- `__all__` list
- Public vs private API
- Import mechanisms

**Code Quality**:
- What linters do
- What formatters do
- Ruff capabilities

---

## Research Required

### Code from Prior Tasks

**Study from Task 006**:
- `src/langchain_llm/config.py`: Public functions to export (get_api_key, load_env_config, etc.)
- `src/langchain_llm/config.py`: ConfigError exception to export
- Purpose: Know what to include in __all__

**Study from Task 007**:
- `src/langchain_llm/logging_config.py`: Public functions to export (setup_logging, get_logger)
- Purpose: Complete the export list

**Study from Task 006-007**:
- Both modules: Observe code style currently used (line length, quotes, formatting)
- Purpose: Configure Ruff to match existing style

### No Forward References

This task doesn't create new implementation code - it only exports existing code from tasks 006-007.

### External Documentation

**Ruff**:
- https://docs.astral.sh/ruff/
- Configuration options
- Rule selection
- Format settings

**Python __all__**:
- https://docs.python.org/3/tutorial/modules.html#importing-from-a-package
- What `from package import *` does
- How `__all__` controls exports

---

## Task Description

### Objective

Create clean package exports in `__init__.py` and configure Ruff for code quality enforcement.

### Requirements

#### 1. Create src/langchain_llm/__init__.py

**Complete file contents**:
```python
"""
LangChain LLM Utilities for EAD LangChain Template.

A minimal utility package providing:
- Custom logging with standardized format
- Configuration helpers for managing API keys
- Clean patterns for working with LangChain providers

Example usage::

    from langchain_llm import setup_logging, get_logger, load_env_config, get_api_key, ConfigError

    # Setup
    setup_logging(level="INFO")
    load_env_config()

    # Use
    logger = get_logger(__name__)
    api_key = get_api_key("openai")
"""

from langchain_llm.config import ConfigError, get_api_key, load_env_config
from langchain_llm.logging_config import get_logger, setup_logging

__version__ = "0.1.0"

__all__ = [
    "setup_logging",
    "get_logger",
    "load_env_config",
    "get_api_key",
    "ConfigError",
]
```

**What to Export** (from tasks 006-007):

From `config.py` (task 006):
- `load_env_config` - Function to load .env file
- `get_api_key` - Function to get API key for provider
- `ConfigError` - Exception class for config errors

From `logging_config.py` (task 007):
- `setup_logging` - Function to configure logging
- `get_logger` - Function to get named logger

**What NOT to Export**:
- `get_all_api_keys()` - Internal utility
- `validate_provider()` - Internal utility
- `get_model_name()` - Internal utility
- `EnvConfigProvider` - Implementation detail
- `CustomFormatter` - Implementation detail
- Interfaces (ConfigProvider, LogFormatter) - Advanced usage only

**Requirements**:
- Module docstring with usage example
- Import only public functions
- Define `__version__` (start with "0.1.0")
- Define `__all__` list (controls `from langchain_llm import *`)
- Keep it simple (~30-40 lines total)

#### 2. Add Ruff Configuration to pyproject.toml

**Add these three sections to `pyproject.toml`**:

```toml
[tool.ruff]
line-length = 130
target-version = "py310"
exclude = [
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".venv",
    "venv",
    "*.ipynb_checkpoints",
]

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "F",   # pyflakes
    "I",   # isort (import sorting)
    "N",   # pep8-naming
    "W",   # pycodestyle warnings
    "UP",  # pyupgrade (modern Python syntax)
]
ignore = []

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
line-ending = "auto"
```

**Configuration Explained**:

**[tool.ruff]** (General settings):
- `line-length = 130`: Maximum line length (same as used in tasks 006-007)
- `target-version = "py310"`: Use Python 3.10+ features
- `exclude`: Directories to skip (build artifacts, venv, cache)

**[tool.ruff.lint]** (Linting rules):
- `E`, `W`: pycodestyle (PEP 8 compliance)
- `F`: pyflakes (logical errors, unused imports)
- `I`: isort (import statement ordering)
- `N`: pep8-naming (variable/function naming conventions)
- `UP`: pyupgrade (modern Python syntax like `str | None`)

**[tool.ruff.format]** (Formatting settings):
- `quote-style = "double"`: Use double quotes for strings
- `indent-style = "space"`: Use spaces (4 spaces per level)
- `line-ending = "auto"`: Platform-appropriate line endings

### Constraints

- `__init__.py` must be minimal (no business logic)
- Only export truly public functions
- Ruff line length: 130 (matches existing code)
- Use double quotes (Ruff format)
- No emojis

---

## Success Criteria

### Functional

- [ ] Can import from package root: `from langchain_llm import setup_logging, get_api_key, ConfigError`
- [ ] `__all__` contains all 5 public functions/exceptions
- [ ] `__version__` defined as "0.1.0"
- [ ] Ruff configuration added to pyproject.toml

### Quality

- [ ] `ruff check .` passes (0 errors)
- [ ] `ruff format .` formats all files correctly
- [ ] __init__.py has module docstring with example
- [ ] All imports work without errors

### Integration

- [ ] Package exports work:
  ```python
  from langchain_llm import (
      setup_logging,
      get_logger,
      load_env_config,
      get_api_key,
      ConfigError,
  )
  ```
- [ ] Can use utilities immediately after import
- [ ] Can catch ConfigError for exception handling

---

## Expected Approach (Ideal Path)

### Step 1: Research What to Export

Study code from tasks 006-007:
```bash
# See what's public in config.py
grep "^def " src/langchain_llm/config.py

# See what's public in logging_config.py
grep "^def " src/langchain_llm/logging_config.py

# See what exceptions exist
grep "class.*Error" src/langchain_llm/config.py
```

### Step 2: Create __init__.py

Create `src/langchain_llm/__init__.py` with:
1. Module docstring with usage example
2. Imports from config and logging_config
3. `__version__ = "0.1.0"`
4. `__all__` list with 5 items

### Step 3: Test Imports

```bash
poetry run python -c "from langchain_llm import setup_logging, get_logger, load_env_config, get_api_key, ConfigError; print('✓ All imports work')"
```

Should print: `✓ All imports work`

### Step 4: Add Ruff Config to pyproject.toml

Add all three `[tool.ruff]` sections at end of `pyproject.toml` (after `[tool.pytest.ini_options]` from task 004).

### Step 5: Run Ruff

```bash
# Check for issues
poetry run ruff check .

# Auto-fix what's possible
poetry run ruff check --fix .

# Format all code
poetry run ruff format .
```

Expected: No errors, all files formatted

### Step 6: Validate

```bash
# Verify imports
poetry run python -c "from langchain_llm import *; print(__all__)"
# Expected: ['setup_logging', 'get_logger', 'load_env_config', 'get_api_key', 'ConfigError']

# Verify version
poetry run python -c "import langchain_llm; print(langchain_llm.__version__)"
# Expected: 0.1.0

# Verify ruff passes
poetry run ruff check .
# Expected: All checks passed!
```

---

## Testing Strategy

### Import Tests

```python
# Manual test script
import langchain_llm
from langchain_llm import (
    setup_logging,
    get_logger,
    load_env_config,
    get_api_key,
    ConfigError,
)

print("✓ All imports successful")
print(f"✓ Exported: {langchain_llm.__all__}")
print(f"✓ Version: {langchain_llm.__version__}")

# Try using each import
setup_logging()
logger = get_logger(__name__)
logger.info("Test")
print("✓ Functions callable")
```

### Ruff Validation

```bash
# Should pass with 0 errors
ruff check .

# Check formatting applied
ruff format . --check
```

---

## Troubleshooting

**Issue**: Import errors
**Solution**: Check file names match (`config.py`, `logging_config.py`), no typos in imports

**Issue**: Ruff not found
**Solution**: Check installed in dev dependencies, run `poetry install`

**Issue**: Ruff checks fail
**Solution**: Run `ruff check --fix .` to auto-fix, address remaining manually

**Issue**: __all__ doesn't include everything
**Solution**: Verify all 5 public items listed: setup_logging, get_logger, load_env_config, get_api_key, ConfigError

**Issue**: Line too long errors
**Solution**: Check line-length = 130 in pyproject.toml, break long lines if needed

---

## Next Steps

After this task, **Phase 02 is complete**!

1. **Validate Phase 02 Success**:
   ```bash
   # All imports work
   poetry run python -c "from langchain_llm import setup_logging, get_api_key"

   # Ruff happy
   poetry run ruff check .

   # Can use utilities
   poetry run python -c "
   from langchain_llm import setup_logging, get_logger
   setup_logging()
   logger = get_logger(__name__)
   logger.info('Phase 02 complete!')
   "
   ```

2. **Move to Phase 04 (Examples)**:
   - Task 009: Implement basic examples (01_basic.py, 02_streaming.py)
   - Demonstrate using the utilities built in Phase 02

---

## Related Documents

**Design**: [001-project-structure.md](../designs/001-project-structure.md) - Package structure
**Requirements**: [004-quality-requirements.md](../requirements/004-quality-requirements.md) - Ruff requirements
**Phase**: [phase-02-core-interfaces-utilities.md](../phases/phase-02-core-interfaces-utilities.md) - Phase overview
**Previous**: [task-007-logging-module.md](task-007-logging-module.md) - Previous task
**Next**: [task-009-implement-basic-examples.md](task-009-implement-basic-examples.md) - Next task

---

## Document Metadata

- **Task ID**: 008
- **Phase**: 02 - Core Interfaces & Utilities (final task of phase)
- **LOC Output**: ~100 lines (40 lines __init__.py + 60 lines ruff config)
- **Complexity**: Low-Medium
- **Prerequisites**: Tasks 001-007 complete
- **Validates**: Package exports work, Ruff configured correctly
