# Design 006: Documentation Strategy

## Document Purpose

This document specifies the complete documentation strategy for the EAD LangChain Template, including docstring standards, README structure, AI assistant guidelines, and documentation maintenance.

---

## Overview

### Documentation Layers

The project has four documentation layers:

1. **Inline Documentation** (Code):
   - Sphinx-style docstrings for all functions/classes
   - Type hints for all signatures
   - Comments explaining WHY (not what)

2. **User-Facing Documentation** (README.md):
   - Quick start guide
   - Installation instructions
   - Usage examples
   - Troubleshooting

3. **AI Assistant Guidelines** (.github/copilot-instructions.md):
   - Project conventions
   - TDD workflow
   - Code patterns
   - Environment variable standards

4. **API Documentation** (Future):
   - Auto-generated from docstrings using Sphinx
   - Hosted documentation site
   - Module/class/function reference

---

## Sphinx Docstring Standard

### Why Sphinx?

**Chosen Over**:
- Google-style (Args:, Returns:)
- NumPy-style (Parameters section with dashes)
- Plain docstrings

**Reasons**:
- Industry standard for Python
- Sphinx tool support (auto-generate docs)
- Precise, structured format
- Type information included

**Enforcement**: Automated tests reject non-Sphinx docstrings

### Sphinx Docstring Format

#### Function Docstrings

**Template**:
```python
def function_name(param1: str, param2: int = 0) -> str | None:
    """
    Brief one-line description.

    Longer description can go here. Multiple paragraphs are fine.
    Explain what the function does, why it exists, and when to use it.

    :param param1: Description of param1
    :ptype param1: str
    :param param2: Description of param2 (optional, defaults to 0)
    :ptype param2: int
    :return: Description of return value
    :rtype: str | None
    :raises ValueError: When param1 is empty
    :raises ConfigError: When configuration is invalid

    Example usage::

        result = function_name("test", 42)
        if result:
            print(result)

    .. note::
        Additional notes can go in special directives.

    .. warning::
        Warnings about potential issues or gotchas.
    """
    pass
```

**Required Elements**:
- Brief description (first line)
- `:param` for each parameter
- `:ptype` for each parameter type
- `:return` if function returns value
- `:rtype` for return type
- `:raises` for each exception that may be raised

**Optional Elements**:
- Longer description (paragraph 2+)
- `Example usage::` code block
- `.. note::` special notes
- `.. warning::` warnings
- `.. seealso::` related functions

#### Class Docstrings

**Template**:
```python
class MyClass:
    """
    Brief description of class.

    Longer description of the class purpose, behavior, and usage.
    Explain what problem it solves and how it fits into the system.

    :param name: Constructor parameter description
    :ptype name: str
    :param value: Another parameter description
    :ptype value: int

    Example usage::

        obj = MyClass("test", 42)
        result = obj.process()

    Attributes:
        name: The name attribute
        value: The value attribute
        computed: Computed attribute based on name and value
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
        self.computed = f"{name}_{value}"

    def process(self, data: str) -> bool:
        """
        Process the data.

        :param data: Data to process
        :ptype data: str
        :return: True if successful
        :rtype: bool
        :raises ValueError: If data is empty
        """
        if not data:
            raise ValueError("Data cannot be empty")
        return True
```

#### Module Docstrings

**Template**:
```python
"""
Module for handling configuration.

This module provides utilities for loading and managing
configuration from environment variables. It implements the
ConfigProvider protocol and provides convenience functions
for common configuration tasks.

Example usage::

    from langchain_llm import load_env_config, get_api_key

    load_env_config()
    api_key = get_api_key("openai")

Functions:
    load_env_config: Load environment variables from .env file
    get_api_key: Retrieve API key for a provider
    get_all_api_keys: Get all configured API keys
    validate_provider: Validate provider configuration

Classes:
    EnvConfigProvider: Configuration from environment variables
    ConfigError: Configuration-related exceptions
"""
```

### Type Hints Requirement

**All function signatures must include type hints**:

```python
from typing import Any

def example(
    name: str,
    count: int,
    items: list[str],
    metadata: dict[str, Any] | None = None,
) -> bool:
    """Function with comprehensive type hints."""
    pass
```

**Benefits**:
- IDE autocomplete
- Static type checking (mypy)
- Documentation (types visible in signature)
- Catches type errors early

---

## README.md Structure

### Required Sections

```markdown
# Project Title

Brief project description (1-2 sentences)

## Features

- Feature 1
- Feature 2
- Feature 3

## Quick Start

### Prerequisites
- Python 3.10+
- API keys for at least one provider

### Installation

#### Option 1: Poetry (Recommended)
[Installation steps]

#### Option 2: pip with venv
[Installation steps]

### Configuration
[.env setup steps]

### Run Your First Example
[Quick win - get something running fast]

## Project Structure
[Directory tree with explanations]

## Examples
[Description of each example with code snippets]

## Environment Variables
[Complete list with examples]

## Development
[Testing, linting, contributing]

## Troubleshooting
[Common issues and solutions]

## Resources
[External links]

## Contributing
[How to contribute]

## License
[License info]

## Support
[How to get help]
```

