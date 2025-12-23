#!/usr/bin/env python3
"""
Sync Python example files to Jupyter notebooks.

This script converts .py files in examples/ to .ipynb format, ensuring
both versions stay synchronized. Uses jupytext for conversion.

Usage:
    python scripts/sync_notebooks.py              # Sync all examples (enhanced)
    python scripts/sync_notebooks.py --check      # Verify sync status only
    python scripts/sync_notebooks.py --simple     # Basic conversion without enhancements
    python scripts/sync_notebooks.py --no-exercises  # Skip Try This exercises
    python scripts/sync_notebooks.py --force      # Force reconversion even if up to date
"""

import argparse
import ast
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def get_project_root() -> Path:
    """
    Get the project root directory.

    :return: Path to project root
    :rtype: Path
    """
    # Script is in scripts/, so parent is project root
    return Path(__file__).parent.parent


def find_example_files() -> list[Path]:
    """
    Find all .py example files.

    :return: List of .py file paths in examples/
    :rtype: list[Path]
    """
    project_root = get_project_root()
    examples_dir = project_root / "examples"

    if not examples_dir.exists():
        print(f"ERROR: Examples directory not found: {examples_dir}")
        sys.exit(1)

    # Find all .py files that match pattern 0X_*.py
    py_files = sorted(examples_dir.glob("[0-9][0-9]_*.py"))

    if not py_files:
        print(f"WARNING: No example files found in {examples_dir}")

    return py_files


def check_jupytext_installed() -> bool:
    """
    Check if jupytext is installed.

    :return: True if jupytext is available
    :rtype: bool
    """
    try:
        result = subprocess.run(
            ["jupytext", "--version"],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


class CodePattern:
    """Detected code patterns for enhancement."""

    def __init__(self):
        """Initialize code pattern storage."""
        self.api_calls = []
        self.model_instantiations = []
        self.functions = []
        self.imports = []
        self.try_blocks = []


class ASTAnalyzer(ast.NodeVisitor):
    """AST visitor to extract patterns from Python code."""

    def __init__(self):
        """Initialize the analyzer."""
        self.patterns = CodePattern()
        self.current_function = None

    def visit_FunctionDef(self, node: ast.FunctionDef):  # noqa: N802
        """Visit function definitions."""
        docstring = ast.get_docstring(node)
        self.patterns.functions.append(
            {
                "name": node.name,
                "docstring": docstring,
                "lineno": node.lineno,
                "args": [arg.arg for arg in node.args.args],
            }
        )
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = None

    def visit_Call(self, node: ast.Call):  # noqa: N802
        """Visit function calls to detect API patterns."""
        # Detect get_api_key calls
        if isinstance(node.func, ast.Name) and node.func.id == "get_api_key":
            self.patterns.api_calls.append({"type": "api_key", "lineno": node.lineno})

        # Detect LLM invoke/stream calls
        if isinstance(node.func, ast.Attribute):
            if node.func.attr in ("invoke", "stream"):
                self.patterns.api_calls.append({"type": node.func.attr, "lineno": node.lineno, "function": self.current_function})

        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):  # noqa: N802
        """Visit assignments to detect model instantiations."""
        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
            model_classes = ("ChatOpenAI", "ChatAnthropic", "ChatGoogleGenerativeAI")
            if node.value.func.id in model_classes:
                # Extract model name from arguments
                model_name = None
                for keyword in node.value.keywords:
                    if keyword.arg == "model" and isinstance(keyword.value, ast.Constant):
                        model_name = keyword.value.value
                        break

                self.patterns.model_instantiations.append(
                    {
                        "class": node.value.func.id,
                        "model": model_name,
                        "lineno": node.lineno,
                        "function": self.current_function,
                    }
                )

        self.generic_visit(node)

    def visit_Try(self, node: ast.Try):  # noqa: N802
        """Visit try/except blocks."""
        self.patterns.try_blocks.append({"lineno": node.lineno, "function": self.current_function})
        self.generic_visit(node)


