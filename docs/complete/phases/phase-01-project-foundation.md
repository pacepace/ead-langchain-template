# Phase 01: Project Foundation

## Phase Overview

**Purpose**: Establish the basic project structure, package configuration, and essential project files before writing any application code.

**Outcome**: A properly structured Python project with:
- Poetry and pip support configured
- Project directory structure created
- GitHub configuration in place (AI assistant guidelines)
- Environment variable template ready
- Foundation for all subsequent development

---

## Why This Phase Comes First

### Setting the Foundation

**Critical First Steps**:
1. **Package Structure**: Must exist before code can be written
2. **GitHub Configuration**: AI assistants need guidelines from the start
3. **Environment Template**: Developers need to know what configuration is required

**Prevents Rework**:
- Changing project structure later is disruptive
- AI assistants generate wrong patterns without copilot-instructions.md
- Missing .env.example causes confusion

### The Cost of Skipping

**What Happens If You Skip This**:
- Code ends up in wrong locations
- Import paths break
- AI assistants violate conventions
- Configuration becomes chaotic
- Tests can't find code

**Time Saved by Doing It Right**:
- 2-4 hours upfront investment
- Saves 10+ hours of refactoring later
- Prevents configuration bugs
- Enables smooth development from day 1

---

## Tasks in This Phase

### Task 001: Initialize Poetry Project
**File**: `task-001-initialize-poetry-project.md`

**Purpose**: Create `pyproject.toml` with project metadata and dependencies

**Key Activities**:
- Run `poetry init`
- Configure package name, version, description
- Add runtime dependencies (LangChain packages, python-dotenv)
- Add development dependencies (pytest, ruff, jupyter)
- Configure src-layout packaging

**Output**: `pyproject.toml`, `poetry.lock`

**Why First**: Poetry manages everything else (dependencies, packaging, scripts)

---

### Task 002: Setup Project Structure
**File**: `task-002-setup-project-structure.md`

**Purpose**: Create all directories and skeleton files

**Key Activities**:
- Create `src/langchain_llm/` (package directory)
- Create `examples/` (tutorial examples)
- Create `tests/` with `enforcement/` subdirectory
- Create `docs/complete/` structure
- Create `.gitignore` with proper exclusions

**Output**: Complete directory tree, empty skeleton files

**Why Second**: Need structure before adding content

---

### Task 003: Create GitHub Structure
**File**: `task-003-create-github-structure.md`

**Purpose**: Set up `.github/` directory with AI assistant guidelines

**Key Activities**:
- Create `.github/` directory
- Create issue templates (bug report, feature request)
- Create PR template (optional)
- Prepare for copilot-instructions.md (Task 004 will write content)

**Output**: `.github/` structure

**Why Early**: GitHub structure conventions need to be in place

---

### Task 004: Write Copilot Instructions
**File**: `task-004-write-copilot-instructions.md`

**Purpose**: Create comprehensive AI assistant guidelines

**Key Activities**:
- Document environment variable conventions
- Explain TDD workflow
- Specify Sphinx docstring requirement
- Provide code examples and patterns
- List common pitfalls

**Output**: `.github/copilot-instructions.md`

**Why Early**: AI assistants need this before generating any code

---

### Task 005: Create .env.example
**File**: `task-005-create-env-example.md`

**Purpose**: Document all environment variables

**Key Activities**:
- List all `EADLANGCHAIN_*` variables
- Add helpful comments and links
- Group by category (AI, LOG, etc.)
- Show default values
- Mark required vs optional

**Output**: `.env.example`

**Why Last in Phase**: Completes foundation, ready for development

---

## Prerequisites

### Before Starting This Phase

**Required**:
- Python 3.10+ installed
- Poetry installed (`pip install poetry` or from source)
- Git installed and configured
- Text editor / IDE ready

**Recommended**:
- Understanding of Python packaging
- Familiarity with Poetry basics
- Git/GitHub experience
- Project requirements documents read

**Not Required**:
- API keys (those come later)
- LangChain knowledge (learning as we go)
- Advanced Python skills (template is educational)

### Verification

**Check Prerequisites**:
```bash
# Python version
python --version  # Should be 3.10+

# Poetry installed
poetry --version  # Should be 1.5+

# Git configured
git config --global user.name
git config --global user.email
```

---

## Phase Execution Strategy

### Sequential Execution

**Tasks MUST be done in order**:
1. Poetry init (001) - Creates project config
2. Structure (002) - Creates directories
3. GitHub structure (003) - Creates .github/
4. Copilot instructions (004) - Writes AI guidelines
5. .env.example (005) - Documents configuration

