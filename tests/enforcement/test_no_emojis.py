"""
Enforcement test: No emoji characters allowed in code.

This test scans all code and configuration files for emoji characters
and fails if any are found. Emojis make code less professional and can
cause encoding issues in some environments.
"""

import json
from pathlib import Path

import pytest


def is_emoji(char):
    """
    Check if character is emoji.

    :param char: Character to check
    :ptype char: str
    :return: True if character is emoji
    :rtype: bool
    """
    code_point = ord(char)

    # Emoji Unicode ranges
    emoji_ranges = [
        (0x1F600, 0x1F64F),  # Emoticons
        (0x1F300, 0x1F5FF),  # Misc Symbols and Pictographs
        (0x1F680, 0x1F6FF),  # Transport and Map
        (0x1F1E0, 0x1F1FF),  # Regional indicators
        (0x2600, 0x26FF),  # Misc symbols
        (0x2700, 0x27BF),  # Dingbats
        (0xFE00, 0xFE0F),  # Variation Selectors
        (0x1F900, 0x1F9FF),  # Supplemental Symbols and Pictographs
        (0x1F018, 0x1F270),  # Various symbols
        (0x238C, 0x2454),  # Misc items
        (0x20D0, 0x20FF),  # Combining Diacritical Marks for Symbols
    ]

    return any(start <= code_point <= end for start, end in emoji_ranges)


def find_emojis_in_text(text, file_path):
    """
    Find all emojis in text content.

    :param text: Text content to scan
    :ptype text: str
    :param file_path: Path to file being scanned (for error messages)
    :ptype file_path: Path
    :return: List of (line_number, line_content, emoji_char) tuples
    :rtype: list
    """
    violations = []

    for line_num, line in enumerate(text.splitlines(), start=1):
        for char in line:
            if is_emoji(char):
                violations.append((line_num, line.strip(), char))

    return violations


def scan_python_file(file_path):
    """
    Scan Python file for emojis.

    :param file_path: Path to Python file
    :ptype file_path: Path
    :return: List of violations
    :rtype: list
    """
    with open(file_path, encoding="utf-8") as f:
        content = f.read()

    return find_emojis_in_text(content, file_path)


def scan_notebook_file(file_path):
    """
    Scan Jupyter notebook for emojis.

    :param file_path: Path to notebook file
    :ptype file_path: Path
    :return: List of violations
    :rtype: list
    """
    with open(file_path, encoding="utf-8") as f:
        notebook = json.load(f)

    violations = []

    # Check all cells
    for cell_idx, cell in enumerate(notebook.get("cells", [])):
        source = cell.get("source", [])

        # Convert source to string
        if isinstance(source, list):
            source_text = "".join(source)
        else:
            source_text = source

        # Scan cell content
        cell_violations = find_emojis_in_text(source_text, file_path)

        # Add cell context to violations
        for line_num, line, emoji in cell_violations:
            violations.append((f"cell_{cell_idx}:{line_num}", line, emoji))

    return violations


def scan_text_file(file_path):
    """
    Scan text or config file for emojis.

    :param file_path: Path to file
    :ptype file_path: Path
    :return: List of violations
    :rtype: list
    """
    with open(file_path, encoding="utf-8") as f:
        content = f.read()

    return find_emojis_in_text(content, file_path)


def get_project_root():
    """
    Get project root directory.

    :return: Path to project root
    :rtype: Path
    """
    # Go up from tests/enforcement/ to project root
    return Path(__file__).parent.parent.parent


def test_no_emojis_in_python_files():
    """
    Test that no Python files contain emoji characters.
    """
    project_root = get_project_root()
    all_violations = []

    # Scan all Python files
    for py_file in project_root.rglob("*.py"):
        # Skip virtual environment and build directories
        if any(part in py_file.parts for part in [".venv", "venv", "__pycache__", ".tox", "build", "dist", ".pytest_cache"]):
            continue

        violations = scan_python_file(py_file)
        if violations:
            relative_path = py_file.relative_to(project_root)
            for line_num, line, emoji in violations:
                all_violations.append(f"{relative_path}:{line_num} - Found emoji '{emoji}' in: {line}")

    if all_violations:
        error_message = "\n".join(
            [
                "EMOJI CHARACTERS FOUND IN PYTHON FILES:",
                "Emojis are not allowed in code. Please remove them.",
                "",
                *all_violations,
            ]
        )
        pytest.fail(error_message)


def test_no_emojis_in_notebook_files():
    """
    Test that no Jupyter notebook files contain emoji characters.
    """
    project_root = get_project_root()
    all_violations = []

    # Scan all notebook files
    for nb_file in project_root.rglob("*.ipynb"):
        # Skip checkpoint files
        if ".ipynb_checkpoints" in nb_file.parts:
            continue

        violations = scan_notebook_file(nb_file)
        if violations:
            relative_path = nb_file.relative_to(project_root)
            for location, line, emoji in violations:
                all_violations.append(f"{relative_path}:{location} - Found emoji '{emoji}' in: {line}")

    if all_violations:
        error_message = "\n".join(
            [
                "EMOJI CHARACTERS FOUND IN NOTEBOOK FILES:",
                "Emojis are not allowed in notebooks. Please remove them.",
                "",
                *all_violations,
            ]
        )
        pytest.fail(error_message)


def test_no_emojis_in_config_files():
    """
    Test that no configuration files contain emoji characters.
    """
    project_root = get_project_root()
    all_violations = []

    # Scan specific config files
    config_files = [
        project_root / "pyproject.toml",
        project_root / "requirements.txt",
    ]

    for config_file in config_files:
        if not config_file.exists():
            continue

        violations = scan_text_file(config_file)
        if violations:
            relative_path = config_file.relative_to(project_root)
            for line_num, line, emoji in violations:
                all_violations.append(f"{relative_path}:{line_num} - Found emoji '{emoji}' in: {line}")

    if all_violations:
        error_message = "\n".join(
            [
                "EMOJI CHARACTERS FOUND IN CONFIGURATION FILES:",
                "Emojis are not allowed in config files. Please remove them.",
                "",
                *all_violations,
            ]
        )
        pytest.fail(error_message)
