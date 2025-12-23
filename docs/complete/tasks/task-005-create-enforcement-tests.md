# Task 005: Create Enforcement Tests

## Task Context

**Phase**: 03 - Test Infrastructure Foundation
**Sequence**: Fifth task (second of Phase 03)
**Complexity**: Medium
**Output**: ~500 LOC (2 enforcement test files)

### Why This Task Exists

Code quality must be enforced automatically:
- **Sphinx-style docstrings**: Mandatory format for all code (no Google/NumPy styles)
- **No emoji characters**: Professional code, avoid encoding issues
- **Fail builds early**: Catch violations before they spread

These enforcement tests act as quality gates. They come early in the workflow so all subsequent code (tasks 006+) is checked against these standards from the start.

### Where This Fits

```
Task 004 → Task 005 (YOU ARE HERE) → Task 006 → Task 007 → Task 008
pytest     Enforcement               TDD Config  TDD Logging  Exports
setup      Tests                     Module      Module
```

---

## Prerequisites

### Completed Tasks

- [x] **Task 004**: pytest infrastructure configured

### Required Knowledge

**Python AST**:
- Abstract Syntax Trees for code analysis
- `ast.parse()`, `ast.NodeVisitor`
- Analyzing docstrings programmatically

**Regular Expressions**:
- Pattern matching for docstring styles
- Multiline matching

**Unicode**:
- Emoji character ranges
- Unicode code points

**pathlib**:
- Recursive file traversal with `.rglob()`
- Path manipulation

---

## Research Required

### Code from Prior Tasks

**Study from Task 004**:
- `tests/conftest.py`: Basic test structure
- `pyproject.toml`: pytest configuration (markers)
- Purpose: Understand test discovery and how pytest finds these tests

### No Module Code Exists Yet

Tasks 006-007 will create `src/langchain_llm/*.py` files. These enforcement tests will validate that code when it's created.

### External Documentation

**Python AST**:
- https://docs.python.org/3/library/ast.html
- AST visitor pattern
- Getting docstrings from nodes

**Unicode Emoji Ranges**:
- https://unicode.org/emoji/charts/full-emoji-list.html
- Emoji block specifications

---

## Task Description

### Objective

Create automated enforcement tests that scan all Python code for:
1. Non-Sphinx docstring styles (Google, NumPy)
2. Missing Sphinx elements in docstrings
3. Emoji characters in code/notebooks/config files

These tests fail the build if violations are found, ensuring code quality from task 006 onward.

### Requirements

#### 1. Create Enforcement Test Directory

```
tests/enforcement/
├── __init__.py
├── test_sphinx_docstrings.py
└── test_no_emojis.py
```

**tests/enforcement/__init__.py** (empty file):
```python
# Empty file - makes enforcement/ a test package
```

#### 2. Create test_sphinx_docstrings.py

This file must implement AST-based docstring checking.

**Required Sphinx Docstring Format** (to enforce):
```python
def example_function(name, value):
    """
    Brief description of function.

    :param name: Description of name parameter
    :ptype name: str
    :param value: Description of value parameter
    :ptype value: int
    :return: Description of return value
    :rtype: bool
    :raises ValueError: When value is invalid
    """
```

**Google-Style Patterns to Detect** (not allowed):
```
Args:
Arguments:
Returns:
Return:
Yields:
Raises:
Note:
Notes:
Example:
Examples:
Attributes:
```

**NumPy-Style Patterns to Detect** (not allowed):
```
Parameters
----------
Returns
-------
Yields
------
```

**Implementation Requirements**:

**Class: DocstringVisitor(ast.NodeVisitor)**
- Inherits from `ast.NodeVisitor`
- Visits function and class definitions
- Extracts and validates docstrings
- Records violations with file path and line number

**Methods**:
- `__init__(self, file_path)`: Store file path for error messages
- `visit_FunctionDef(self, node)`: Check function docstrings
- `visit_AsyncFunctionDef(self, node)`: Check async function docstrings
- `visit_ClassDef(self, node)`: Check class docstrings
- `_check_docstring(self, node, node_type)`: Core validation logic

**Validation Logic**:
1. Skip if no docstring AND (function is private OR is test function)
2. If docstring exists:
   - Check for Google-style patterns (regex multiline match)
   - Check for NumPy-style patterns (regex multiline match)
   - If function has parameters (excluding self/cls):
     - Verify `:param name:` directives present
     - Verify `:ptype name:` directives present
   - If function has return type hint:
     - Verify `:return:` directive present
     - Verify `:rtype:` directive present

