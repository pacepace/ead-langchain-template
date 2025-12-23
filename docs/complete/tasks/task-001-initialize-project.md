# Task 001: Initialize Project with Poetry and Structure

## Task Context

**Phase**: 01 - Project Foundation
**Sequence**: First task (no prerequisites)
**Complexity**: Medium
**Output**: ~400 LOC across multiple configuration files

### Why This Task Exists

Every Python project needs:
- Package metadata and dependencies managed
- Directory structure established
- Build system configured
- Code quality tools set up

This task creates the foundation that all subsequent work builds on.

### Where This Fits

```
Task 001 (YOU ARE HERE) → Task 002 → Task 003 → ... → Task 014
Poetry + Structure          GitHub       .env      Core Code   README
```

---

## Prerequisites

### Required Knowledge

**Python Packaging**:
- Understand what pyproject.toml is (PEP 518/621)
- Know difference between runtime and dev dependencies
- Understand src-layout vs flat layout

**Poetry Basics**:
- What Poetry does (dependency management + packaging)
- Basic Poetry commands (init, add, install)
- Poetry vs pip differences

**Project Structure**:
- What goes in src/ vs tests/ vs examples/
- Why separate concerns

### Required Tools

```bash
# Verify these are installed
python --version  # Should be 3.10+
poetry --version  # Should be 1.5+
git --version     # For version control

# If Poetry not installed:
pip install poetry
# OR from official installer
curl -sSL https://install.python-poetry.org | python3 -
```

### Completed Tasks

- None (this is the first task)

---

## Research Required

### Python Packaging

**Read**:
- PEP 518: pyproject.toml specification
- PEP 621: Storing project metadata in pyproject.toml
- Poetry documentation: https://python-poetry.org/docs/

**Key Concepts to Understand**:
- Why src-layout prevents import issues
- How Poetry resolves dependencies
- Difference between `[tool.poetry.dependencies]` and `[tool.poetry.group.dev.dependencies]`

### Code Quality Tools

**Read**:
- Ruff documentation: https://docs.astral.sh/ruff/
- Ruff configuration options

**Key Concepts**:
- What Ruff replaces (flake8, black, isort)
- Line length conventions (we use 130)
- Import sorting rules

---

## Code to Explore

### Similar Projects to Study

Since this is the first task, look at these reference implementations:

**Poetry pyproject.toml Examples**:
```toml
# Example structure (don't copy verbatim, adapt)
[tool.poetry]
name = "package-name"
version = "0.1.0"
description = "Description here"
authors = ["Your Name <your.email@example.com>"]
packages = [{include = "package_name", from = "src"}]

[tool.poetry.dependencies]
python = "^3.10"
# runtime deps here

[tool.poetry.group.dev.dependencies]
# dev deps here
```

**Ruff Configuration Examples**:
```toml
[tool.ruff]
line-length = 130
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]
```

### Patterns to Study

**Src-Layout Pattern**:
```
project-root/
├── src/
│   └── package_name/
│       ├── __init__.py
│       └── module.py
├── tests/
├── examples/
└── pyproject.toml
```

Why: Prevents accidental imports of uninstalled package during development.

---

## Task Description

### Objective

Create a complete Poetry-managed Python project with proper structure, all directories, and code quality configuration.

### Requirements

#### 1. Initialize Poetry Project

**Create pyproject.toml with**:
- Package name: `langchain-llm`
- Version: `0.1.0`
- Description: "EAD template for building LLM applications with LangChain"
- Python requirement: `^3.10`
- Src-layout package configuration

**Runtime Dependencies**:
```toml
[tool.poetry.dependencies]
python = "^3.10"
langchain-core = "^0.3.0"
langchain-openai = "^0.2.0"
langchain-anthropic = "^0.3.0"
langchain-google-genai = "^2.0.0"
python-dotenv = "^1.0.0"
```

**Development Dependencies**:
```toml
[tool.poetry.group.dev.dependencies]
pytest = "^8.0.0"
pytest-asyncio = "^0.23.0"
pytest-cov = "^7.0.0"
ruff = "^0.8.0"
jupyter = "^1.1.0"
ipykernel = "^6.29.0"
```

#### 2. Create Directory Structure

**Required Directories**:
```
project-root/
├── src/
│   └── langchain_llm/          # Package directory
│       └── __init__.py         # Empty for now
├── examples/                   # Tutorial examples
├── tests/                      # Test suite
│   └── enforcement/            # Code quality tests
│       └── __init__.py         # Empty
├── docs/
│   └── complete/              # Already exists (these docs!)
└── .github/                    # GitHub configuration
```

