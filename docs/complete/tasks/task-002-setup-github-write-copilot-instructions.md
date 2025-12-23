# Task 002: Setup GitHub and Write Copilot Instructions

## Task Context

**Phase**: 01 - Project Foundation
**Sequence**: Second task (after Poetry setup)
**Complexity**: Medium-High
**Output**: ~600 LOC (copilot-instructions.md + GitHub templates)

### Why This Task Exists

AI coding assistants (GitHub Copilot, Claude Code, etc.) need explicit guidelines to:
- Follow project conventions
- Generate compliant code
- Understand design decisions
- Apply correct patterns

Without these guidelines, AI assistants will:
- Use wrong environment variable names
- Generate Google-style docstrings (we require Sphinx)
- Skip TDD
- Violate code standards

### Where This Fits

```
Task 001 → Task 002 (YOU ARE HERE) → Task 003 → ... → Task 014
Poetry     GitHub + Copilot          .env      Core      README
```

---

## Prerequisites

### Completed Tasks

- [x] **Task 001**: Poetry project initialized, directory structure created

### Required Knowledge

**GitHub Structure**:
- What `.github/` directory is for
- Issue templates purpose
- PR templates purpose

**AI Assistant Behavior**:
- How GitHub Copilot reads copilot-instructions.md
- How to write effective AI guidelines
- Common AI assistant mistakes

**Project Conventions** (from design docs):
- Environment variable naming (`EADLANGCHAIN_*`)
- Sphinx docstring requirement
- TDD workflow
- Code style standards

### Required Tools

- Text editor
- Access to design documents for reference

---

## Research Required

### GitHub Conventions

**Read**:
- GitHub issue template documentation
- GitHub PR template documentation
- GitHub Copilot workspace instructions format

**Key Concepts**:
- Issue template YAML frontmatter
- PR template markdown structure
- How Copilot discovers instructions

### AI Assistant Guidelines

**Study Examples**:
Look at other projects' copilot-instructions.md files for structure ideas (but adapt to our project, don't copy).

**Key Sections to Include**:
- Project overview
- Environment variable conventions
- TDD workflow
- Docstring standard (critical!)
- Code style
- Common pitfalls

---

## Code to Explore

### Reference Documents

**Must Read**:
- `docs/complete/requirements/003-environment-conventions.md` - Env var patterns
- `docs/complete/requirements/004-quality-requirements.md` - TDD requirements
- `docs/complete/designs/006-documentation-strategy.md` - Sphinx docstrings
- `docs/complete/designs/000-architecture-overview.md` - Design principles

### Patterns to Document

**Environment Variable Pattern**:
```bash
EADLANGCHAIN_<TYPE>_<KEY>
# Example: EADLANGCHAIN_AI_OPENAI_API_KEY
```

**Sphinx Docstring Pattern**:
```python
def function_name(param: str) -> str:
    """
    Brief description.

    :param param: Parameter description
    :ptype param: str
    :return: Return value description
    :rtype: str
    """
    pass
```

**TDD Pattern**:
```
1. RED: Write failing test
2. GREEN: Minimal implementation
3. REFACTOR: Improve code
```

---

## Task Description

### Objective

Create comprehensive AI assistant guidelines and GitHub project structure to ensure consistent code generation and contribution patterns.

### Requirements

#### 1. Create GitHub Directory Structure

```
.github/
├── copilot-instructions.md     # AI assistant guidelines (MAIN DELIVERABLE)
├── ISSUE_TEMPLATE/
│   ├── bug_report.md
│   └── feature_request.md
└── PULL_REQUEST_TEMPLATE.md    # Optional but recommended
```

#### 2. Write copilot-instructions.md

**Required Sections** (~600 lines total):

**Section 1: Project Overview** (50 lines):
- What this project is
- Educational template for LangChain
- Thin utility layer philosophy
- Target audience

**Section 2: Environment Variables Convention** (100 lines):
- `EADLANGCHAIN_<TYPE>_<KEY>` pattern  (**CRITICAL**)
- Why we don't use generic names
- Examples for each type (AI, LOG, etc.)
- How to add new variables

**Section 3: Package Management** (60 lines):
- Poetry primary, pip alternative
- Installation commands
- Adding dependencies

**Section 4: Test-Driven Development** (120 lines):
- Red-Green-Refactor cycle
- When to use TDD (all src/ code)
- Example workflow
- Running tests

