from __future__ import annotations

from pathlib import Path
from rich.tree import Tree 
from rich.filesize import decimal
from rich.markup import escape
from rich.text import Text
from rich.console import Console

console = Console(record=True)

def generate_tree(directory: Path, node: Tree, ignore_dirs: set) -> None:
    """Function that builds a file structure tree"""
    accessible_entries = []
    
    try:
        # Step 1: Safely gather entries we have permission to touch
        for path in Path(directory).iterdir():
            try:
                # Triggers a stat call via is_file() to safely check permissions early
                path.is_file()
                accessible_entries.append(path)
            except PermissionError:
                # Skip the restricted file silently and continue with the rest
                continue
    except PermissionError:
        # If the parent directory itself is completely restricted
        return

    # Step 2: Safe sorting (folders first, then files) on accessible files only
    entries = sorted(accessible_entries, key=lambda p: (p.is_file(), p.name.lower()))

    for path in entries:
        # Ignore hidden files/folders and ignored directories
        if path.name.startswith(".") or path.name in ignore_dirs:
            continue

        try:
            is_directory = path.is_dir()
            
            if is_directory:
                # New branch for folders
                branch = node.add(
                    f"[bold blue]📂 {escape(path.name)}[/bold blue]",
                    guide_style="bright_blue"
                )
                generate_tree(path, branch, ignore_dirs)
            else:
                # Handle files with icons
                text_filename = Text(path.name)
                
                # Determine icon and color based on file extension
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

                # Get file size
                file_size = decimal(path.stat().st_size)
                text_filename.append(f" ({file_size})", "italic white")
                
                node.add(Text(f"{icon} ") + text_filename)

        except PermissionError:
            continue