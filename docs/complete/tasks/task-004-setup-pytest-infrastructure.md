# Task 004: Setup pytest Infrastructure

## Task Context

**Phase**: 03 - Test Infrastructure Foundation
**Sequence**: Fourth task (first of Phase 03)
**Complexity**: Low
**Output**: ~50 LOC (pytest config + basic test structure)

### Why This Task Exists

Before writing any tests, we need:
- Test discovery configuration
- pytest markers for test organization
- Basic test directory structure
- Foundation for incremental fixture creation

This task creates the minimal testing infrastructure. Fixtures will be added incrementally in tasks 006-007 as they're needed.

### Where This Fits

```
Task 003 → Task 004 (YOU ARE HERE) → Task 005 → Task 006 → Task 007
.env.example  pytest setup           Enforcement  TDD Config  TDD Logging
                                     Tests        Module      Module
```

---

## Prerequisites

### Completed Tasks

- [x] **Task 001**: Poetry project initialized with pyproject.toml
- [x] **Task 002**: GitHub setup, copilot instructions
- [x] **Task 003**: .env.example created

### Required Knowledge

**pytest**:
- Test discovery patterns
- Configuration in pyproject.toml
- Test markers
- conftest.py purpose

**Testing Concepts**:
- Test directory structure
- Test file naming conventions
- Fixture concept (will use later)

---

## Research Required

### pytest Documentation

**Read**:
- pytest configuration: https://docs.pytest.org/en/stable/reference/customize.html
- pytest test discovery: https://docs.pytest.org/en/stable/goodpractices.html#test-discovery
- pytest markers: https://docs.pytest.org/en/stable/mark.html

**Key Concepts**:
- `testpaths`: Where pytest looks for tests
- `python_files`, `python_classes`, `python_functions`: Discovery patterns
- Markers: Custom test categorization
- conftest.py: Shared test configuration

### No Code to Research Yet

This is the first testing task. No prior test code exists to reference.

---

## Task Description

### Objective

Configure pytest in pyproject.toml and create basic test directory structure with empty conftest.py. This provides the foundation for test writing in subsequent tasks.

### Requirements

#### 1. Add pytest Configuration to pyproject.toml

Add the following section to `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --strict-markers"
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
]
```

**Configuration Explained**:

**testpaths**:
- Tells pytest to look in `tests/` directory for test files
- Speeds up test discovery by limiting search scope
- Can run `pytest` without arguments

**python_files**:
- Pattern for test file names: `test_*.py`
- Example: `test_config.py`, `test_logging.py`
- Standard pytest convention

**python_classes** (optional usage):
- Pattern for test class names: `Test*`
- Example: `TestConfigProvider`, `TestGetApiKey`
- Used when grouping related tests in classes

**python_functions**:
- Pattern for test function names: `test_*`
- Example: `test_get_api_key_with_valid_key`
- Standard pytest convention

**addopts**:
- `-v`: Verbose output (shows individual test names)
- `--strict-markers`: Fail if unknown markers used (catches typos)

**markers**:
- `slow`: Custom marker for time-consuming tests
- Usage in future tests: `@pytest.mark.slow`
- Can skip slow tests: `pytest -m "not slow"`

#### 2. Create Test Directory Structure

Create the following directory structure:

```
tests/
├── __init__.py
└── conftest.py
```

**Files to create**:

**tests/__init__.py** (empty file):
```python
# Empty file - makes tests/ a Python package
```

**tests/conftest.py** (basic structure):
```python
"""
Shared pytest configuration and fixtures for langchain_llm tests.

This file will be populated incrementally as tasks need fixtures:
- Task 006 will add config-related fixtures (mock_env_vars, clean_env, temp_env_file)
- Task 007 will add logging-related fixtures (capture_logs, temp_project_root)

For now, this file establishes the structure.
"""

import pytest


# Fixtures will be added here incrementally by tasks 006-007
```

#### 3. Verify pytest Configuration

Run pytest to verify configuration is recognized:

```bash
poetry run pytest --version
# Should show: pytest X.Y.Z

poetry run pytest --collect-only
# Should show: collected 0 items (no tests exist yet)

poetry run pytest --markers
# Should show: @pytest.mark.slow: marks tests as slow...
```

### Constraints

- pytest config must be in `[tool.pytest.ini_options]` section of pyproject.toml
- Test directory must be named `tests/` (lowercase)
- conftest.py must be in root of tests/ directory
- Do not create fixtures yet (those come later)

---

## Success Criteria

### Functional

- [ ] `[tool.pytest.ini_options]` added to pyproject.toml
- [ ] Markers configured correctly
- [ ] `tests/` directory created
- [ ] `tests/__init__.py` exists (empty)
- [ ] `tests/conftest.py` exists with basic structure
- [ ] `pytest --collect-only` works (collects 0 items)
- [ ] `pytest --markers` shows slow marker

### Quality

- [ ] TOML syntax valid (no parse errors)
- [ ] conftest.py has module docstring
- [ ] Directory structure correct

### Integration

- [ ] pytest discovers tests/ directory
- [ ] Ready for test files in tasks 005-007
- [ ] conftest.py ready for fixture additions

---

## Expected Approach (Ideal Path)

### Step 1: Add pytest Configuration

Open `pyproject.toml` and add the `[tool.pytest.ini_options]` section after the `[tool.poetry.dependencies]` section.

Copy the configuration exactly as specified in Requirements section above.

### Step 2: Create Test Directory

```bash
# From project root
mkdir tests
touch tests/__init__.py
```

### Step 3: Create conftest.py

Create `tests/conftest.py` with the basic structure provided in Requirements section.

Key points:
- Add module docstring explaining incremental fixture approach
- Import pytest (will need it for fixtures later)
- Add comment placeholder for future fixtures

### Step 4: Validate Configuration

```bash
# Check pytest recognizes config
poetry run pytest --version

# Check test discovery (should find no tests yet)
poetry run pytest --collect-only

# Check markers registered
poetry run pytest --markers | grep slow
# Should see: @pytest.mark.slow: marks tests as slow...

# Validate conftest.py syntax
poetry run python -c "import sys; sys.path.insert(0, 'tests'); import conftest; print('✓ conftest.py valid')"
```

Expected output:
- `--collect-only`: "collected 0 items"
- `--markers`: Shows slow marker with description
- No errors or warnings

---

## Troubleshooting

**Issue**: pytest not found
**Solution**: Run `poetry install` to install dev dependencies, ensure pytest in `[tool.poetry.group.dev.dependencies]`

**Issue**: pytest doesn't see config
**Solution**: Check TOML syntax (use online TOML validator if needed), ensure section name exact: `[tool.pytest.ini_options]`

**Issue**: Can't import conftest
**Solution**: Ensure tests/__init__.py exists, conftest.py has valid Python syntax

**Issue**: --markers doesn't show slow marker
**Solution**: Check markers list in pyproject.toml, ensure correct format with colon and description

**Issue**: --strict-markers causes errors
**Solution**: This is expected if using undefined markers; only use markers defined in config

---

## Next Steps

After completing this task:

1. **Validate**:
   ```bash
   pytest --collect-only  # Should work with 0 items
   pytest --markers       # Should show slow marker
   ```

2. **Move to Task 005**:
   - Create enforcement tests (Sphinx docstrings, no emojis)
   - First actual test files using this pytest infrastructure

---

## Related Documents

**Design**: [005-testing-strategy.md](../designs/005-testing-strategy.md) - Testing philosophy
**Phase**: [phase-03-testing-infrastructure.md](../phases/phase-03-testing-infrastructure.md) - Phase overview
**Previous**: [task-003-create-env-example.md](task-003-create-env-example.md) - Previous task
**Next**: [task-005-create-enforcement-tests.md](task-005-create-enforcement-tests.md) - Next task

---

## Document Metadata

- **Task ID**: 004
- **Phase**: 03 - Test Infrastructure Foundation
- **LOC Output**: ~50 lines (pytest config + basic structure)
- **Complexity**: Low
- **Prerequisites**: Tasks 001-003 complete
- **Validates**: pytest infrastructure ready for test creation