def analyze_python_file(py_file: Path) -> CodePattern:
    """
    Analyze Python file to extract patterns.

    :param py_file: Path to Python file
    :ptype py_file: Path
    :return: Detected code patterns
    :rtype: CodePattern
    """
    source = py_file.read_text()
    tree = ast.parse(source)
    analyzer = ASTAnalyzer()
    analyzer.visit(tree)
    return analyzer.patterns


def format_docstring_as_markdown(docstring: str | None) -> str:
    """
    Convert a docstring to rich markdown.

    :param docstring: Raw docstring text
    :ptype docstring: str | None
    :return: Formatted markdown
    :rtype: str
    """
    if not docstring:
        return ""

    lines = docstring.strip().split("\n")
    formatted = []

    for line in lines:
        line = line.strip()
        if not line:
            formatted.append("")
            continue

        # Convert "Shows:" or similar to bold headers
        if line.endswith(":") and len(line.split()) <= 2:
            formatted.append(f"**{line}**")
        # Convert dash lists to proper markdown
        elif line.startswith("-"):
            formatted.append(line)
        else:
            formatted.append(line)

    return "\n".join(formatted)


def should_add_exercise(func_name: str, func_info: dict[str, Any]) -> bool:
    """
    Determine if a function should get an exercise cell.

    :param func_name: Name of the function
    :ptype func_name: str
    :param func_info: Function information from AST
    :ptype func_info: dict[str, Any]
    :return: True if exercise should be added
    :rtype: bool
    """
    # Skip certain patterns
    skip_patterns = [
        "main",  # Already handled
        "__init__",  # Constructor
        "on_",  # Callback methods
        "get_",  # Getters
        "have_",  # Helper functions
    ]

    for pattern in skip_patterns:
        if func_name == pattern or func_name.startswith(pattern):
            return False

    return True


def generate_exercise_for_function(
    func_name: str, func_info: dict[str, Any], patterns: CodePattern, source_code: str = ""
) -> list[str]:
    """
    Generate a Try This exercise for a function.

    :param func_name: Name of the function
    :ptype func_name: str
    :param func_info: Function information from AST
    :ptype func_info: dict[str, Any]
    :param patterns: Detected code patterns
    :ptype patterns: CodePattern
    :param source_code: Source code of the function to analyze
    :ptype source_code: str
    :return: Exercise markdown as list of lines (for Jupyter format)
    :rtype: list[str]
    """
    exercises = []
    exercises.append("### Try This\n")
    exercises.append("\n")
    exercises.append("Experiment with the code above:\n")

    # Check if function uses models
    models_used = [m for m in patterns.model_instantiations if m["function"] == func_name]

    # Check if function uses invoke/stream
    api_calls = [c for c in patterns.api_calls if c.get("function") == func_name]
    has_stream = any(c["type"] == "stream" for c in api_calls)
    has_invoke = any(c["type"] == "invoke" for c in api_calls)
    has_batch = "batch" in source_code.lower()

    # Check if function already demonstrates temperature (avoid redundant suggestions)
    demonstrates_temperature = "temperature" in func_name.lower() or (source_code and source_code.count("temperature") > 1)

    suggestion_num = 1

    # Only suggest temperature if function creates models and doesn't already demonstrate it
    if models_used and not demonstrates_temperature:
        exercises.append(
            f"{suggestion_num}. Try changing the `temperature` parameter (0.0 for deterministic, 1.0 for creative)\n"
        )
        suggestion_num += 1

    # Suggest model alternatives based on provider
    if models_used:
        model_info = models_used[0]
        if "ChatOpenAI" in model_info["class"]:
            exercises.append(f"{suggestion_num}. Experiment with different models: `gpt-4o`, `gpt-5-mini`, or `gpt-5`\n")
        elif "ChatAnthropic" in model_info["class"]:
            exercises.append(f"{suggestion_num}. Try different Claude models: `claude-3-5-sonnet-20241022`, `claude-haiku-4-5`\n")
        elif "ChatGoogleGenerativeAI" in model_info["class"]:
            exercises.append(f"{suggestion_num}. Test other Gemini models: `gemini-2.5-flash`, `gemini-1.5-pro`\n")
        suggestion_num += 1

    # Context-specific third suggestion
    if has_stream:
        exercises.append(f"{suggestion_num}. Add a character or word counter to track the streaming progress\n")
    elif has_batch:
        exercises.append(f"{suggestion_num}. Try adding more prompts to the batch and compare timing\n")
    elif has_invoke and "conversation" in func_name.lower():
        exercises.append(f"{suggestion_num}. Add more conversation turns and see how context affects responses\n")
    elif has_invoke:
        exercises.append(f"{suggestion_num}. Modify the prompt to ask about a topic relevant to your work\n")
    elif "callback" in func_name.lower() or "token" in func_name.lower():
        exercises.append(f"{suggestion_num}. Track additional metrics like response time or token efficiency\n")
    elif models_used:
        exercises.append(f"{suggestion_num}. Change the prompt and observe how the response varies\n")

    return exercises


