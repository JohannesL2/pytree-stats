from __future__ import annotations

from rich.tree import Tree 
from rich.console import Console
from rich.filesize import decimal
from collections import Counter
from rich.table import Table


# Own functions
from app.core import generate_tree
from app.export import handle_markdown, handle_copy

console = Console(record=True)

def return_summary(file_counts: Counter) -> Table:
    """Creates and returns a table with file statistics."""
    tb_obj = Table(title="File statistics", title_style="bold magenta", show_header=True, header_style="bold cyan")

    tb_obj.add_column("File type", style="dim")
    tb_obj.add_column("Quantity", justify="right")

    for ext, count in file_counts.most_common():
        label = ext if ext else "No extension"
        tb_obj.add_row(label, str(count))
    
    return tb_obj

def print_to_terminal(root, total_files, file_counts, total_size, total_folders, ignore):
    """handles the printing of all text in the Terminal"""
    t_obj = Tree(f":open_file_folder: [bold cyan]{root.name}[/bold cyan]", guide_style="bright_black")
    generate_tree(root, t_obj, ignore)
        
    # Capture tree as string
    tree_console = Console(record=True)
    tree_console.print(t_obj)
    tree_text_only = tree_console.export_text()
    print("\n")
    # Print Summary to Terminal
    summary_table = return_summary(file_counts)
    summary_console = Console(record=True)
    summary_console.print(summary_table)
    summary_console.print("\n")
    summary_console.print(f"[bold cyan]Total files scanned:[/bold cyan] {total_files}")
    summary_console.print(f"[bold cyan]Total folders scanned:[/bold cyan] {total_folders}")
    summary_console.print(f"[bold cyan]Total size:[/bold cyan] {decimal(total_size)}")
    summary_text_only = summary_console.export_text()
    handle_copy(tree_text_only)
    handle_markdown(summary_text_only, tree_text_only)



    