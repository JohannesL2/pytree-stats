from pathlib import Path
from unittest.mock import patch

from rich.console import Console
from rich.tree import Tree

from app.core import generate_tree


class TestGenerateTree:
    def test_generate_tree_lists_nested_files_and_folders(self, tmp_path: Path):
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "main.py").write_text("print('hi')")
        (tmp_path / "README.md").write_text("# readme")

        tree = Tree("project")
        generate_tree(tmp_path, tree, set())

        console = Console(record=True)
        console.print(tree)
        text = console.export_text()

        assert "src" in text
        assert "main.py" in text
        assert "README.md" in text

    def test_generate_tree_sorts_folders_before_files(self, tmp_path: Path):
        (tmp_path / "z_file.txt").write_text("last")
        (tmp_path / "m_folder").mkdir()
        (tmp_path / "a_folder").mkdir()

        tree = Tree("project")
        generate_tree(tmp_path, tree, set())

        console = Console(record=True)
        console.print(tree)
        text = console.export_text()

        assert text.index("a_folder") < text.index("m_folder")
        assert text.index("m_folder") < text.index("z_file.txt")

    def test_generate_tree_skips_hidden_entries(self, tmp_path: Path):
        (tmp_path / "visible.py").write_text("keep")
        (tmp_path / ".hidden").mkdir()
        (tmp_path / ".hidden" / "secret.py").write_text("skip")
        (tmp_path / ".gitignore").write_text("skip")

        tree = Tree("project")
        generate_tree(tmp_path, tree, set())

        console = Console(record=True)
        console.print(tree)
        text = console.export_text()

        assert "visible.py" in text
        assert ".hidden" not in text
        assert ".gitignore" not in text
        assert "secret.py" not in text

    def test_generate_tree_skips_ignored_directories(self, tmp_path: Path):
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "main.py").write_text("keep")
        (tmp_path / "build").mkdir()
        (tmp_path / "build" / "out.js").write_text("skip")

        tree = Tree("project")
        generate_tree(tmp_path, tree, {"build"})

        console = Console(record=True)
        console.print(tree)
        text = console.export_text()

        assert "src" in text
        assert "main.py" in text
        assert "build" not in text
        assert "out.js" not in text

    def test_generate_tree_shows_file_sizes(self, tmp_path: Path):
        file_path = tmp_path / "notes.txt"
        file_path.write_text("hello")

        tree = Tree("project")
        generate_tree(tmp_path, tree, set())

        console = Console(record=True)
        console.print(tree)
        text = console.export_text()

        assert "notes.txt" in text
        assert str(file_path.stat().st_size) in text

    def test_generate_tree_shows_icons_for_file_types(self, tmp_path: Path):
        (tmp_path / "main.py").write_text("py")
        (tmp_path / "readme.md").write_text("md")
        (tmp_path / "config.json").write_text("{}")

        tree = Tree("project")
        generate_tree(tmp_path, tree, set())

        console = Console(record=True)
        console.print(tree)
        text = console.export_text()

        assert "🐍" in text
        assert "main.py" in text
        assert "📄" in text
        assert "readme.md" in text
        assert "⚙️" in text
        assert "config.json" in text

    def test_generate_tree_handles_empty_directory(self, tmp_path: Path):
        tree = Tree("project")
        generate_tree(tmp_path, tree, set())

        console = Console(record=True)
        console.print(tree)
        text = console.export_text()

        assert "project" in text
        assert text.strip() == "project"

    def test_generate_tree_skips_files_with_permission_error(self, tmp_path: Path):
        open_file = tmp_path / "open.py"
        open_file.write_text("ok")
        blocked_file = tmp_path / "secret.py"
        blocked_file.write_text("no access")

        real_stat = Path.stat

        # We mock Path.stat to immediately raise PermissionError for the blocked file
        def stat_with_denial(self, follow_symlinks=True):
            if self == blocked_file:
                raise PermissionError
            return real_stat(self, follow_symlinks=follow_symlinks)

        with patch.object(Path, "stat", stat_with_denial):
            tree = Tree("project")
            generate_tree(tmp_path, tree, set())

            console = Console(record=True)
            console.print(tree)
            text = console.export_text()

        assert "open.py" in text
        assert "secret.py" not in text