**Google-Style Regex Patterns**:
```python
google_patterns = [
    r"^\s*Args:\s*$",
    r"^\s*Arguments:\s*$",
    r"^\s*Returns:\s*$",
    r"^\s*Return:\s*$",
    r"^\s*Yields:\s*$",
    r"^\s*Raises:\s*$",
    r"^\s*Note:\s*$",
    r"^\s*Notes:\s*$",
    r"^\s*Example:\s*$",
    r"^\s*Examples:\s*$",
    r"^\s*Attributes:\s*$",
]
```

**NumPy-Style Regex Patterns**:
```python
numpy_patterns = [
    r"^\s*Parameters\s*\n\s*-+\s*$",
    r"^\s*Returns\s*\n\s*-+\s*$",
    r"^\s*Yields\s*\n\s*-+\s*$",
    r"^\s*Raises\s*\n\s*-+\s*$",
]
```

**Helper Functions**:
- `check_file_docstrings(file_path)`: Parse file, visit AST, return violations
- `get_project_root()`: Navigate up from `tests/enforcement/` to project root

**Test Functions** (3 required):
- `test_sphinx_docstrings_in_src()`: Scan `src/` directory
- `test_sphinx_docstrings_in_tests()`: Scan `tests/` directory
- `test_sphinx_docstrings_in_examples()`: Scan `examples/` directory

**Error Message Format**:
```
DOCSTRING VIOLATIONS FOUND IN SOURCE CODE:
All functions and classes must use Sphinx-style docstrings.

Required format:
  :param name: description
  :ptype name: type
  :return: description
  :rtype: type
  :raises ExceptionType: description

Violations:
src/langchain_llm/config.py:42 - function 'get_api_key' uses Google-style docstring. Use Sphinx-style instead
src/langchain_llm/config.py:78 - function 'load_env' has parameters but docstring is missing :param directives
```

#### 3. Create test_no_emojis.py

This file must scan all code for emoji Unicode characters.

**Emoji Unicode Ranges** (to detect):
```python
emoji_ranges = [
    (0x1F600, 0x1F64F),  # Emoticons (😀-🙏)
    (0x1F300, 0x1F5FF),  # Misc Symbols and Pictographs (🌀-🗿)
    (0x1F680, 0x1F6FF),  # Transport and Map (🚀-🛿)
    (0x1F1E0, 0x1F1FF),  # Regional indicators (🇦-🇿 flags)
    (0x2600, 0x26FF),    # Misc symbols (☀-⛿)
    (0x2700, 0x27BF),    # Dingbats (✀-➿)
    (0xFE00, 0xFE0F),    # Variation Selectors
    (0x1F900, 0x1F9FF),  # Supplemental Symbols and Pictographs (🤀-🧿)
    (0x1F018, 0x1F270),  # Various symbols
    (0x238C, 0x2454),    # Misc items
    (0x20D0, 0x20FF),    # Combining Diacritical Marks for Symbols
]
```

**Implementation Requirements**:

**Function: is_emoji(char)**
- Check if a single character is an emoji
- Use `ord(char)` to get Unicode code point
- Check if code point falls in any emoji range
- Return True if emoji, False otherwise

**Function: find_emojis_in_text(text, file_path)**
- Scan text line by line
- For each character in each line, check if emoji
- Return list of (line_number, line_content, emoji_char) tuples

**Function: scan_python_file(file_path)**
- Read Python file with UTF-8 encoding
- Call `find_emojis_in_text()`
- Return violations

**Function: scan_notebook_file(file_path)**
- Read Jupyter notebook as JSON
- Extract all cell sources
- Scan each cell for emojis
- Return violations with cell context

**Function: scan_text_file(file_path)**
- Read config/text file with UTF-8 encoding
- Call `find_emojis_in_text()`
- Return violations

**Function: get_project_root()**
- Navigate up from `tests/enforcement/` to project root
- Return Path object

**Test Functions** (3 required):
- `test_no_emojis_in_python_files()`: Scan all `*.py` files (skip .venv, __pycache__)
- `test_no_emojis_in_notebook_files()`: Scan all `*.ipynb` files (skip checkpoints)
- `test_no_emojis_in_config_files()`: Scan `pyproject.toml`, `requirements.txt`

