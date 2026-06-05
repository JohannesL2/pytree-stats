import os
from pathlib import Path
from rich.tree import Tree 
from rich.console import Console
from rich.prompt import Confirm
from rich.filesize import decimal
from rich.markup import escape
from rich.text import Text
from collections import Counter
from rich.table import Table
import pyperclip
import argparse

HEADING = "## Project Structure"
IGNORE_DIRS = {".git", "__pycache__", "node_modules", "venv", ".venv", ".DS_Store"}

def generate_tree(directory: Path, node: Tree, ignore_dirs: set):
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
            file_size = decimal(path.stat().st_size)
            text_filename.append(f" ({file_size})", "italic white")
            
            node.add(Text(f"{icon} ") + text_filename)

# Summarize and count files

def print_summary(file_counts: Counter):
    """Creates and write a table with file statistics."""
    tb_obj = Table(title="File statistics", title_style="bold magenta", show_header=True, header_style="bold cyan")

    tb_obj.add_column("File type", style="dim")
    tb_obj.add_column("Quantity", justify="right")

    for ext, count in file_counts.most_common():
        label = ext if ext else "No extension"
        tb_obj.add_row(label, str(count))
    
    return tb_obj

def main():
    parser = argparse.ArgumentParser(description="Generate a directory tree and file statistics.")
    parser.add_argument("path", nargs="?", default=Path.cwd(), type=Path, help="Directory to scan (defaults to current working directory)")
    parser.add_argument("-i", "--ignore", default="", help="List of directories to ignore (seperate by comma)")

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

    c = Console(record=True)
    all_extensions = []

    def collect_stats(directory: Path):
        total_size = 0
        total_folders = 1
        for path in directory.rglob("*"):
            if any(part.startswith('.') or part in ignore_dirs for part in path.parts):
                continue
            if path.is_dir():
                total_folders += 1
            elif path.is_file():
                all_extensions.append(path.suffix.lower())
                total_size += path.stat().st_size
        return total_size, total_folders
    
    total_size, total_folders = collect_stats(root)
    total_files = len(all_extensions)
    file_counts = Counter(all_extensions)

    t_obj = Tree(f":open_file_folder: [bold cyan]{root.name}[/bold cyan]", guide_style="bright_black")
    generate_tree(root, t_obj, ignore_dirs)
    
    # Capture tree as string
    tree_console = Console(record=True)
    tree_console.print(t_obj)
    tree_text_only = tree_console.export_text()
    print("\n")
    
    # Capture summary table and totals for markdown export
    summary_table = print_summary(file_counts)
    summary_console = Console(record=True)
    summary_console.print(summary_table)
    summary_console.print("\n")
    summary_console.print(f"[bold cyan]Total files scanned:[/bold cyan] {total_files}")
    summary_console.print(f"[bold cyan]Total folders scanned:[/bold cyan] {total_folders}")
    summary_console.print(f"[bold cyan]Total size:[/bold cyan] {decimal(total_size)}")
    summary_text_only = summary_console.export_text()
    
    # Print to the terminal screen
    """ c.print(summary_table)
    c.print("\n")
    c.print(f"[bold cyan]Total files scanned:[/bold cyan] {total_files}")
    c.print(f"[bold cyan]Total folders scanned:[/bold cyan] {total_folders}")
    c.print(f"[bold cyan]Total size:[/bold cyan] {decimal(total_size)}") """
    # Copy the tree to clipboard
    print("")
    if Confirm.ask("Do you want to copy the tree structure to clipboard?"):
        try:
            tree_text = c.export_text()
            pyperclip.copy(tree_text)
            c.print("[bold green] Copied to clipboard![/bold green]")
        except Exception as e:
            c.print(f"[bold red] Failed to copy to clipboard: {e}[/bold red]")
    else:
        c.print("[yellow]Skip copying to clipboard.[/yellow]")        

    # Download as a markdown file

    
    print("")
    if Confirm.ask("Do you want to download the tree structure as a Markdown?"):
        try:
            file_name = input("Name your file: ")
            print("")
            while not Confirm.ask(f"Are you sure you want to name the file {file_name}?"):
                file_name = input("Name your file: ")
                print("")
            if Path(file_name).suffix.lower() != ".md":
                file_name += ".md"
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(f"{HEADING}\n")
            
                f.write(f"```text\n{tree_text_only}\n```\n\n")
                
                f.write(f"```{summary_text_only}\n```\n")

        except Exception as e:
            c.print("[yellow]Skip downloading to Markdown")

if __name__ == "__main__":
    main()