def enhance_notebook(ipynb_file: Path, py_file: Path, add_exercises: bool = True) -> bool:
    """
    Enhance a converted notebook with rich explanations and exercises.

    :param ipynb_file: Path to notebook file
    :ptype ipynb_file: Path
    :param py_file: Path to source Python file
    :ptype py_file: Path
    :param add_exercises: Whether to add Try This exercises
    :ptype add_exercises: bool
    :return: True if enhancement succeeded
    :rtype: bool
    """
    try:
        # Load the notebook
        notebook = json.loads(ipynb_file.read_text())

        # Analyze the Python source
        patterns = analyze_python_file(py_file)

        # Track which functions we've added exercises for
        exercises_added = set()

        # Enhance cells
        enhanced_cells = []
        for i, cell in enumerate(notebook["cells"]):
            # Enhance markdown cells with better formatting
            if cell["cell_type"] == "markdown":
                source = "".join(cell["source"])

                # Check if this is a docstring we can enhance
                if "Shows:" in source or "demonstrates" in source.lower():
                    # Format it better
                    enhanced_source = format_docstring_as_markdown(source)
                    cell["source"] = enhanced_source.split("\n")
                enhanced_cells.append(cell)

            # Add exercises after function definition cells
            elif cell["cell_type"] == "code" and add_exercises:
                source = "".join(cell["source"])

                # Check if this cell defines a function we should add an exercise for
                added_exercise = False
                for func in patterns.functions:
                    if (
                        f"def {func['name']}(" in source
                        and should_add_exercise(func["name"], func)
                        and func["name"] not in exercises_added
                    ):
                        # Add the code cell first
                        enhanced_cells.append(cell)

                        # Add exercise markdown with proper formatting
                        exercise_lines = generate_exercise_for_function(func["name"], func, patterns, source)
                        enhanced_cells.append(
                            {
                                "cell_type": "markdown",
                                "metadata": {},
                                "source": exercise_lines,
                            }
                        )

                        # Add empty code cell for experimentation
                        enhanced_cells.append(
                            {
                                "cell_type": "code",
                                "metadata": {},
                                "source": ["# Your experiments here\n"],
                                "outputs": [],
                                "execution_count": None,
                            }
                        )

                        exercises_added.add(func["name"])
                        added_exercise = True
                        break  # Only add exercise for first matching function

                # Only add cell if we didn't already add it with an exercise
                if not added_exercise:
                    enhanced_cells.append(cell)

            else:
                enhanced_cells.append(cell)

        # Update notebook with enhanced cells
        notebook["cells"] = enhanced_cells

        # Write back
        ipynb_file.write_text(json.dumps(notebook, indent=1))
        return True

    except Exception as e:
        print(f"  [WARNING] Enhancement failed: {e}")
        return False