**Skip Patterns** (directories to ignore):
```python
skip_parts = [".venv", "venv", "__pycache__", ".tox", "build", "dist", ".pytest_cache", ".ipynb_checkpoints"]
```

**Error Message Format**:
```
EMOJI CHARACTERS FOUND IN PYTHON FILES:
Emojis are not allowed in code. Please remove them.

src/langchain_llm/config.py:15 - Found emoji '😀' in: print("Success! 😀")
examples/01_basic.py:42 - Found emoji '🚀' in: # Let's go! 🚀
```

### Constraints

- All functions must have Sphinx docstrings (these files demonstrate the standard)
- Use AST parsing, not regex, for Python syntax analysis
- Use pathlib for all file operations (not os.path)
- Tests must be fast (< 5 seconds total execution)
- Error messages must list ALL violations, not just first one

---

## Success Criteria

### Functional

- [ ] `tests/enforcement/` directory created
- [ ] `test_sphinx_docstrings.py` created with 3 test functions
- [ ] `test_no_emojis.py` created with 3 test functions
- [ ] Tests pass on current codebase: `pytest tests/enforcement/ -v`
- [ ] Tests catch violations when manually introduced

### Quality

- [ ] All functions have Sphinx docstrings (demonstrate the standard)
- [ ] Type hints on all functions
- [ ] `ruff check tests/enforcement/` passes
- [ ] Tests execute quickly (< 5 seconds)

### Integration

- [ ] pytest discovers enforcement tests
- [ ] Tests run as part of `pytest` command
- [ ] Error messages are clear and actionable
- [ ] Tests are ready to validate code from tasks 006+

---

## Expected Approach (Ideal Path)

### Step 1: Create Enforcement Directory

```bash
# From project root
mkdir -p tests/enforcement
touch tests/enforcement/__init__.py
```

### Step 2: Create test_sphinx_docstrings.py

**Start with imports and module docstring**:
```python
"""
Enforcement test: Sphinx-style docstrings required.

This test ensures all functions and classes use Sphinx-style docstrings
with proper formatting. Google-style and NumPy-style docstrings are not allowed.

Required Sphinx elements:
- :param name: description
- :ptype name: type
- :return: description
- :rtype: type
- :raises ExceptionType: description
"""

import ast
import re
from pathlib import Path

import pytest
```

**Implement DocstringVisitor class**:
- Inherit from `ast.NodeVisitor`
- Implement visit methods for FunctionDef, AsyncFunctionDef, ClassDef
- Implement `_check_docstring` with Google/NumPy pattern detection
- Store violations as list

**Implement helper functions**:
- `check_file_docstrings()`: Parse file with `ast.parse()`, visit tree
- `get_project_root()`: Navigate up from `__file__`

**Implement test functions**:
- Three tests: src/, tests/, examples/
- Each scans directory with `.rglob("*.py")`
- Collect all violations
- If violations found, use `pytest.fail()` with detailed message

### Step 3: Create test_no_emojis.py

**Start with imports and module docstring**:
```python
"""
Enforcement test: No emoji characters allowed in code.

This test scans all code and configuration files for emoji characters
and fails if any are found. Emojis make code less professional and can
cause encoding issues in some environments.
"""

import json
from pathlib import Path

import pytest
```

**Implement emoji detection**:
- `is_emoji(char)`: Check Unicode ranges
- `find_emojis_in_text()`: Scan text for emojis

**Implement file scanners**:
- `scan_python_file()`: Read and scan Python files
- `scan_notebook_file()`: Parse JSON, scan cells
- `scan_text_file()`: Read and scan text files

**Implement test functions**:
- Three tests: Python files, notebooks, config files
- Use `.rglob()` with appropriate patterns
- Skip build/cache directories
- Collect all violations
- Fail with detailed error message if violations found

### Step 4: Add Comprehensive Docstrings

