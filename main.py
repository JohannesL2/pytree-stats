from __future__ import annotations

from pathlib import Path
import argparse

from app import IGNORE_DIRS, calc_helper, print_to_terminal, CopyAction, MarkdownAction


def main()->None:
    """Main Application"""
    parser = argparse.ArgumentParser(description="Generate a directory tree and file statistics.")
    parser.add_argument("path", nargs="?", default=Path.cwd(), type=Path, help="Directory to scan (defaults to current working directory)")
    parser.add_argument("-i", "--ignore", default="", help="List of directories to ignore (separate by comma)")
    parser.add_argument("-c", "--copy", nargs=0, action=CopyAction, default=False, help=argparse.SUPPRESS)
    parser.add_argument(
        "-m",
        "--markdown",
        nargs="?",
        metavar="FILENAME",
        action=MarkdownAction,
        default=False,
        help="Save output to a markdown file",
    )

    args = parser.parse_args()

    user_ignores = {item.strip() for item in args.ignore.split(",") if item.strip()}
    ignore_dirs = IGNORE_DIRS | user_ignores

    root = args.path.resolve()

    if not root.exists():
        print(f"Error: '{root}' does not exist.")
        return

    if not root.is_dir():
        print(f"Error: '{root}' is not a directory.")
        return
    
    total_files, file_counts, total_size, total_folder = calc_helper(root, ignore_dirs)

    print_to_terminal(
        root,
        total_files,
        file_counts,
        total_size,
        total_folder,
        ignore_dirs,
        copy_output=args.copy,
        markdown_output=args.markdown,
    )

if __name__ == "__main__":
    main()