**Why Sequential**:
- Each task depends on previous
- Poetry must exist before directories (defines package location)
- Directories must exist before populating
- GitHub structure before writing copilot-instructions.md

### Common Issues

**Issue**: Poetry not found after installation
**Solution**: Close and reopen terminal, or add Poetry to PATH

**Issue**: Python version mismatch
**Solution**: Use pyenv or virtualenv to manage Python versions

**Issue**: Git not initialized
**Solution**: `git init` in project root

---

## Success Criteria

### Phase Complete When

- [ ] `pyproject.toml` exists and is valid
- [ ] `poetry.lock` exists
- [ ] All directories created (src/, examples/, tests/, docs/, .github/)
- [ ] `.gitignore` comprehensive
- [ ] `.github/copilot-instructions.md` complete and detailed
- [ ] `.env.example` documents all variables
- [ ] `poetry install` runs without errors
- [ ] Package can be imported: `from langchain_llm import ...` (even though empty)

### Validation Commands

```bash
# Verify Poetry setup
poetry install
poetry run python -c "import langchain_llm; print('Package imported!')"

# Verify structure
ls src/langchain_llm/
ls examples/
ls tests/enforcement/
ls .github/

# Verify files
cat .github/copilot-instructions.md
cat .env.example
cat pyproject.toml
```

### Quality Gates

- [ ] `poetry check` passes
- [ ] All required directories exist
- [ ] `.gitignore` prevents committing .env
- [ ] Copilot instructions are comprehensive (>500 lines)
- [ ] .env.example has all variables documented

---

## Outputs of This Phase

### Files Created

```
project-root/
├── pyproject.toml           # Poetry configuration
├── poetry.lock              # Locked dependencies
├── .gitignore               # Git exclusions
├── .env.example             # Environment variable template
├── src/
│   └── langchain_llm/
│       └── __init__.py      # Empty package init
├── examples/                # Empty directory
├── tests/
│   ├── conftest.py          # Empty fixture file
│   └── enforcement/
│       └── __init__.py      # Empty init
├── docs/
│   └── complete/            # Empty structure
└── .github/
    └── copilot-instructions.md  # AI assistant guidelines
```

### Configurations Set

**Poetry** (`pyproject.toml`):
- Package name: `langchain-llm`
- Python: `^3.10`
- Dependencies: LangChain packages, dotenv
- Dev dependencies: pytest, ruff, jupyter
- Src-layout: `{include = "langchain_llm", from = "src"}`

**Git** (`.gitignore`):
- `.env` files
- `__pycache__`
- `.pytest_cache`
- Virtual environments
- IDE files

**GitHub** (`.github/copilot-instructions.md`):
- Environment variable conventions
- TDD workflow
- Sphinx docstring requirement
- Code patterns

---

## Transition to Next Phase

### Ready for Phase 02 When

**Prerequisites Met**:
- [ ] All Phase 01 tasks complete
- [ ] Project structure validated
- [ ] Poetry environment works
- [ ] Git repository initialized (optional but recommended)

**What's Next** (Phase 02):
- Create interface definitions (`interfaces.py`)
- Implement configuration module (`config.py`)
- Implement logging module (`logging_config.py`)
- Create package exports (`__init__.py`)

**Why This Order**:
- Phase 01 created structure
- Phase 02 fills it with core utilities
- Interfaces must be defined before implementations
- Configuration and logging are foundations for examples

---

## Related Documents

**Requirements**:
- [002-technical-requirements.md](../requirements/002-technical-requirements.md) - Tech stack details
- [003-environment-conventions.md](../requirements/003-environment-conventions.md) - Env var standards

**Designs**:
- [001-project-structure.md](../designs/001-project-structure.md) - Directory layout
- [000-architecture-overview.md](../designs/000-architecture-overview.md) - Overall architecture

**Tasks** (detailed instructions):
- [task-001-initialize-poetry-project.md](../tasks/task-001-initialize-poetry-project.md)
- [task-002-setup-project-structure.md](../tasks/task-002-setup-project-structure.md)
- [task-003-create-github-structure.md](../tasks/task-003-create-github-structure.md)
- [task-004-write-copilot-instructions.md](../tasks/task-004-write-copilot-instructions.md)
- [task-005-create-env-example.md](../tasks/task-005-create-env-example.md)

**Next Phase**:
- [phase-02-core-interfaces-utilities.md](phase-02-core-interfaces-utilities.md)

---

## Document Metadata

- **Version**: 1.0
- **Phase Number**: 01 of 06
- **Task Range**: 001-005 (5 tasks)
- **Estimated Duration**: 2-4 hours
- **Complexity**: Low-Medium
- **Dependencies**: None (first phase)
- **Status**: Active
- **Owner**: EAD LangChain Template Team
