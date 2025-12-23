# Phase 02: Core Interfaces & Utilities

## Phase Overview

**Purpose**: Implement core utility modules using Test-Driven Development (TDD) - configuration management and logging utilities that form the foundation of the entire project.

**Outcome**: Working configuration and logging modules with:
- Protocol and ABC interface definitions
- Environment variable configuration management
- Custom logging with enhanced formatting
- Complete test coverage (TDD: tests written FIRST)
- Clean package exports

---

## Why This Phase Comes Second

### Building on Foundation

**Phase 01 Created**:
- Project structure
- Package configuration
- AI assistant guidelines
- Environment variable template

**Phase 02 Fills It**:
- Actual utility code (TDD approach)
- Interface definitions
- Core functionality
- Testable, reusable modules

### Test-Driven Development

**This Phase Uses TDD**:
- Tests written FIRST (RED phase)
- Implementation written SECOND (GREEN phase)
- Refactoring THIRD (REFACTOR phase)
- Each task shows complete TDD workflow

**Why TDD**:
- Tests define requirements clearly
- Implementation is testable by design
- Refactoring is safe (tests catch regressions)
- Code quality built in from start

**Order Matters**:
1. Write tests for config module (RED → GREEN → REFACTOR)
2. Write tests for logging module (RED → GREEN → REFACTOR)
3. Export public API (`__init__.py`) - user-facing functions

---

## Tasks in This Phase

### Task 006: Configuration Module (TDD)
**File**: `task-006-config-module.md`

**Purpose**: Implement configuration management using Test-Driven Development

