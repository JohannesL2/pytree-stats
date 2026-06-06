from __future__ import annotations

from pathlib import Path
from rich.tree import Tree 
from rich.filesize import decimal
from rich.markup import escape
from rich.text import Text
from rich.console import Console

console = Console(record=True)
def generate_tree(directory: Path, node: Tree, ignore_dirs: set)->None:
    """Function that builds a file structure tree"""
    # Sort folders first then files
    paths = sorted(Path(directory).iterdir(), key=lambda p: (p.is_file(), p.name.lower()))

    for path in paths:
        # Ignore hidden maps like .git .gitignore
        if path.name.startswith(".") or path.name in ignore_dirs:
            continue

        if path.is_dir():
            # New branch for folders
            style = "bold blue"
            branch = node.add(
                f"[bold blue]📂 {escape(path.name)}[/bold blue]",
                guide_style="bright_blue"
            )
            generate_tree(path, branch, ignore_dirs)
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
            try:
                file_size = decimal(path.stat().st_size)
            except PermissionError:
                console.print(f"[yellow]WARNING:[/yellow] Skipping file (permission denied): {path}")
                continue
            
            text_filename.append(f" ({file_size})", "italic white")

            # Add file size for convenience
            
            
            node.add(Text(f"{icon} ") + text_filename)