**Section 5: LangChain Usage** (80 lines):
- Use LangChain directly, don't wrap
- Always pass API keys explicitly
- Provider-agnostic patterns

**Section 6: Code Style** (60 lines):
- Ruff configuration
- Line length (130 chars)
- Import ordering

**Section 7: Docstring Standard - MANDATORY** (150 lines):
- **Sphinx-style ONLY**
- Google/NumPy styles are FORBIDDEN
- Enforcement tests will fail
- Complete examples (function, class, module)
- Common mistakes

**Section 8: Project Structure** (50 lines):
- Directory layout
- Where files go
- Src-layout importance

**Section 9: Common Patterns** (80 lines):
- Adding utility function
- Adding example
- Adding environment variable

**Section 10: Common Pitfalls** (50 lines):
- Don't use generic env vars
- Don't skip tests
- Don't use emojis in code
- Don't use Google/NumPy docstrings

**Section 11: IMPORTANT - No Phase/Task References** (40 lines):
**CRITICAL**: Add this section:
```markdown
## Code Content Guidelines

**IMPORTANT**: Code, comments, and docstrings must NOT reference:
- Phase numbers (e.g., "Phase 02", "This is phase 3")
- Task numbers (e.g., "Task 005", "Completed in task 12")
- Project management artifacts

**Why**: These are internal project organization tools. Code should be
self-explanatory and reference concepts, not project scaffolding.

**Bad Examples**:
```python
# Phase 02: Implement configuration
def load_config():
    pass

# TODO: Complete in Task 015
def advanced_feature():
    pass
```

**Good Examples**:
```python
# Load configuration from environment variables
def load_config():
    pass

# TODO: Implement advanced callback features
def advanced_feature():
    pass
```

Use conceptual references ("configuration module", "logging system")
not organizational references ("Phase 2", "Task 5").
```

#### 3. Create Issue Templates

**Bug Report** (`ISSUE_TEMPLATE/bug_report.md`):
```markdown
---
name: Bug Report
about: Report a bug in the template
title: "[BUG] "
labels: bug
assignees: ''
---

## Describe the Bug
A clear description of what the bug is.

## To Reproduce
Steps to reproduce the behavior:
1. Go to '...'
2. Run command '...'
3. See error

## Expected Behavior
What you expected to happen.

## Environment
- Python version:
- Poetry version:
- OS:
- Relevant API provider:

## Additional Context
Add any other context about the problem here.
```

**Feature Request** (`ISSUE_TEMPLATE/feature_request.md`):
```markdown
---
name: Feature Request
about: Suggest a new feature or improvement
title: "[FEATURE] "
labels: enhancement
assignees: ''
---

## Feature Description
Clear description of the feature you'd like to see.

## Use Case
Why is this feature needed? What problem does it solve?

## Proposed Solution
How do you think this should be implemented?

## Alternatives Considered
What other approaches did you consider?

## Additional Context
Add any other context or screenshots about the feature request here.
```

#### 4. Create PR Template (Optional)

**Pull Request** (`.github/PULL_REQUEST_TEMPLATE.md`):
```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Testing
- [ ] Tests added/updated
- [ ] All tests pass (`pytest`)
- [ ] Coverage maintained (>80%)

## Code Quality
- [ ] Ruff check passes (`ruff check .`)
- [ ] Ruff format applied (`ruff format .`)
- [ ] Sphinx docstrings added
- [ ] No emojis in code

## Checklist
- [ ] Followed TDD workflow
- [ ] Updated README if needed
- [ ] No secrets committed
```

### Constraints

- copilot-instructions.md MUST be comprehensive (500+ lines)
- Sphinx docstring requirement MUST be emphasized heavily
- Environment variable convention MUST be clear
- No phase/task references in example code
- Examples must be correct and runnable

---

## Success Criteria

### Functional

- [ ] `.github/` directory created
- [ ] `copilot-instructions.md` complete and comprehensive (500+ lines)
- [ ] Issue templates created (bug report, feature request)
- [ ] PR template created (optional)
- [ ] All example code in instructions is correct

### Quality

- [ ] copilot-instructions.md covers all critical conventions
- [ ] Sphinx docstring requirement heavily emphasized
- [ ] TDD workflow clearly explained
- [ ] Environment variable pattern crystal clear
- [ ] Common pitfalls documented
- [ ] No phase/task references in examples

### Integration

- [ ] GitHub Copilot can discover copilot-instructions.md
- [ ] Issue templates appear in GitHub UI (when repo created)
- [ ] PR template auto-loads (when repo created)

