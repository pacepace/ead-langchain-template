"""
Tests for scripts/sync_notebooks.py

This demonstrates testing utility scripts following TDD patterns.
Even though scripts/ aren't part of the package, we test critical logic.

Run these tests with: pytest tests/integration/test_sync_notebooks.py -v
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add scripts directory to path for imports
scripts_dir = Path(__file__).parent.parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

import sync_notebooks  # noqa: E402 - Import after sys.path modification is intentional


class TestGetProjectRoot:
    """Tests for get_project_root function."""

    def test_get_project_root_returns_path(self):
        """
        Test that get_project_root returns Path object.
        """
        root = sync_notebooks.get_project_root()
        assert isinstance(root, Path)

    def test_get_project_root_is_parent_of_scripts(self):
        """
        Test that project root is parent of scripts/ directory.
        """
        root = sync_notebooks.get_project_root()
        scripts = root / "scripts"
        assert scripts.exists()

    def test_get_project_root_has_pyproject_toml(self):
        """
        Test that project root contains pyproject.toml.
        """
        root = sync_notebooks.get_project_root()
        assert (root / "pyproject.toml").exists()


class TestFindExampleFiles:
    """Tests for find_example_files function."""

    def test_find_example_files_returns_list(self):
        """
        Test that find_example_files returns list.
        """
        files = sync_notebooks.find_example_files()
        assert isinstance(files, list)

    def test_find_example_files_returns_path_objects(self):
        """
        Test that all returned items are Path objects.
        """
        files = sync_notebooks.find_example_files()
        if files:  # Only test if files exist
            assert all(isinstance(f, Path) for f in files)

    def test_find_example_files_match_pattern(self):
        """
        Test that all files match pattern 0X_*.py.
        """
        files = sync_notebooks.find_example_files()
        if files:
            for f in files:
                assert f.suffix == ".py"
                assert f.name[0].isdigit()
                assert f.name[1].isdigit()
                assert f.name[2] == "_"

    def test_find_example_files_are_sorted(self):
        """
        Test that files are returned in sorted order.
        """
        files = sync_notebooks.find_example_files()
        if len(files) > 1:
            file_names = [f.name for f in files]
            assert file_names == sorted(file_names)

    def test_find_example_files_exits_if_no_examples_dir(self, tmp_path, monkeypatch):
        """
        Test that function exits if examples/ directory doesn't exist.

        :param tmp_path: Pytest fixture providing temporary directory
        :ptype tmp_path: Path
        :param monkeypatch: Pytest fixture for modifying environment
        :ptype monkeypatch: pytest.MonkeyPatch
        """

        # Mock get_project_root to return temp dir without examples/
        def mock_root():
            """
            Mock function that returns temp directory.

            :return: Temporary path without examples directory
            :rtype: Path
            """
            return tmp_path

        monkeypatch.setattr(sync_notebooks, "get_project_root", mock_root)

        with pytest.raises(SystemExit) as exc_info:
            sync_notebooks.find_example_files()

        assert exc_info.value.code == 1


class TestCheckJupytextInstalled:
    """Tests for check_jupytext_installed function."""

    def test_check_jupytext_returns_bool(self):
        """
        Test that check_jupytext_installed returns boolean.
        """
        result = sync_notebooks.check_jupytext_installed()
        assert isinstance(result, bool)

    @patch("sync_notebooks.subprocess.run")
    def test_check_jupytext_installed_true_when_available(self, mock_run):
        """
        Test returns True when jupytext is available.

        :param mock_run: mock subprocess.run
        :ptype mock_run: unittest.mock.MagicMock
        """
        # Mock successful jupytext --version call
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        result = sync_notebooks.check_jupytext_installed()

        assert result is True
        mock_run.assert_called_once()

    @patch("sync_notebooks.subprocess.run")
    def test_check_jupytext_installed_false_when_not_available(self, mock_run):
        """
        Test returns False when jupytext is not available.

        :param mock_run: Mock subprocess.run
        :ptype mock_run: unittest.mock.MagicMock
        """
        # Mock FileNotFoundError (jupytext not in PATH)
        mock_run.side_effect = FileNotFoundError()

        result = sync_notebooks.check_jupytext_installed()

        assert result is False


class TestSyncFile:
    """Tests for sync_file function."""

    def test_sync_file_returns_bool(self, tmp_path):
        """
        Test that sync_file returns boolean.

        :param tmp_path: Pytest fixture providing temporary directory
        :ptype tmp_path: Path
        """
        # Create a test .py file
        py_file = tmp_path / "01_test.py"
        py_file.write_text("# Test file\nprint('hello')\n")

        result = sync_notebooks.sync_file(py_file, check_only=True)

        assert isinstance(result, bool)

    def test_sync_file_check_only_returns_false_if_ipynb_missing(self, tmp_path):
        """
        Test check_only mode returns False when .ipynb is missing.

        :param tmp_path: Pytest fixture providing temporary directory
        :ptype tmp_path: Path
        """
        py_file = tmp_path / "01_test.py"
        py_file.write_text("# Test file\n")

        result = sync_notebooks.sync_file(py_file, check_only=True)

        assert result is False

    def test_sync_file_check_only_returns_true_if_ipynb_up_to_date(self, tmp_path):
        """
        Test check_only mode returns True when .ipynb is up to date.

        :param tmp_path: Pytest fixture providing temporary directory
        :ptype tmp_path: Path
        """
        py_file = tmp_path / "01_test.py"
        ipynb_file = tmp_path / "01_test.ipynb"

        py_file.write_text("# Test file\n")
        ipynb_file.write_text('{"cells": []}\n')

        # Touch ipynb to make it newer
        import time

        time.sleep(0.01)
        ipynb_file.touch()

        result = sync_notebooks.sync_file(py_file, check_only=True)

        assert result is True

    def test_sync_file_check_only_returns_false_if_ipynb_out_of_date(self, tmp_path):
        """
        Test check_only mode returns False when .ipynb is older than .py.

        :param tmp_path: Pytest fixture providing temporary directory
        :ptype tmp_path: Path
        """
        py_file = tmp_path / "01_test.py"
        ipynb_file = tmp_path / "01_test.ipynb"

        ipynb_file.write_text('{"cells": []}\n')

        # Touch py to make it newer
        import time

        time.sleep(0.01)
        py_file.write_text("# Test file\n")

        result = sync_notebooks.sync_file(py_file, check_only=True)

        assert result is False

    @patch("sync_notebooks.subprocess.run")
    def test_sync_file_converts_with_jupytext(self, mock_run, tmp_path):
        """
        Test that sync_file calls jupytext with correct arguments.

        :param mock_run: Mock subprocess.run
        :ptype mock_run: unittest.mock.MagicMock
        :param tmp_path: Pytest fixture providing temporary directory
        :ptype tmp_path: Path
        """
        py_file = tmp_path / "01_test.py"
        py_file.write_text("# Test file\n")

        # Mock successful jupytext call
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        result = sync_notebooks.sync_file(py_file, check_only=False)

        # Verify jupytext was called
        mock_run.assert_called_once()
        call_args = mock_run.call_args[0][0]

        assert "jupytext" in call_args
        assert "--to" in call_args
        assert "notebook" in call_args
        assert str(py_file) in call_args
        assert result is True

    @patch("sync_notebooks.subprocess.run")
    def test_sync_file_returns_false_on_conversion_error(self, mock_run, tmp_path):
        """
        Test that sync_file returns False when conversion fails.

        :param mock_run: Mock subprocess.run
        :ptype mock_run: unittest.mock.MagicMock
        :param tmp_path: Pytest fixture providing temporary directory
        :ptype tmp_path: Path
        """
        py_file = tmp_path / "01_test.py"
        py_file.write_text("# Test file\n")

        # Mock failed jupytext call
        from subprocess import CalledProcessError

        mock_run.side_effect = CalledProcessError(1, "jupytext", stderr="Error")

        result = sync_notebooks.sync_file(py_file, check_only=False)

        assert result is False


class TestMainIntegration:
    """Integration tests for main function."""

    @patch("sync_notebooks.sys.argv", ["sync_notebooks.py"])
    @patch("sync_notebooks.sys.exit")
    @patch("sync_notebooks.check_jupytext_installed")
    def test_main_exits_if_jupytext_not_installed(self, mock_check, mock_exit):
        """
        Test main exits with error if jupytext is not installed.

        :param mock_check: Mock check_jupytext_installed
        :ptype mock_check: unittest.mock.MagicMock
        :param mock_exit: Mock sys.exit
        :ptype mock_exit: unittest.mock.MagicMock
        """
        mock_check.return_value = False
        mock_exit.side_effect = SystemExit(1)

        with pytest.raises(SystemExit):
            sync_notebooks.main()

        mock_exit.assert_called_with(1)

    @patch("sync_notebooks.sys.argv", ["sync_notebooks.py"])
    @patch("sync_notebooks.sys.exit")
    @patch("sync_notebooks.find_example_files")
    @patch("sync_notebooks.check_jupytext_installed")
    def test_main_exits_success_if_no_files(self, mock_check, mock_find, mock_exit):
        """
        Test main exits successfully if no example files found.

        :param mock_check: Mock check_jupytext_installed
        :ptype mock_check: unittest.mock.MagicMock
        :param mock_find: Mock find_example_files
        :ptype mock_find: unittest.mock.MagicMock
        :param mock_exit: Mock sys.exit
        :ptype mock_exit: unittest.mock.MagicMock
        """
        mock_check.return_value = True
        mock_find.return_value = []
        mock_exit.side_effect = SystemExit(0)

        with pytest.raises(SystemExit):
            sync_notebooks.main()

        mock_exit.assert_called_with(0)