**TDD Workflow**:
1. **RED**: Write test_config.py with all tests (tests fail - code doesn't exist)
2. **GREEN**: Create interfaces.py (ConfigProvider), create config.py (EnvConfigProvider)
3. **REFACTOR**: Add docstrings, improve error messages (tests stay green)

**Key Activities**:
- Create comprehensive test suite (15-20 tests)
- Create fixtures (mock_env_vars, clean_env, temp_env_file)
- Define `ConfigProvider` protocol
- Implement `EnvConfigProvider` class
- Implement convenience functions (load_env_config, get_api_key, etc.)
- Add comprehensive Sphinx docstrings

**Output**: test_config.py (~300 lines), interfaces.py (~80 lines), config.py (~220 lines)

**Why First**: Configuration is foundation for everything

---

### Task 007: Logging Module (TDD)
**File**: `task-007-logging-module.md`

**Purpose**: Implement custom logging using Test-Driven Development

**TDD Workflow**:
1. **RED**: Write test_logging.py with all tests (tests fail - code doesn't exist)
2. **GREEN**: Add LogFormatter ABC to interfaces.py, create logging_config.py
3. **REFACTOR**: Add docstrings, improve format (tests stay green)

**Key Activities**:
- Create comprehensive test suite (15-20 tests)
- Create fixtures (capture_logs, temp_project_root)
- Define `LogFormatter` ABC
- Implement `CustomFormatter` class (enhanced formatting)
- Implement setup_logging(), get_logger() functions
- Add comprehensive Sphinx docstrings

**Output**: test_logging.py (~300 lines), logging_config.py (~250 lines)

**Why Second**: Can reference config module tests as pattern

---

### Task 008: Create Package Exports & Configure Ruff
**File**: `task-008-create-exports-configure-ruff.md`

**Purpose**: Finalize package exports and configure code quality tools

**Key Activities**:
- Create `src/langchain_llm/__init__.py`
  - Import public functions from config and logging_config
  - Define __all__ list (5 exports)
  - Set __version__ = "0.1.0"
  - Write package-level docstring with usage example
- Configure Ruff in `pyproject.toml`
  - Linting rules (E, F, I, N, W, UP)
  - Formatting options (double quotes, 130 chars)
  - Exclusions (__pycache__, .venv, etc.)
- Validate with `ruff check .` and `ruff format .`
- Test imports: `from langchain_llm import setup_logging, get_api_key, ConfigError`

**Output**: `__init__.py` (~40 lines), Ruff config (~60 lines)

**Why Third**: Completes Phase 02, validates all code meets quality standards

---

## Prerequisites

### Before Starting This Phase

**Phase 01 Complete**:
- [ ] Project structure exists
- [ ] Poetry configured
- [ ] .github/copilot-instructions.md in place
- [ ] .env.example created

**Phase 03 Started (Task 004-005)**:
- [ ] pytest configured
- [ ] Enforcement tests created

**Knowledge Required**:
- Test-Driven Development (RED-GREEN-REFACTOR)
- Python protocols (PEP 544)
- Abstract base classes (ABC)
- pytest basics (fixtures, assertions)
- Environment variables (os.getenv)
- Python logging module

**Tools Ready**:
- Poetry environment activated
- pytest installed and configured
- Enforcement tests running

---

## Phase Execution Strategy

### Test-Driven Development (Mandatory)

**THIS PHASE USES TDD**:
- Write tests FIRST (RED phase - they fail)
- Implement SECOND (GREEN phase - tests pass)
- Refactor THIRD (REFACTOR phase - tests stay green)

**No Exceptions**: Both tasks 006 and 007 follow complete TDD workflow

### Suggested Order

1. **Task 006** (Config Module):
   - RED: Write test_config.py, create fixtures
   - GREEN: Create interfaces.py, create config.py
   - REFACTOR: Add docstrings, improve errors
   - Validate: All tests pass, coverage >80%

2. **Task 007** (Logging Module):
   - RED: Write test_logging.py, add fixtures
   - GREEN: Add LogFormatter ABC, create logging_config.py
   - REFACTOR: Add docstrings, improve format
   - Validate: All tests pass, coverage >80%

3. **Task 008** (Exports & Ruff):
   - Create __init__.py with exports
   - Configure Ruff in pyproject.toml
   - Validate: ruff check passes, imports work

---

## Success Criteria

### Phase Complete When

**All Tests Pass**:
- [ ] test_config.py: All tests passing (15-20 tests)
- [ ] test_logging.py: All tests passing (15-20 tests)
- [ ] Enforcement tests: All passing
- [ ] No test failures: `pytest tests/ -v`

**Coverage Achieved**:
- [ ] config.py: >80% coverage
- [ ] logging_config.py: >80% coverage
- [ ] Overall: >80% coverage

**Code Written**:
- [ ] `interfaces.py` with ConfigProvider protocol and LogFormatter ABC
- [ ] `config.py` with EnvConfigProvider and helper functions
- [ ] `logging_config.py` with CustomFormatter and setup functions
- [ ] `__init__.py` with proper exports (5 items)

**Quality Checks**:
- [ ] All functions have Sphinx docstrings
- [ ] All signatures have type hints
- [ ] `ruff check .` passes (0 errors)
- [ ] `ruff format .` applied successfully
- [ ] Enforcement tests pass

**Functionality Works**:
```python
# Test complete workflow
from langchain_llm import (
    setup_logging,
    get_logger,
    load_env_config,
    get_api_key,
    ConfigError,
)

# Setup
setup_logging(level="INFO")
load_env_config()

# Use
logger = get_logger(__name__)
logger.info("Phase 02 complete")  # Shows with custom format

# Config works
try:
    key = get_api_key("openai", required=False)
    if key:
        logger.info(f"OpenAI configured")
except ConfigError as e:
    logger.warning(f"OpenAI not configured: {e}")
```

### Validation Commands

```bash
# All tests must pass
pytest tests/ -v

# Coverage must be >80%
pytest --cov=src/langchain_llm --cov-report=term

# Enforcement must pass
pytest tests/enforcement/ -v

# Ruff must pass
ruff check .
ruff format . --check

# Imports must work
poetry run python -c "from langchain_llm import setup_logging, get_api_key, ConfigError"
```

---

## Outputs of This Phase

### Files Created/Modified

```
src/langchain_llm/
├── __init__.py              # NEW: Public API exports
├── interfaces.py            # NEW: ConfigProvider + LogFormatter
├── config.py                # NEW: Configuration management
└── logging_config.py        # NEW: Logging utilities

pyproject.toml               # MODIFIED: Added [tool.ruff] sections
```

### Interfaces Defined

**ConfigProvider Protocol**:
```python
class ConfigProvider(Protocol):
    def get_key(self, provider: str, required: bool = True) -> Optional[str]: ...
    def get_all_keys(self) -> Dict[str, Optional[str]]: ...
    def validate(self, provider: str) -> None: ...
    def get_model_name(self, provider: str) -> Optional[str]: ...
```

**LogFormatter ABC**:
```python
class LogFormatter(ABC):
    @abstractmethod
    def format(self, record: logging.LogRecord) -> str: ...
```

### Public API Functions

From `__init__.py`:
- `setup_logging(level, log_file, format_string)` - Configure logging
- `get_logger(name)` - Get named logger
- `load_env_config(env_file)` - Load environment variables
- `get_api_key(provider, required)` - Get provider API key

---

## Common Issues & Solutions

**Issue**: Import errors when testing
**Solution**: Ensure `poetry install` ran, activate Poetry shell

**Issue**: Type hints not recognized
**Solution**: Using Python 3.10+? Check `python --version`

**Issue**: Ruff check fails
**Solution**: Run `ruff check --fix .` to auto-fix, then `ruff format .`

**Issue**: Can't find project root in logging
**Solution**: Ensure pyproject.toml exists at project root

**Issue**: Environment variables not loading
**Solution**: Check .env file exists, `load_env_config()` called before `get_api_key()`

---

## Transition to Next Phase

### Ready for Phase 03 When

**Code Complete**:
- [ ] All 4 tasks finished (004-007)
- [ ] Interfaces defined
- [ ] Modules implemented
- [ ] Ruff configured
- [ ] Exports working

**Manual Tests Pass**:
- [ ] Can import package
- [ ] Logging produces formatted output
- [ ] Config reads environment variables
- [ ] No import errors

**What's Next** (Phase 03):
- Setup pytest infrastructure
- Write fixtures for testing
- Write tests for config module (TDD validation)
- Write tests for logging module (TDD validation)
- Create enforcement tests (Sphinx docstrings, no emojis)

**Why This Order**:
- Phase 02 created code
- Phase 03 validates it with tests
- TDD cycle completes (tests validate implementation)
- Examples (Phase 04-05) use tested utilities

---

## Related Documents

**Requirements**:
- [003-environment-conventions.md](../requirements/003-environment-conventions.md) - Configuration standards
- [004-quality-requirements.md](../requirements/004-quality-requirements.md) - TDD requirements

**Designs**:
- [002-configuration-design.md](../designs/002-configuration-design.md) - Config implementation details
- [003-logging-design.md](../designs/003-logging-design.md) - Logging implementation details
- [000-architecture-overview.md](../designs/000-architecture-overview.md) - Interface-driven design

**Tasks**:
- [task-006-config-module.md](../tasks/task-006-config-module.md) - Config module with TDD
- [task-007-logging-module.md](../tasks/task-007-logging-module.md) - Logging module with TDD
- [task-008-create-exports-configure-ruff.md](../tasks/task-008-create-exports-configure-ruff.md) - Package exports

**Previous/Next**:
- [phase-01-project-foundation.md](phase-01-project-foundation.md) - Previous phase
- [phase-03-testing-infrastructure.md](phase-03-testing-infrastructure.md) - Test infrastructure (tasks 004-005)
- [phase-04-basic-examples.md](phase-04-basic-examples.md) - Next phase (after task 008)

---

## Document Metadata

- **Version**: 2.0
- **Phase Number**: 02 of 06
- **Task Range**: 006-008 (3 tasks)
- **Estimated Duration**: 6-8 hours
- **Complexity**: High
- **Dependencies**: Phase 01 complete, pytest configured (task 004), enforcement tests (task 005)
- **Status**: Active
- **Owner**: EAD LangChain Template Team
- **TDD**: Mandatory for all implementation tasks