---

## Expected Approach (Ideal Path)

### Step 1: Create GitHub Directory

```bash
# From project root
mkdir -p .github/ISSUE_TEMPLATE
```

### Step 2: Write copilot-instructions.md

Create `.github/copilot-instructions.md`:

```markdown
# GitHub Copilot Instructions for EAD LangChain Template

This file provides guidance to GitHub Copilot and other AI coding assistants
when working with this project.

## Project Overview

This is a template for building LLM applications using LangChain during the
EAD LangChain Template. The template provides:
- Clean project structure with proper packaging
- Standardized logging with custom formatting
- Configuration management for API keys
- Progressive examples from basic to advanced usage
- Test infrastructure with pytest

[Continue with all sections from Requirements...]
```

**Key Sections to Emphasize**:

1. **Environment Variables** (make this very clear):
```markdown
## Environment Variables Convention

**IMPORTANT:** All environment variables MUST use the `EADLANGCHAIN_` prefix.

### Pattern
```bash
EADLANGCHAIN_<TYPE>_<KEY>
```

### Examples
```bash
# AI Provider Keys
EADLANGCHAIN_AI_OPENAI_API_KEY=sk-...
EADLANGCHAIN_AI_ANTHROPIC_API_KEY=sk-ant-...
EADLANGCHAIN_AI_GEMINI_API_KEY=...

# Logging
EADLANGCHAIN_LOG_LEVEL=INFO
EADLANGCHAIN_LOG_FILE=logs/app.log
```

### Why?
- Prevents conflicts with system/other project variables
- Clear ownership
- Professional pattern

### Never Use
```bash
# ❌ WRONG - Too generic
OPENAI_API_KEY=...
API_KEY=...
LOG_LEVEL=...
```
```

2. **Sphinx Docstrings** (emphasize heavily):
```markdown
## Docstrings - MANDATORY Sphinx Format

This project **REQUIRES** Sphinx-style docstrings.
Google-style (Args:, Returns:) and NumPy-style are **NOT ALLOWED**
and will cause enforcement tests to fail.

### Required Format

```python
def function_name(param1: str, param2: int) -> str:
    """
    Brief description of function.

    Longer description can go here. Multiple paragraphs are fine.

    :param param1: Description of param1
    :ptype param1: str
    :param param2: Description of param2
    :ptype param2: int
    :return: Description of return value
    :rtype: str
    :raises ValueError: When param1 is invalid

    Example usage::

        result = function_name("test", 42)
        print(result)
    """
    pass
```

### What NOT to Use

```python
# ❌ WRONG - Google-style (will fail enforcement tests)
def bad_function(param):
    """
    Args:
        param: Some parameter

    Returns:
        Some value
    """
    pass

# ❌ WRONG - NumPy-style (will fail enforcement tests)
def bad_function(param):
    """
    Parameters
    ----------
    param : str
        Some parameter

    Returns
    -------
    str
        Some value
    """
    pass
```

### Enforcement

Tests scan all .py files and fail if non-Sphinx docstrings are found.
Run `pytest tests/enforcement/` to check.
```

3. **No Phase/Task References** (new section):
```markdown
## Code Content Guidelines

**IMPORTANT**: Code, comments, and docstrings must NOT reference phases or tasks.

### Why?
Phases and tasks are project management scaffolding. Code should reference
concepts, not organizational structures.

### Examples

**Bad** (references phase/task):
```python
# Phase 02: Configuration implementation
class Config:
    pass

# TODO: Complete in Task 015
def feature():
    pass
```

**Good** (references concepts):
```python
# Configuration management using environment variables
class Config:
    pass

# TODO: Implement advanced callback features
def feature():
    pass
```

Use: "configuration module", "logging system", "example implementation"
Don't use: "Phase 2", "Task 5", "step 3 of the plan"
```

### Step 3: Create Issue Templates

Create `.github/ISSUE_TEMPLATE/bug_report.md` and `feature_request.md`
with content from Requirements section.

### Step 4: Create PR Template

Create `.github/PULL_REQUEST_TEMPLATE.md` with content from Requirements section.

### Step 5: Validate

```bash
# Check files exist
ls -la .github/
ls -la .github/ISSUE_TEMPLATE/

# Check copilot-instructions.md is comprehensive
wc -l .github/copilot-instructions.md
# Should be 500+ lines

# Check for common sections
grep -i "sphinx" .github/copilot-instructions.md
grep -i "EADLANGCHAIN" .github/copilot-instructions.md
grep -i "TDD" .github/copilot-instructions.md
```