Create all directories and empty `__init__.py` files.

#### 3. Create .gitignore

**Must Exclude**:
```gitignore
# Environment variables
.env
.env.local
*.env
!.env.example

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Virtual environments
env/
venv/
.venv/
ENV/
env.bak/
venv.bak/

# Poetry
# Note: poetry.lock should be committed
dist/
build/
*.egg-info/

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# Jupyter
.ipynb_checkpoints/
*.ipynb_checkpoints

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
logs/
*.log
```

#### 4. Configure Ruff

**Add to pyproject.toml**:
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

#### 5. Generate requirements.txt

After Poetry setup, generate pip-compatible requirements:
```bash
poetry export -f requirements.txt -o requirements.txt --without-hashes
```

### Constraints

- Use Poetry commands, not manual file editing (where possible)
- Follow src-layout strictly
- No emojis in any files
- Line length: 130 characters maximum

### Interfaces (Design Specification)

None for this task (just project setup).

---

## Success Criteria

### Functional

- [ ] `pyproject.toml` exists and is valid
- [ ] `poetry.lock` generated
- [ ] All directories created
- [ ] `.gitignore` comprehensive
- [ ] `requirements.txt` generated
- [ ] Can run: `poetry install` without errors
- [ ] Can activate: `poetry shell`
- [ ] Can import package (even though empty): `python -c "import langchain_llm"`

### Quality

- [ ] `poetry check` passes
- [ ] All required dependencies listed
- [ ] Dev dependencies separate from runtime
- [ ] Ruff configuration valid
- [ ] `.gitignore` prevents committing secrets

### Integration

- [ ] Poetry lock file exists (reproducible builds)
- [ ] Package discoverable by Poetry
- [ ] Virtual environment created
- [ ] All tools (pytest, ruff, jupyter) available

---

## Expected Approach (Ideal Path)

### Step 1: Initialize Poetry Project

```bash
# Create project directory
mkdir ead-langchain-template
cd ead-langchain-template

# Initialize git (recommended)
git init

# Initialize Poetry
poetry init

# Answer prompts:
# - Package name: langchain-llm
# - Version: 0.1.0
# - Description: LangChain LLM utilities for EAD LangChain Template
# - Author: [Your details or skip]
# - License: [Choose or skip]
# - Python: ^3.10
# - Interactive dependency input: no (we'll add manually)
```

### Step 2: Configure src-layout in pyproject.toml

Edit `pyproject.toml`, add:
```toml
[tool.poetry]
# ... existing fields ...
packages = [{include = "langchain_llm", from = "src"}]
```

### Step 3: Add Dependencies

```bash
# Runtime dependencies
poetry add langchain-core
poetry add langchain-openai
poetry add langchain-anthropic
poetry add langchain-google-genai
poetry add python-dotenv

# Development dependencies
poetry add --group dev pytest
poetry add --group dev pytest-cov
poetry add --group dev ruff
poetry add --group dev jupyter
poetry add --group dev ipykernel
```

### Step 4: Create Directory Structure

```bash
# Create directories
mkdir -p src/langchain_llm
mkdir -p examples
mkdir -p tests/enforcement
mkdir -p .github
mkdir -p logs  # For runtime logs

# Create empty __init__.py files
touch src/langchain_llm/__init__.py
touch tests/__init__.py
touch tests/enforcement/__init__.py
```

### Step 5: Create .gitignore

Create `.gitignore` file with content from Requirements section above.

### Step 6: Add Ruff Configuration

Edit `pyproject.toml`, add Ruff sections from Requirements above.

### Step 7: Generate requirements.txt

```bash
poetry export -f requirements.txt -o requirements.txt --without-hashes
```

### Step 8: Validate Setup

```bash
# Verify Poetry configuration
poetry check

# Install dependencies
poetry install

# Activate environment
poetry shell

# Test import (should work even though package is empty)
python -c "import langchain_llm; print('Package imported successfully!')"

# Test that dev tools are available
pytest --version
ruff --version
jupyter --version

# Exit Poetry shell
exit
```

---

## Testing Strategy

### Validation Commands

