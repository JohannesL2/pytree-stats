from collections import Counter
from pathlib import Path

from app.stats import calc_helper, collect_stats


class TestCollectStats:
    def test_collect_stats_counts_files_folders_and_size(self, tmp_path: Path):
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "main.py").write_text("print(hi)")
        (tmp_path / "src" / "random.PY").write_text("Random Content")
        (tmp_path / "src" / "utils.txt").write_text("x = 1")
        (tmp_path / "README.md").write_text("# readme")

        total_size, total_folders, all_extensions = collect_stats(tmp_path, ignore=set())

        assert Counter(all_extensions) == Counter({".py": 2, ".txt": 1, ".md": 1})
        assert total_folders == 2
        assert total_size == sum(
            path.stat().st_size
            for path in [
                tmp_path / "src" / "main.py",
                tmp_path / "src" / "random.PY",
                tmp_path / "src" / "utils.txt",
                tmp_path / "README.md",
            ]
        )

    def test_collect_stats_returns_empty_results_for_empty_directory(self, tmp_path: Path):
        total_size, total_folders, all_extensions = collect_stats(tmp_path, ignore=set())

        assert total_size == 0
        assert total_folders == 1
        assert all_extensions == []

    def test_collect_stats_skips_ignored_directories(self, tmp_path: Path):
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "main.py").write_text("keep")
        (tmp_path / "build").mkdir()
        (tmp_path / "build" / "out.js").write_text("skip")

        total_size, total_folders, all_extensions = collect_stats(tmp_path, ignore={"build"})

        assert all_extensions == [".py"]
        assert total_folders == 2
        assert total_size == (tmp_path / "src" / "main.py").stat().st_size

    def test_collect_stats_skips_hidden_paths(self, tmp_path: Path):
        (tmp_path / "visible.py").write_text("keep")
        (tmp_path / ".hidden").mkdir()
        (tmp_path / ".hidden" / "secret.py").write_text("skip")
        (tmp_path / ".git").mkdir()
        (tmp_path / ".git" / "config").write_text("skip")

        _, _, all_extensions = collect_stats(tmp_path, ignore=set())

        assert all_extensions == [".py"]

    def test_collect_stats_includes_files_without_extension(self, tmp_path: Path):
        (tmp_path / "Makefile").write_text("all:")
        (tmp_path / "app.py").write_text("run")

        _, _, all_extensions = collect_stats(tmp_path, ignore=set())

        assert Counter(all_extensions) == Counter({"": 1, ".py": 1})


class TestCalcHelper:
    def test_calc_helper_returns_aggregate_stats(self, tmp_path: Path):
        (tmp_path / "a.py").write_text("1")
        (tmp_path / "b.py").write_text("22")
        (tmp_path / "c.md").write_text("# Text")

        total_files, file_counts, total_size, total_folders = calc_helper(tmp_path, ignore=set())

        assert total_files == 3
        assert file_counts == Counter({".py": 2, ".md": 1})
        assert total_folders == 1
        assert total_size == sum(
            path.stat().st_size for path in [tmp_path / "a.py", tmp_path / "b.py", tmp_path / "c.md"]
        )

    def test_calc_helper_respects_ignore_set(self, tmp_path: Path):
        (tmp_path / "keep.py").write_text("1")
        (tmp_path / "vendor").mkdir()
        (tmp_path / "vendor" / "lib.py").write_text("skip")

        total_files, file_counts, total_size, total_folders = calc_helper(tmp_path, ignore={"vendor"})

        assert total_files == 1
        assert file_counts == Counter({".py": 1})
        assert total_folders == 1
        assert total_size == (tmp_path / "keep.py").stat().st_size
