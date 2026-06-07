import sys
from collections import Counter
from pathlib import Path
from unittest.mock import patch

from app.cli import print_to_terminal
from app.global_ import HEADING, IGNORE_DIRS
from main import main


class TestArgumentParsing:
    def test_main_errors_when_path_does_not_exist(self, monkeypatch, capsys, tmp_path: Path):
        missing = tmp_path / "does-not-exist"
        monkeypatch.setattr(sys, "argv", ["main.py", str(missing)])

        with patch("main.calc_helper") as mock_calc, patch("main.print_to_terminal") as mock_print:
            main()

        output = capsys.readouterr().out
        assert f"Error: '{missing.resolve()}' does not exist." in output
        mock_calc.assert_not_called()
        mock_print.assert_not_called()

    def test_main_errors_when_path_is_a_file(self, monkeypatch, capsys, tmp_path: Path):
        file_path = tmp_path / "readme.txt"
        file_path.write_text("hello")
        monkeypatch.setattr(sys, "argv", ["main.py", str(file_path)])

        with patch("main.calc_helper") as mock_calc, patch("main.print_to_terminal") as mock_print:
            main()

        output = capsys.readouterr().out
        assert f"Error: '{file_path.resolve()}' is not a directory." in output
        mock_calc.assert_not_called()
        mock_print.assert_not_called()

    def test_main_defaults_to_current_directory(self, monkeypatch, tmp_path: Path):
        (tmp_path / "a.py").write_text("1")
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr(sys, "argv", ["main.py"])

        with patch("main.print_to_terminal") as mock_print, patch(
            "main.calc_helper", return_value=(1, Counter({".py": 1}), 1, 1)
        ):
            main()

        root, _, _, _, _, _ = mock_print.call_args[0]
        assert root.resolve() == tmp_path.resolve()

    def test_main_merges_user_ignores_with_short_flag(self, monkeypatch, tmp_path: Path):
        (tmp_path / "a.py").write_text("1")
        monkeypatch.setattr(sys, "argv", ["main.py", str(tmp_path), "-i", " build,,dist, "])

        with patch("main.print_to_terminal") as mock_print, patch(
            "main.calc_helper", return_value=(1, Counter({".py": 1}), 1, 1)
        ):
            main()

        _, _, _, _, _, ignore_dirs = mock_print.call_args[0]
        assert IGNORE_DIRS.issubset(ignore_dirs)
        assert {"build", "dist"}.issubset(ignore_dirs)

    def test_main_merges_user_ignores_with_long_flag(self, monkeypatch, tmp_path: Path):
        (tmp_path / "a.py").write_text("1")
        monkeypatch.setattr(sys, "argv", ["main.py", str(tmp_path), "--ignore", " build,,dist, "])

        with patch("main.print_to_terminal") as mock_print, patch(
            "main.calc_helper", return_value=(1, Counter({".py": 1}), 1, 1)
        ):
            main()

        _, _, _, _, _, ignore_dirs = mock_print.call_args[0]
        assert IGNORE_DIRS.issubset(ignore_dirs)
        assert {"build", "dist"}.issubset(ignore_dirs)

    def test_main_uses_only_default_ignores_when_flag_empty(self, monkeypatch, tmp_path: Path):
        (tmp_path / "a.py").write_text("1")
        monkeypatch.setattr(sys, "argv", ["main.py", str(tmp_path), "-i", ""])

        with patch("main.print_to_terminal") as mock_print, patch(
            "main.calc_helper", return_value=(1, Counter({".py": 1}), 1, 1)
        ):
            main()

        _, _, _, _, _, ignore_dirs = mock_print.call_args[0]
        assert ignore_dirs == IGNORE_DIRS

    def test_main_passes_scan_results_to_print_to_terminal(self, monkeypatch, tmp_path: Path):
        (tmp_path / "main.py").write_text("print('hi')")
        file_counts = Counter({".py": 1})
        monkeypatch.setattr(sys, "argv", ["main.py", str(tmp_path)])

        with patch("main.print_to_terminal") as mock_print, patch(
            "main.calc_helper", return_value=(1, file_counts, 16, 1)
        ) as mock_calc:
            main()

        _, ignore_dirs = mock_calc.call_args[0]
        mock_print.assert_called_once_with(
            tmp_path.resolve(), 1, file_counts, 16, 1, ignore_dirs
        )


class TestUserInput:
    def test_print_to_terminal_copies_tree_when_user_confirms(self, monkeypatch, tmp_path: Path):
        (tmp_path / "a.py").write_text("1")
        monkeypatch.setattr("app.export.Confirm.ask", lambda prompt: True)

        with patch("app.export.pyperclip.copy") as mock_copy:
            print_to_terminal(tmp_path, 1, Counter({".py": 1}), 1, 1, set())

        mock_copy.assert_called_once()
        assert "a.py" in mock_copy.call_args[0][0]

    def test_print_to_terminal_skips_copy_when_user_declines(self, monkeypatch, tmp_path: Path):
        (tmp_path / "a.py").write_text("1")

        def confirm(prompt):
            return "clipboard" not in prompt

        monkeypatch.setattr("app.export.Confirm.ask", confirm)

        with patch("app.export.pyperclip.copy") as mock_copy:
            print_to_terminal(tmp_path, 1, Counter({".py": 1}), 1, 1, set())

        mock_copy.assert_not_called()

    def test_print_to_terminal_writes_markdown_when_user_confirms(self, monkeypatch, tmp_path: Path):
        (tmp_path / "a.py").write_text("1")
        monkeypatch.chdir(tmp_path)

        def confirm(prompt):
            return "clipboard" not in prompt

        monkeypatch.setattr("app.export.Confirm.ask", confirm)
        monkeypatch.setattr("builtins.input", lambda prompt: "report")

        print_to_terminal(tmp_path, 1, Counter({".py": 1}), 1, 1, set())

        content = (tmp_path / "report.md").read_text(encoding="utf-8")
        assert content.startswith(HEADING)
        assert "a.py" in content

    def test_print_to_terminal_skips_markdown_when_user_declines(self, monkeypatch, tmp_path: Path):
        (tmp_path / "a.py").write_text("1")
        monkeypatch.chdir(tmp_path)

        def confirm(prompt):
            return "Markdown" not in prompt

        monkeypatch.setattr("app.export.Confirm.ask", confirm)

        print_to_terminal(tmp_path, 1, Counter({".py": 1}), 1, 1, set())

        assert list(tmp_path.iterdir()) == [tmp_path / "a.py"]
