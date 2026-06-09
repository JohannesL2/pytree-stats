from __future__ import annotations

from typing import Optional

from rich.tree import Tree 
from rich.console import Console
from rich.filesize import decimal
from collections import Counter
from rich.table import Table


# Own functions
from app.core import generate_tree
from app.export import copy, markdown, handle_markdown, handle_copy



def return_summary(file_counts: Counter) -> Table:
    """Creates and returns a table with file statistics."""
    tb_obj = Table(title="File statistics", title_style="bold magenta", show_header=True, header_style="bold cyan")

    tb_obj.add_column("File type", style="dim")
    tb_obj.add_column("Quantity", justify="right")

    for ext, count in file_counts.most_common():
        label = ext if ext else "No extension"
        tb_obj.add_row(label, str(count))
    
    return tb_obj

def print_to_terminal(
    root,
    total_files,
    file_counts,
    total_size,
    total_folders,
    ignore,
    _console: Optional[Console] = None,
    copy_output: bool = False,
    markdown_output: bool = False,
):
    """handles the printing of all text in the Terminal"""
    # Skapa en helt egen, isolerad konsol för trädet
    tree_console = Console(record=True)

    t_obj = Tree(f":open_file_folder: [bold cyan]{root.name}[/bold cyan]", guide_style="bright_black")
    generate_tree(root, t_obj, ignore)
        
    # Capture tree as string (Helt isolerat i tree_console)
    tree_console.print(t_obj)
    tree_text_only = tree_console.export_text()
    print("\n")
    
    # Skapa eller använd konsolen för sammanfattningen
    if _console is None:
        _console = Console(record=True)

    sum_console = return_summary(file_counts)
    _console.print(sum_console)
    _console.print("\n")
    _console.print(f"[bold cyan]Total files scanned:[/bold cyan] {total_files}")
    _console.print(f"[bold cyan]Total folders scanned:[/bold cyan] {total_folders}")
    _console.print(f"[bold cyan]Total size:[/bold cyan] {decimal(total_size)}")
    summary_text_only = _console.export_text()

    if copy_output:
        copy(f"{tree_text_only}\n{summary_text_only}", _console)

    if markdown_output:
        file_name = markdown_output if isinstance(markdown_output, str) else None
        markdown(summary_text_only, tree_text_only, _console, file_name=file_name)

    if copy_output or markdown_output:
        return

    handle_copy(tree_text_only, _console)
    handle_markdown(summary_text_only, tree_text_only, _console)