### README Best Practices

**Quick Win First**:
- Users should be able to run something in <10 minutes
- "Quick Start" section comes early
- Clear, sequential steps

**Progressive Disclosure**:
- Essential info first (installation, quick start)
- Details later (advanced features, troubleshooting)
- Table of contents for long READMEs

**Working Examples**:
- All code snippets must work
- Test them manually
- Keep them updated

**Visual Elements**:
- Code blocks with syntax highlighting
- Clear section headers
- Bullet points for lists
- Badges (optional): build status, coverage

### README Maintenance

**Update When**:
- Adding new features
- Changing installation process
- New dependencies added
- API changes
- User-reported issues

**Review Checklist**:
- [ ] All installation steps work
- [ ] All code examples run
- [ ] Links are not broken
- [ ] Environment variables documented
- [ ] Troubleshooting current

---

## .github/copilot-instructions.md

### Purpose

Guide AI coding assistants (GitHub Copilot, Claude Code, etc.) to:
- Follow project conventions
- Generate compliant code
- Understand architecture decisions
- Apply correct patterns

### Structure

```markdown
# GitHub Copilot Instructions for EAD LangChain Template

## Project Overview
[What this project is]

## Environment Variables Convention
[EADLANGCHAIN_* pattern, why, examples]

## Package Management
[Poetry primary, pip alternative]

## Test-Driven Development (TDD)
[TDD workflow, Red-Green-Refactor]

## LangChain Usage
[Use LangChain directly, don't wrap it]

## Code Style
[Ruff configuration, line length, imports]

## Docstring Standard - MANDATORY
[Sphinx-style only, enforcement, examples]

## Project Structure
[Directory layout, where files go]

## Common Patterns
[Adding utility function, new example, new env var]

## Common Pitfalls
[What NOT to do]

## Getting Help
[Where to look for answers]
```

### Key Sections

#### Environment Variables Convention

**Must Document**:
- `EADLANGCHAIN_<TYPE>_<KEY>` pattern
- Examples for each type (AI, LOG, etc.)
- Why we don't use generic names
- How to add new variables

**Example**:
```markdown
## Environment Variables Convention

**IMPORTANT:** All environment variables MUST use the `EADLANGCHAIN_` prefix.

Pattern: `EADLANGCHAIN_<TYPE>_<KEY>`

Examples:
- `EADLANGCHAIN_AI_OPENAI_API_KEY` - OpenAI API key
- `EADLANGCHAIN_LOG_LEVEL` - Logging level

**Why?** Prevents conflicts, clear ownership, professional pattern.

**Never use**: `OPENAI_API_KEY`, `API_KEY`, etc. (too generic)
```

#### Sphinx Docstring Requirement

**Must Emphasize**:
- Sphinx-style is mandatory
- Google/NumPy styles are forbidden
- Enforcement tests will fail
- Examples of correct format

**Example**:
```markdown
## Docstrings - MANDATORY Sphinx Format

This project **REQUIRES** Sphinx-style docstrings.

**Allowed**:
```python
def example(param: str) -> str:
    """
    Brief description.

    :param param: Parameter description
    :ptype param: str
    :return: Return value description
    :rtype: str
    """
    pass
```

**NOT Allowed**:
```python
def example(param: str) -> str:
    """
    Brief description.

    Args:
        param: Parameter description

    Returns:
        Return value description
    """
    pass
```

Enforcement: Tests scan all .py files and fail if non-Sphinx docstrings found.
```

#### TDD Workflow

**Must Explain**:
- Red-Green-Refactor cycle
- Write test first
- Minimal implementation
- When to refactor

**Example**:
```markdown
## Test-Driven Development (TDD)

All code in `src/langchain_llm/` MUST follow TDD.

Workflow:
1. **Red**: Write failing test
2. **Green**: Write minimal code to pass
3. **Refactor**: Improve while keeping tests green
4. **Repeat**: Next feature

Example:
```python
# Step 1: Write test (RED)
def test_new_feature():
    result = new_feature()
    assert result == expected

# Step 2: Run test - should fail
pytest tests/test_module.py::test_new_feature

# Step 3: Implement (GREEN)
def new_feature():
    return expected

# Step 4: Test passes - now refactor
```

---

## Example Code Documentation

### Examples Should Have

**Module Docstring**:
```python
"""
Example 01: Basic LLM Usage

This example demonstrates the simplest possible way to use LangChain
with different providers. Just prompt → response, no complexity.

Shows:
- Loading configuration
- Setting up logging
- Basic invocation with OpenAI, Anthropic, and Gemini

Prerequisites:
- At least one API key configured in .env
- Python 3.10+
"""
```

**Function Docstrings**:
```python
def basic_openai_example():
    """
    Simple example using OpenAI.

    Demonstrates:
    - Getting API key from environment
    - Creating ChatOpenAI instance
    - Basic invoke pattern
    - Handling response
    """
    pass
