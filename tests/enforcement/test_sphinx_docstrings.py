"""
Enforcement test for Sphinx docstring format compliance.

Validates that all docstrings follow mandatory format:
- Use :ptype NOT :type for parameter types
- Conditional requirements based on function signatures
- Docstrings must start with capital letter (PEP 257)
"""

import ast
import re
from pathlib import Path

import pytest


class TestSphinxDocstringEnforcement:
    """Test suite enforcing Sphinx docstring format."""

    # proper nouns allowed to start with uppercase
    ALLOWED_PROPER_NOUNS = {
        "PostgreSQL",
        "Redis",
        "DuckDB",
        "LangGraph",
        "LangChain",
        "UUID",
        "FastAPI",
        "Pydantic",
        "Python",
        "OpenAI",
        "Anthropic",
        "WebSocket",
        "Alembic",
        "Docker",
        "JSON",
        "HTTP",
        "HTTPS",
        "API",
        "URL",
        "CLI",
        "TTL",
        "SSL",
        "TLS",
        "AWS",
        "None",
        "True",
        "False",
        "PII",
        "OTEL",
        "OpenTelemetry",
        "Sphinx",
        "JWT",
        "SQL",
        "LLM",
        "CSV",
        "Prometheus",
        "InfluxDB",
        "Lua",
        "Pytest",
        "Google",
        "Gemini",
        "Claude",
        "ChatOpenAI",
        "ChatAnthropic",
        "ChatGoogleGenerativeAI",
        "Path",
        "Dict",
        "List",
        "Optional",
        "Tuple",
        "Set",
        "LogRecord",
    }

    # directories to check
    SOURCE_DIRS = ["src/langchain_llm", "tests", "examples"]

    # files to exclude from checking
    EXCLUDED_FILES = {
        "test_sphinx_docstrings.py",
        "test_sphinx_docstring_enforcement.py",
    }

    def _get_python_files(self) -> list[Path]:
        """
        Get all Python files to check for docstring compliance.

        :return: List of Python file paths
        :rtype: list[Path]
        """
        project_root = Path(__file__).parent.parent.parent
        python_files = []

        for source_dir in self.SOURCE_DIRS:
            dir_path = project_root / source_dir
            if dir_path.exists():
                python_files.extend(dir_path.rglob("*.py"))

        # filter out excluded files
        return [f for f in python_files if f.name not in self.EXCLUDED_FILES and "__pycache__" not in str(f)]

    def _extract_docstring(self, node: ast.AST) -> str | None:
        """
        Extract docstring from AST node.

        :param node: AST node to extract docstring from
        :ptype node: ast.AST
        :return: Docstring text or None if no docstring
        :rtype: str | None
        """
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            return None

        if (
            node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and isinstance(node.body[0].value.value, str)
        ):
            return node.body[0].value.value

        return None

    def _get_function_signature(self, node: ast.FunctionDef) -> tuple[list[str], bool]:
        """
        Extract function signature details for validation.

        :param node: Function definition AST node
        :ptype node: ast.FunctionDef
        :return: Tuple of (parameter names, has return value)
        :rtype: tuple[list[str], bool]
        """
        # extract parameter names (skip self, cls)
        param_names = [arg.arg for arg in node.args.args if arg.arg not in ("self", "cls")]

        # check if function has return type hint (indicates return value)
        has_return = node.returns is not None

        return param_names, has_return

    def _find_type_violations(self, filepath: Path) -> list[tuple[int, str]]:
        """
        Find :type usage instead of :ptype in docstrings.

        :param filepath: Path to Python file to check
        :ptype filepath: Path
        :return: List of (line_number, line_content) tuples
        :rtype: list[tuple[int, str]]
        """
        violations = []
        type_pattern = re.compile(r":type\s+\w+:")

        try:
            with open(filepath, encoding="utf-8") as f:
                lines = f.readlines()

            for line_no, line in enumerate(lines, start=1):
                if type_pattern.search(line):
                    violations.append((line_no, line.strip()))

        except Exception as e:
            print(f"Warning: could not read {filepath}: {e}")

        return violations

    def _find_missing_documentation_violations(self, filepath: Path) -> list[tuple[int, str, str]]:
        """
        Find missing required docstring sections based on function signature.

        :param filepath: Path to Python file to check
        :ptype filepath: Path
        :return: List of (line_number, function_name, missing_section) tuples
        :rtype: list[tuple[int, str, str]]
        """
        violations = []

        try:
            with open(filepath, encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content, filename=str(filepath))

            for node in ast.walk(tree):
                if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                    continue

                # skip private methods (can have minimal docs)
                if node.name.startswith("_") and not node.name.startswith("__"):
                    continue

                # skip test functions (allow simpler docs)
                if node.name.startswith("test_"):
                    continue

                # skip property methods
                if any(isinstance(dec, ast.Name) and dec.id == "property" for dec in node.decorator_list):
                    continue

                docstring = self._extract_docstring(node)
                if not docstring:
                    # require docstring for public functions
                    violations.append((node.lineno, node.name, "missing docstring"))
                    continue

                param_names, has_return = self._get_function_signature(node)

                # check for required :param and :ptype for each parameter
                for param_name in param_names:
                    param_pattern = f":param {param_name}:"
                    ptype_pattern = f":ptype {param_name}:"

                    if param_pattern not in docstring:
                        violations.append((node.lineno, node.name, f"missing :param {param_name}:"))

                    if ptype_pattern not in docstring:
                        violations.append((node.lineno, node.name, f"missing :ptype {param_name}:"))

                # check for :return and :rtype if function has return annotation
                if has_return:
                    # skip if return type is None
                    if isinstance(node.returns, ast.Constant) and node.returns.value is None:
                        continue

                    if ":return:" not in docstring:
                        violations.append((node.lineno, node.name, "missing :return:"))

                    if ":rtype:" not in docstring:
                        violations.append((node.lineno, node.name, "missing :rtype:"))

        except SyntaxError:
            # skip files with syntax errors
            pass
        except Exception as e:
            print(f"Warning: could not parse {filepath}: {e}")

        return violations

    def test_no_type_field_usage(self):
        """
        Test that :ptype is used instead of :type for parameter types.

        Validates rule: use :ptype NOT :type for parameter types.

        :return: None
        :rtype: None
        """
        python_files = self._get_python_files()
        assert len(python_files) > 0, "no Python files found to check"

        all_violations = {}

        for filepath in python_files:
            violations = self._find_type_violations(filepath)
            if violations:
                all_violations[filepath] = violations

        if all_violations:
            error_lines = ["\nFound :type usage (should be :ptype) in docstrings:\n"]

            for filepath, violations in all_violations.items():
                error_lines.append(f"\n{filepath}:")
                for line_no, line_content in violations:
                    error_lines.append(f"  Line {line_no}: {line_content}")

            error_lines.append("\nRule: use :ptype NOT :type")
            error_lines.append("Fix: replace ':type param_name:' with ':ptype param_name:'")

            pytest.fail("".join(error_lines))

    def test_required_docstring_sections(self):
        """
        Test that functions have required docstring sections based on signature.

        Validates rule: include ALL sections (conditional on signature).
        If function has params, must document them. If returns value, must document it.

        :return: None
        :rtype: None
        """
        python_files = self._get_python_files()
        assert len(python_files) > 0, "no Python files found to check"

        all_violations = {}

        for filepath in python_files:
            violations = self._find_missing_documentation_violations(filepath)
            if violations:
                all_violations[filepath] = violations

        if all_violations:
            error_lines = ["\nFound missing required docstring sections:\n"]

            for filepath, violations in all_violations.items():
                # group by function to make output readable
                violations_by_func: dict[str, list[str]] = {}
                for line_no, func_name, missing in violations:
                    key = f"{func_name} (line {line_no})"
                    if key not in violations_by_func:
                        violations_by_func[key] = []
                    violations_by_func[key].append(missing)

                error_lines.append(f"\n{filepath}:")
                for func_key, missing_sections in violations_by_func.items():
                    error_lines.append(f"  {func_key}:")
                    for section in missing_sections:
                        error_lines.append(f"    - {section}")

            error_lines.append("\nRule: document all parameters and returns")
            error_lines.append("If function has params → need :param and :ptype")
            error_lines.append("If function returns value → need :return and :rtype")

            pytest.fail("".join(error_lines))

    def _find_capitalization_violations(self, filepath: Path) -> list[tuple[int, str, str]]:
        """
        Find docstrings that don't start with capital letter.

        :param filepath: Path to Python file to check
        :ptype filepath: Path
        :return: List of (line_number, entity_name, first_line) tuples
        :rtype: list[tuple[int, str, str]]
        """
        violations = []

        try:
            with open(filepath, encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content, filename=str(filepath))

            for node in ast.walk(tree):
                docstring = self._extract_docstring(node)
                if not docstring:
                    continue

                # get entity name
                entity_name = getattr(node, "name", "<module>")

                # get first non-empty, non-whitespace line
                first_line = None
                for line in docstring.split("\n"):
                    stripped = line.strip()
                    if stripped:
                        first_line = stripped
                        break

                if not first_line:
                    continue

                # skip if starts with special chars (like :param:, >>>, etc.)
                if first_line[0] in (":", ">", "`", "-", "*", "#"):
                    continue

                # check if first character is uppercase
                if not first_line[0].isupper():
                    violations.append((node.lineno, entity_name, first_line[:60]))

        except SyntaxError:
            # skip files with syntax errors
            pass
        except Exception as e:
            print(f"Warning: could not parse {filepath}: {e}")

        return violations

    def test_docstring_capitalization(self):
        """
        Test that docstrings start with capital letter per PEP 257.

        Validates rule: first letter of docstring must be capitalized.
        Follows standard Python PEP 257 convention.

        :return: None
        :rtype: None
        """
        python_files = self._get_python_files()
        assert len(python_files) > 0, "no Python files found to check"

        all_violations = {}

        for filepath in python_files:
            violations = self._find_capitalization_violations(filepath)
            if violations:
                all_violations[filepath] = violations

        if all_violations:
            error_lines = ["\nFound docstrings not starting with capital letter:\n"]

            for filepath, violations in all_violations.items():
                error_lines.append(f"\n{filepath}:")
                for line_no, entity_name, first_line in violations:
                    error_lines.append(f"  Line {line_no} ({entity_name}): {first_line}...")

            error_lines.append("\nRule: Docstrings must start with capital letter (PEP 257)")
            error_lines.append("Fix: Capitalize first letter of each docstring")

            pytest.fail("".join(error_lines))