```bash
# 1. Poetry validity
poetry check
# Expected: All set!

# 2. Dependencies installed
poetry install
# Expected: No errors, creates/updates poetry.lock

# 3. Package importable
poetry run python -c "import langchain_llm"
# Expected: No errors

# 4. Directory structure
ls -la src/langchain_llm/
ls -la tests/enforcement/
ls -la examples/
# Expected: All directories exist

# 5. Tools available
poetry run pytest --version
poetry run ruff --version
poetry run jupyter --version
# Expected: All tools found

# 6. Ruff configuration valid
poetry run ruff check --help
# Expected: Help text, no errors

# 7. Git ignores .env
touch .env
git status
# Expected: .env not listed in untracked files
rm .env
```

### Manual Checks

- [ ] Open `pyproject.toml`, verify all fields correct
- [ ] Check `poetry.lock` exists and has content
- [ ] Verify `.gitignore` covers all necessary files
- [ ] Check `requirements.txt` generated and complete

---

## Troubleshooting

### Common Issues

**Issue**: Poetry init fails
**Solution**: Ensure Poetry installed correctly: `poetry --version`

**Issue**: Python version mismatch
**Solution**: Use pyenv or specify Python path: `poetry env use /path/to/python3.10`

**Issue**: Dependencies fail to install
**Solution**: Clear Poetry cache: `poetry cache clear pypi --all` then retry

**Issue**: Package not importable after install
**Solution**: Check `packages` configuration in pyproject.toml, ensure `from = "src"`

**Issue**: Virtual environment not activated
**Solution**: Run `poetry shell` or prefix commands with `poetry run`

**Issue**: requirements.txt export fails
**Solution**: Ensure poetry.lock exists first: `poetry lock`

**Issue**: Git still tracks .env
**Solution**: If .env was previously committed, remove from git: `git rm --cached .env`

### Diagnostic Commands

```bash
# Show Poetry configuration
poetry config --list

# Show virtual environment location
poetry env info

# List installed packages
poetry show

# Check for dependency conflicts
poetry check

# Show project info
poetry about
```

---

## Output Examples

### Expected pyproject.toml Structure

```toml
[tool.poetry]
name = "langchain-llm"
version = "0.1.0"
description = "EAD template for building LLM applications with LangChain"
authors = ["Your Name <your.email@example.com>"]
packages = [{include = "langchain_llm", from = "src"}]

[tool.poetry.dependencies]
python = "^3.10"
langchain-core = "^0.3.0"
langchain-openai = "^0.2.0"
langchain-anthropic = "^0.3.0"
langchain-google-genai = "^2.0.0"
python-dotenv = "^1.0.0"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0.0"
pytest-asyncio = "^0.23.0"
pytest-cov = "^7.0.0"
ruff = "^0.8.0"
jupyter = "^1.1.0"
ipykernel = "^6.29.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.ruff]
line-length = 130
target-version = "py310"
# ... rest of Ruff config ...
```

### Expected Directory Tree

```
ead-langchain-template/
├── .git/
├── .gitignore
├── pyproject.toml
├── poetry.lock
├── requirements.txt
├── src/
│   └── langchain_llm/
│       └── __init__.py
├── examples/
├── tests/
│   ├── __init__.py
│   └── enforcement/
│       └── __init__.py
├── docs/
│   └── complete/
│       ├── requirements/
│       ├── designs/
│       ├── phases/
│       └── tasks/
└── .github/
```

---

## Next Steps

After completing this task:

1. **Commit Your Work**:
   ```bash
   git add .
   git commit -m "Task 001: Initialize Poetry project with structure"
   ```

2. **Verify Success**:
   - All success criteria checked
   - Poetry install works
   - Package importable

3. **Move to Task 002**:
   - Setup GitHub and write copilot instructions
   - Build on the structure created here

---

## Related Documents

**Design References**:
- [001-project-structure.md](../designs/001-project-structure.md) - Directory layout details
- [002-technical-requirements.md](../requirements/002-technical-requirements.md) - Tech stack

**Phase Overview**:
- [phase-01-project-foundation.md](../phases/phase-01-project-foundation.md)

**Next Task**:
- [task-002-setup-github-write-copilot-instructions.md](task-002-setup-github-write-copilot-instructions.md)

---

## Document Metadata

- **Task ID**: 001
- **Phase**: 01 - Project Foundation
- **Complexity**: Medium
- **LOC Output**: ~400 lines (configuration files + directory structure)
- **Prerequisites**: None (first task)
- **Validates**: Project can be set up correctly