---

## Testing Strategy

### Validation Commands

```bash
# 1. Files exist
test -f .github/copilot-instructions.md && echo "✓ copilot-instructions.md exists"
test -f .github/ISSUE_TEMPLATE/bug_report.md && echo "✓ Bug template exists"
test -f .github/ISSUE_TEMPLATE/feature_request.md && echo "✓ Feature template exists"

# 2. copilot-instructions.md is comprehensive
line_count=$(wc -l < .github/copilot-instructions.md)
if [ $line_count -gt 500 ]; then
    echo "✓ copilot-instructions.md is comprehensive ($line_count lines)"
else
    echo "✗ copilot-instructions.md too short ($line_count lines, need 500+)"
fi

# 3. Key sections present
grep -q "EADLANGCHAIN" .github/copilot-instructions.md && echo "✓ Env var section present"
grep -q "Sphinx" .github/copilot-instructions.md && echo "✓ Docstring section present"
grep -q "TDD" .github/copilot-instructions.md && echo "✓ TDD section present"

# 4. Issue templates have YAML frontmatter
head -n 1 .github/ISSUE_TEMPLATE/bug_report.md | grep -q "---" && echo "✓ Bug template has frontmatter"
```

### Manual Review

- [ ] Read copilot-instructions.md start to finish
- [ ] Verify all critical conventions documented
- [ ] Check all code examples are correct
- [ ] Verify no phase/task references in examples
- [ ] Ensure Sphinx requirement is crystal clear

---

## Troubleshooting

### Common Issues

**Issue**: copilot-instructions.md feels incomplete
**Solution**: Check against design docs, ensure all conventions covered

**Issue**: Unsure what to emphasize
**Solution**: Emphasize things AI commonly gets wrong (env vars, docstrings, TDD)

**Issue**: Examples in instructions have errors
**Solution**: Test all code examples in Python REPL before including

**Issue**: Too wordy, AI won't read it all
**Solution**: Use clear headers, bullet points, code examples. AI handles long docs fine.

---

## Output Example

### copilot-instructions.md Structure

```markdown
# GitHub Copilot Instructions for EAD LangChain Template

## Project Overview
[50 lines: What this is, purpose, scope]

## Environment Variables Convention
[100 lines: EADLANGCHAIN_* pattern, examples, why]

## Package Management
[60 lines: Poetry primary, pip alternative]

## Test-Driven Development (TDD)
[120 lines: Red-Green-Refactor, examples, when to use]

## LangChain Usage
[80 lines: Use directly, don't wrap, patterns]

## Code Style
[60 lines: Ruff, line length, imports]

## Docstrings - MANDATORY Sphinx Format
[150 lines: Required format, what NOT to use, examples, enforcement]

## Project Structure
[50 lines: Directory layout, where files go]

## Common Patterns
[80 lines: Adding functions, examples, env vars]

## Common Pitfalls
[50 lines: What NOT to do]

## Code Content Guidelines
[40 lines: No phase/task references]

Total: ~600-700 lines
```

---

## Next Steps

After completing this task:

1. **Commit Your Work**:
   ```bash
   git add .github/
   git commit -m "Add GitHub structure and copilot instructions"
   ```

2. **Verify GitHub Copilot Can Read It**:
   - Open any Python file
   - Start typing, see if Copilot follows conventions
   - (May need to reload IDE/editor)

3. **Move to Task 003**:
   - Create .env.example
   - Document all environment variables

---

## Related Documents

**Design References**:
- [006-documentation-strategy.md](../designs/006-documentation-strategy.md) - Documentation standards
- [003-environment-conventions.md](../requirements/003-environment-conventions.md) - Env var patterns
- [004-quality-requirements.md](../requirements/004-quality-requirements.md) - TDD requirements

**Phase Overview**:
- [phase-01-project-foundation.md](../phases/phase-01-project-foundation.md)

**Previous/Next Tasks**:
- [task-001-initialize-project.md](task-001-initialize-project.md) - Previous
- [task-003-create-env-example.md](task-003-create-env-example.md) - Next

---

## Document Metadata

- **Task ID**: 002
- **Phase**: 01 - Project Foundation
- **Complexity**: Medium-High
- **LOC Output**: ~600-700 lines (copilot-instructions + templates)
- **Prerequisites**: Task 001 complete
- **Validates**: AI assistants have proper guidelines
