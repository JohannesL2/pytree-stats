import os
from pathlib import Path
from rich.tree import Tree
from rich.console import Console
from rich.filesize import decimal
from rich.markup import escape
from rich.text import Text
from collections import Counter
from rich.table import Table

IGNORE_DIRS = {".git", "__pycache__", "node_modules", "venv", ".venv", ".DS_Store"}

def generate_tree(directory: Path, node: Tree):
    """Function that builds a file structure tree"""
    # Sort folders first then files
    paths = sorted(Path(directory).iterdir(), key=lambda p: (p.is_file(), p.name.lower()))

    for path in paths:
        # Ignore hidden maps like .git .gitignore
        if path.name.startswith("."):
            continue

        if path.is_dir():
            # New branch for folders
            style = "bold blue"
            branch = node.add(
                f"[bold blue]📂 {escape(path.name)}[/bold blue]",
                guide_style="bright_blue"
            )
            generate_tree(path, branch)
        else:
            # Handle files with icons
            text_filename = Text(path.name)
            
            # File extension colors
            if path.suffix == ".py":
                text_filename.stylize("green")
                icon = "🐍"
            elif path.suffix in [".md", ".txt"]:
                text_filename.stylize("yellow")
                icon = "📄"
            elif path.suffix in [".json", ".yaml", ".yml"]:
                text_filename.stylize("magenta")
                icon = "⚙️"
            elif path.suffix in [".java"]:
                text_filename.stylize("magenta")
                icon = "☕️"
            elif path.suffix in [".kt"]:
                text_filename.stylize("magenta")
                icon = "🟣"
            elif path.suffix in [".class"]:
                text_filename.stylize("magenta")
                icon = "🛡️"
            else:
                icon = "📄"

            # Add file size for convenience
            file_size = decimal(path.stat().st_size)
            text_filename.append(f" ({file_size})", "italic white")
            
            node.add(Text(f"{icon} ") + text_filename)

# Summarize and count files

def print_summary(file_counts: Counter, console: Console):
    """Creates and write a table with file statistics."""
    tb_obj = Table(title="File statistics", title_style="bold magenta", show_header=True, header_style="bold cyan")

    tb_obj.add_column("File type", style="dim")
    tb_obj.add_column("Quantity", justify="right")

    for ext, count in file_counts.most_common():
        label = ext if ext else "No extension"
        tb_obj.add_row(label, str(count))
    
    console.print("\n")
    console.print(tb_obj)

def main():
    c = Console()
    root = Path.cwd()  # Run in current folder
    all_extensions = []

    def collect_stats(directory: Path):
        for path in directory.rglob("*"):
            if path.is_file() and not any(part.startswith('.') or part in IGNORE_DIRS for part in path.parts):
                all_extensions.append(path.suffix.lower())
    
    collect_stats(root)
    file_counts = Counter(all_extensions)

    t_obj = Tree(f":open_file_folder: [bold cyan]{root.name}[/bold cyan]", guide_style="bright_black")
    generate_tree(root, t_obj)

    c.print(t_obj)
    print_summary(file_counts, c)

if __name__ == "__main__":
    main()