Every function in both test files must have complete Sphinx docstrings (demonstrating the standard you're enforcing).

### Step 5: Test the Enforcement Tests

```bash
# Should pass (no violations in current code)
pytest tests/enforcement/ -v

# Verify they catch violations by temporarily adding one
echo 'def bad(): """Args: test"""' >> tests/test_temp.py
pytest tests/enforcement/test_sphinx_docstrings.py
# Should fail with violation message

# Clean up
rm tests/test_temp.py

# Verify emoji detection
echo 'x = "test 😀"' >> tests/test_temp.py
pytest tests/enforcement/test_no_emojis.py
# Should fail with emoji violation

# Clean up
rm tests/test_temp.py
```

### Step 6: Validate with ruff

```bash
ruff check tests/enforcement/
ruff format tests/enforcement/
```

---

## Code Structure Examples

### DocstringVisitor Pattern

```python
class DocstringVisitor(ast.NodeVisitor):
    """
    AST visitor to find and validate docstrings.

    :param file_path: Path to file being analyzed
    :ptype file_path: Path
    """

    def __init__(self, file_path):
        """
        Initialize the visitor.

        :param file_path: Path to file being analyzed
        :ptype file_path: Path
        """
        self.file_path = file_path
        self.violations = []

    def visit_FunctionDef(self, node):  # noqa: N802
        """
        Visit function definition node.

        :param node: AST node for function definition
        :ptype node: ast.FunctionDef
        """
        self._check_docstring(node, "function")
        self.generic_visit(node)

    def _check_docstring(self, node, node_type):
        """
        Check if a node has a proper Sphinx-style docstring.

        :param node: AST node to check
        :ptype node: ast.AST
        :param node_type: Type of node (for error messages)
        :ptype node_type: str
        """
        docstring = ast.get_docstring(node)

        # Skip if no docstring and function is private/test
        if not docstring:
            if not node.name.startswith("_") and not node.name.startswith("test_"):
                self.violations.append(f"{self.file_path}:{node.lineno} - {node_type} '{node.name}' missing docstring")
            return

        # Check for Google-style patterns
        for pattern in google_patterns:
            if re.search(pattern, docstring, re.MULTILINE):
                self.violations.append(f"{self.file_path}:{node.lineno} - {node_type} '{node.name}' uses Google-style docstring")
                return
```

### Emoji Detection Pattern

```python
def is_emoji(char):
    """
    Check if a character is an emoji.

    :param char: Character to check
    :ptype char: str
    :return: True if character is an emoji
    :rtype: bool
    """
    code_point = ord(char)

    emoji_ranges = [
        (0x1F600, 0x1F64F),  # Emoticons
        (0x1F300, 0x1F5FF),  # Misc Symbols and Pictographs
        # ... more ranges ...
    ]

    return any(start <= code_point <= end for start, end in emoji_ranges)
```

---

## Troubleshooting

**Issue**: AST parse errors
**Solution**: Wrap `ast.parse()` in try/except, skip files with syntax errors

**Issue**: False positives on test function docstrings
**Solution**: Skip functions starting with `test_` or `_`

**Issue**: Emoji detection misses some emojis
**Solution**: Verify Unicode ranges are comprehensive, check https://unicode.org/emoji/

**Issue**: Tests too slow
**Solution**: Ensure skipping .venv, __pycache__, and other build directories

**Issue**: Import errors (ast, pytest)
**Solution**: Ensure poetry environment activated, run `poetry install`

---

## Next Steps

After completing this task:

1. **Validate Enforcement Tests Work**:
   ```bash
   # Should pass (clean codebase)
   pytest tests/enforcement/ -v

   # Manually test they catch violations
   # (add temporary violation, run test, should fail, remove violation)
   ```

2. **Move to Task 006**:
   - TDD Config Module (tests first, then implementation)
   - All code will be validated by these enforcement tests

---

## Related Documents

**Design**: [005-testing-strategy.md](../designs/005-testing-strategy.md) - Enforcement testing section
**Requirements**: [004-quality-requirements.md](../requirements/004-quality-requirements.md) - Code quality standards
**Phase**: [phase-03-testing-infrastructure.md](../phases/phase-03-testing-infrastructure.md) - Phase overview
**Previous**: [task-004-setup-pytest-infrastructure.md](task-004-setup-pytest-infrastructure.md) - Previous task
**Next**: [task-006-config-module.md](task-006-config-module.md) - Next task

---

## Document Metadata

- **Task ID**: 005
- **Phase**: 03 - Test Infrastructure Foundation
- **LOC Output**: ~500 lines (2 enforcement test files)
- **Complexity**: Medium
- **Prerequisites**: Task 004 complete
- **Validates**: Code quality standards enforced automatically