```

**Inline Comments** (explain WHY, not WHAT):
```python
# Use temperature=0.7 for more creative responses
llm = ChatOpenAI(temperature=0.7)

# Longer prompt to make streaming effect visible
prompt = "Explain the history of AI in 3 paragraphs."
```

---

## .env.example Documentation

### Structure

```bash
# ============================================================================
# Section Header (clearly separated)
# ============================================================================

# Variable Name
# Human-readable description of what this does
# Get it from: https://example.com/link (if applicable)
# Default: value (if has default)
# Optional/Required: mark if optional
EADLANGCHAIN_VARIABLE_NAME=example-value-here

# Another variable in same section
EADLANGCHAIN_ANOTHER_VARIABLE=another-example

# ============================================================================
# Next Section
# ============================================================================
```

### Best Practices

**Clear Headers**:
- Separate logical groups
- Use visual dividers (=== lines)
- Descriptive section names

**Helpful Comments**:
- Explain what each variable does
- Link to docs to get values (API keys)
- Show example values
- Note if optional

**Example**:
```bash
# ============================================================================
# AI Provider API Keys (at least one required)
# ============================================================================

# OpenAI API Key (Required for OpenAI examples)
# Sign up at: https://platform.openai.com
# Get your key: https://platform.openai.com/api-keys
EADLANGCHAIN_AI_OPENAI_API_KEY=your-openai-api-key-here

# ============================================================================
# Optional Configuration
# ============================================================================

# Logging Level (Default: INFO)
# Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
# EADLANGCHAIN_LOG_LEVEL=INFO
```

---

## Documentation Maintenance

### When to Update Documentation

**Code Changes**:
- New function added → Add docstring
- API changed → Update docstring and README
- New feature → Update README examples

**User Feedback**:
- Confusing instructions → Clarify
- Missing info → Add section
- Common question → Add to troubleshooting

**Dependencies**:
- New dependency → Update installation instructions
- Version change → Update requirements
- Breaking change → Update migration guide

### Documentation Review Checklist

**Before Commit**:
- [ ] All new functions have Sphinx docstrings
- [ ] Type hints added
- [ ] README updated if public API changed
- [ ] .env.example updated if new env vars
- [ ] Examples still work

**Before Release**:
- [ ] README quick start tested
- [ ] All code examples run
- [ ] Links checked
- [ ] Version numbers updated
- [ ] CHANGELOG updated (if exists)

---

## Future: Auto-Generated API Docs

### Sphinx Documentation (Future Enhancement)

**Setup**:
```bash
# Install Sphinx
poetry add --group dev sphinx sphinx-rtd-theme

# Generate docs
cd docs
sphinx-quickstart
```

**Configuration** (docs/conf.py):
```python
extensions = [
    'sphinx.ext.autodoc',       # Auto-generate from docstrings
    'sphinx.ext.napoleon',      # Support Sphinx style
    'sphinx.ext.viewcode',      # Link to source code
    'sphinx.ext.intersphinx',   # Link to other docs
]

html_theme = 'sphinx_rtd_theme'
```

**Build Docs**:
```bash
cd docs
make html
# Output: docs/_build/html/index.html
```

**Host**: GitHub Pages, Read the Docs, or similar

### Auto-Generated Benefits

**For Users**:
- Searchable API reference
- Cross-linked documentation
- Examples embedded in docs
- Always up-to-date (generated from code)

**For Maintainers**:
- Single source of truth (docstrings)
- Automated updates
- Less manual documentation
- Catches missing docstrings

---

## Documentation Standards Summary

### Mandatory

- [ ] **All functions**: Sphinx docstrings
- [ ] **All parameters**: `:param` and `:ptype`
- [ ] **All returns**: `:return` and `:rtype`
- [ ] **All exceptions**: `:raises`
- [ ] **All signatures**: Type hints
- [ ] **No Google/NumPy style**: Enforced by tests
- [ ] **No emojis in code**: Enforced by tests

### Recommended

- [ ] **Examples in docstrings**: Code blocks showing usage
- [ ] **Module docstrings**: Every .py file has module doc
- [ ] **Class docstrings**: Purpose and usage
- [ ] **Complex logic**: Inline comments explaining WHY

### Documentation Files

- [ ] **README.md**: User-facing, comprehensive
- [ ] **.github/copilot-instructions.md**: AI assistant guide
- [ ] **.env.example**: All env vars documented
- [ ] **docs/complete/**: AI-executable blueprints (this project!)

---

## Related Documents

- **Previous**: [005-testing-strategy.md](005-testing-strategy.md) - Testing strategy
- **Next**: [phases/phase-01-project-setup.md](../phases/phase-01-project-setup.md) - Implementation phases
- **See Also**:
  - [requirements/004-quality-requirements.md](../requirements/004-quality-requirements.md) - Quality requirements
  - [000-architecture-overview.md](000-architecture-overview.md) - Architecture

## Document Metadata

- **Version**: 1.0
- **Status**: Active
- **Owner**: EAD LangChain Template Team
