# Phase 03: Test Infrastructure Foundation

## Phase Overview

**Purpose**: Establish foundational testing infrastructure that enables Test-Driven Development in subsequent phases.

**Outcome**: Testing foundation with:
- pytest configuration and test discovery
- Enforcement tests (quality gates)
- Ready for TDD in Phase 02

**Note**: This is Phase 03 but executes BEFORE Phase 02 because Phase 02 uses TDD and needs this infrastructure first.

---

## Why This Phase Is Essential

### Enabling Test-Driven Development

**Phase 03 Creates Foundation**:
- pytest configuration
- Test discovery patterns
- Enforcement tests (quality gates)

**Phase 02 Uses Foundation**:
- Writes tests first (RED)
- Implements to pass tests (GREEN)
- Refactors while tests stay green (REFACTOR)

### Meta-Testing Infrastructure

**This Phase Is About**:
- Testing tools (pytest)
- Quality gates (enforcement tests)
- NOT about testing modules (that's in Phase 02 with TDD)

**What's Different**:
- No implementation code yet (Phase 02 will create that)
- Just infrastructure and quality enforcement
- Runs EARLY to enable TDD workflow

---

## Tasks in This Phase

### Task 004: Setup pytest Infrastructure
**File**: `task-004-setup-pytest-infrastructure.md`

**Purpose**: Configure pytest for test discovery

**Key Activities**:
- Add pytest configuration to `pyproject.toml` ([tool.pytest.ini_options])
- Configure test discovery (testpaths, python_files, test markers)
- Create `tests/` directory structure
- Create basic `tests/conftest.py` (empty initially, fixtures added incrementally in Phase 02)
- Validate pytest setup: `pytest --collect-only`

**Output**:
- pytest config in `pyproject.toml` (~20 lines)
- `tests/__init__.py` (empty)
- `tests/conftest.py` (basic structure, ~10 lines)

**Why First**: Must configure pytest before writing any tests

---

### Task 005: Create Enforcement Tests
**File**: `task-005-create-enforcement-tests.md`

**Purpose**: Automated quality gates for code standards

**Key Activities**:
- Create `tests/enforcement/` directory
- Create `tests/enforcement/__init__.py` (empty)
- Create `tests/enforcement/test_sphinx_docstrings.py`:
  - Scan Python files with AST parsing
  - Detect Google-style docstrings (Args:, Returns:, etc.)
  - Detect NumPy-style docstrings (Parameters section with dashes)
  - Verify Sphinx elements present (:param, :ptype, :return, :rtype)
  - Fail with clear error messages listing violations
- Create `tests/enforcement/test_no_emojis.py`:
  - Scan all code files (Python, notebooks, configs)
  - Detect emoji characters using Unicode ranges
  - Fail with clear error listing violations
- Validate enforcement tests catch violations

**Output**:
- `tests/enforcement/__init__.py` (empty)
- `tests/enforcement/test_sphinx_docstrings.py` (~300 lines)
- `tests/enforcement/test_no_emojis.py` (~200 lines)

**Why Second**: Quality gates active before any code is written (Phase 02)

**Validation**: `pytest tests/enforcement/ -v` passes

---

## Prerequisites

### Before Starting This Phase

**Phase 01 Complete**:
- [ ] Poetry project initialized
- [ ] pyproject.toml exists
- [ ] Project structure created

**Tools Needed**:
- pytest (will add to dev dependencies)
- Poetry environment activated

**Knowledge Required**:
- pytest basics (test discovery, markers)
- Regular expressions (for enforcement tests)
- Python AST module (for docstring checking)
- Unicode character ranges (for emoji detection)

---

## Phase Execution Strategy

### Infrastructure First, Tests Later

**This Phase** (Tasks 004-005):
- Create testing infrastructure
- Create enforcement tests
- NO module tests yet (those come in Phase 02 with TDD)

**Phase 02** (Tasks 006-007):
- Write tests first (using infrastructure from this phase)
- Implement code second
- True TDD workflow

### Suggested Order

1. **Task 004** (pytest setup):
   - Add pytest config to pyproject.toml
   - Create tests/ directory
   - Create empty conftest.py
   - Validate: `pytest --collect-only` works

2. **Task 005** (enforcement tests):
   - Create enforcement tests directory
   - Write docstring enforcement tests
   - Write emoji enforcement tests
   - Validate: `pytest tests/enforcement/ -v` passes

---

## Success Criteria

### Phase Complete When

**pytest Infrastructure Ready**:
- [ ] pytest config in pyproject.toml
- [ ] tests/ directory created
- [ ] tests/__init__.py exists
- [ ] tests/conftest.py exists (basic structure)
- [ ] `pytest --collect-only` works

**Enforcement Tests Created**:
- [ ] tests/enforcement/ directory exists
- [ ] test_sphinx_docstrings.py created (~300 lines)
- [ ] test_no_emojis.py created (~200 lines)
- [ ] Enforcement tests pass: `pytest tests/enforcement/ -v`

**Enforcement Tests Functional**:
- [ ] Catch Google-style docstrings (Args:, Returns:)
- [ ] Catch NumPy-style docstrings (Parameters\n---)
- [ ] Catch emoji characters in code
- [ ] Clear error messages when violations found
- [ ] Pass when code meets standards

**Ready for Phase 02**:
- [ ] pytest configured and working
- [ ] Quality gates active (enforcement tests)
- [ ] No code violations in existing files

### Validation Commands

```bash
# pytest must be configured
pytest --version

# Test discovery must work (no tests yet, but infrastructure ready)
pytest --collect-only
# Expected: collected 0 items OR collected N items from enforcement/

# Enforcement tests must pass
pytest tests/enforcement/ -v
# Expected: All PASSED

# Validate markers configured
pytest --markers | grep slow
# Expected: shows slow marker description
```

---

## Outputs of This Phase

### Files Created

```
tests/
├── conftest.py                        # NEW: Fixtures
├── test_config.py                     # NEW: Config tests
├── test_logging.py                    # NEW: Logging tests
└── enforcement/
    ├── __init__.py                    # NEW: Empty
    ├── test_sphinx_docstrings.py      # NEW: Docstring enforcement
    └── test_no_emojis.py              # NEW: Emoji enforcement

pyproject.toml                         # MODIFIED: pytest config added
```

### Test Statistics

**Expected Test Count**: ~40-50 tests total
- conftest.py: 5 fixtures
- test_config.py: ~15-20 tests
- test_logging.py: ~15-20 tests
- Enforcement: 3-4 tests

**Expected Coverage**:
- config.py: 85-95%
- logging_config.py: 85-95%
- interfaces.py: 100% (just protocol definitions)
- __init__.py: 100% (just exports)
- Overall: >80%

---

## Common Issues & Solutions

**Issue**: pytest not finding tests
**Solution**: Check `pyproject.toml` has correct testpaths, run `pytest --collect-only`

**Issue**: Fixtures not working
**Solution**: Ensure conftest.py in tests/ directory, check fixture names match

**Issue**: Coverage too low
**Solution**: Check which lines are uncovered with HTML report, add tests for those paths

**Issue**: Enforcement tests false positives
**Solution**: Adjust regex patterns, test on actual violations first

**Issue**: Tests fail on first run
**Solution**: Check .env file exists, mock_env_vars fixture being used

**Issue**: Import errors in tests
**Solution**: Run `poetry install` to install package in editable mode

---

## Transition to Next Phase

### Ready for Phase 04 When

**All Tests Pass**:
- [ ] 0 failures, 0 errors
- [ ] 40-50 tests passing

**Coverage Achieved**:
- [ ] Overall >80%
- [ ] config.py >80%
- [ ] logging_config.py >80%

**Quality Gates Pass**:
- [ ] Enforcement tests pass
- [ ] No Google/NumPy docstrings detected
- [ ] No emojis detected

**What's Next** (Phase 04):
- Implement examples 01-02 (basic + streaming)
- Create Jupyter notebooks for examples
- Demonstrate actual LLM usage
- Show configuration and logging in action

**Why This Order**:
- Phase 03 validated core utilities
- Phase 04 uses tested utilities in examples
- Examples can confidently use config + logging
- Any bugs caught by tests

---

## Related Documents

**Requirements**:
- [004-quality-requirements.md](../requirements/004-quality-requirements.md) - Testing standards

**Designs**:
- [005-testing-strategy.md](../designs/005-testing-strategy.md) - Detailed testing approach

**Tasks**:
- [task-004-setup-pytest-infrastructure.md](../tasks/task-004-setup-pytest-infrastructure.md) - pytest config
- [task-005-create-enforcement-tests.md](../tasks/task-005-create-enforcement-tests.md) - Quality gates

**Previous/Next**:
- [phase-01-project-foundation.md](phase-01-project-foundation.md) - Previous
- [phase-02-core-interfaces-utilities.md](phase-02-core-interfaces-utilities.md) - Next (uses this infrastructure)
- [phase-04-basic-examples.md](phase-04-basic-examples.md) - Later phase

---

## Document Metadata

- **Version**: 2.0
- **Phase Number**: 03 of 06 (executes early, between phases 01 and 02)
- **Task Range**: 004-005 (2 tasks)
- **Complexity**: Medium
- **Dependencies**: Phase 01 complete
- **Status**: Active
- **Owner**: EAD LangChain Template Team
- **Purpose**: Enable TDD for Phase 02