def sync_file(
    py_file: Path, check_only: bool = False, enhance: bool = True, add_exercises: bool = True, force: bool = False
) -> bool:
    """
    Sync a single .py file to .ipynb.

    :param py_file: Path to .py file
    :ptype py_file: Path
    :param check_only: If True, only check sync status
    :ptype check_only: bool
    :param enhance: If True, enhance notebook with rich content
    :ptype enhance: bool
    :param add_exercises: If True, add Try This exercises
    :ptype add_exercises: bool
    :param force: If True, force reconversion even if up to date
    :ptype force: bool
    :return: True if file is synced (or was synced successfully)
    :rtype: bool
    """
    ipynb_file = py_file.with_suffix(".ipynb")

    # Check if .ipynb exists and is newer (unless forced)
    if ipynb_file.exists() and not force:
        if ipynb_file.stat().st_mtime >= py_file.stat().st_mtime:
            print(f"[OK] {py_file.name} -> {ipynb_file.name} (up to date)")
            return True
        else:
            if check_only:
                print(f"[SKIP] {py_file.name} -> {ipynb_file.name} (out of sync)")
                return False

    if check_only:
        print(f"[SKIP] {py_file.name} -> {ipynb_file.name} (missing)")
        return False

    # Convert .py to .ipynb using jupytext
    print(f"→ Converting {py_file.name} to {ipynb_file.name}...")

    try:
        subprocess.run(
            ["jupytext", "--to", "notebook", "--output", str(ipynb_file), str(py_file)],
            capture_output=True,
            text=True,
            check=True,
        )

        # Enhance the notebook if requested
        if enhance:
            print("  → Enhancing with rich content...")
            if enhance_notebook(ipynb_file, py_file, add_exercises=add_exercises):
                mode = "enhanced" if add_exercises else "enhanced (no exercises)"
                print(f"[OK] {py_file.name} -> {ipynb_file.name} ({mode})")
            else:
                print(f"[OK] {py_file.name} -> {ipynb_file.name} (converted, enhancement partially failed)")
        else:
            print(f"[OK] {py_file.name} -> {ipynb_file.name} (converted)")

        return True

    except subprocess.CalledProcessError as e:
        print(f"[FAIL] {py_file.name} -> {ipynb_file.name} (FAILED)")
        print(f"  Error: {e.stderr}")
        return False


def main():
    """
    Main entry point for sync script.

    :return: None
    :rtype: None
    """
    parser = argparse.ArgumentParser(description="Sync Python example files to Jupyter notebooks with optional enhancements")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check sync status only (don't convert)",
    )
    parser.add_argument(
        "--simple",
        action="store_true",
        help="Basic conversion without enhancements",
    )
    parser.add_argument(
        "--no-exercises",
        action="store_true",
        help="Skip adding Try This exercise cells",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force reconversion even if notebooks are up to date",
    )

    args = parser.parse_args()

    # Determine enhancement mode
    enhance = not args.simple
    add_exercises = not args.no_exercises

    mode_desc = "Enhanced" if enhance else "Simple"
    if enhance and not add_exercises:
        mode_desc = "Enhanced (no exercises)"

    print("=" * 80)
    print(f"Example File Sync: .py → .ipynb ({mode_desc})")
    print("=" * 80)
    print()

    # Check if jupytext is installed
    if not check_jupytext_installed():
        print("ERROR: jupytext is not installed")
        print()
        print("Install with:")
        print("  pip install jupytext")
        print("  # OR")
        print("  poetry add --group dev jupytext")
        print()
        sys.exit(1)

    # Find all example files
    py_files = find_example_files()

    if not py_files:
        print("No example files to sync")
        sys.exit(0)

    print(f"Found {len(py_files)} example file(s)")
    if enhance:
        print("Mode: Enhanced conversion with rich explanations")
        if add_exercises:
            print("      + Try This exercise cells")
    else:
        print("Mode: Simple conversion (use without --simple for enhancements)")
    print()

    # Sync each file
    results = [
        sync_file(py_file, check_only=args.check, enhance=enhance, add_exercises=add_exercises, force=args.force)
        for py_file in py_files
    ]

    # Summary
    print()
    print("=" * 80)

    if args.check:
        if all(results):
            print("[OK] All notebooks are in sync")
            sys.exit(0)
        else:
            out_of_sync = sum(1 for r in results if not r)
            print(f"[FAIL] {out_of_sync} notebook(s) out of sync")
            print()
            print("Run without --check to sync:")
            print("  python scripts/sync_notebooks.py")
            sys.exit(1)
    else:
        successful = sum(1 for r in results if r)
        failed = sum(1 for r in results if not r)

        if failed == 0:
            print(f"[OK] Successfully synced {successful} file(s)")
            sys.exit(0)
        else:
            print(f"[FAIL] Synced {successful} file(s), {failed} failed")
            sys.exit(1)


if __name__ == "__main__":
    main()
