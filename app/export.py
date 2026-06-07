from __future__ import annotations

from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.prompt import Confirm
import pyperclip

from app.global_ import HEADING

DEFAULT_MARKDOWN_FILE = "pytree-stats.md"


def copy(tree_text: str, console: Console) -> None:
    try:
        pyperclip.copy(tree_text)
        console.print("[bold green] Copied to clipboard![/bold green]")
    except Exception as e:
        console.print(f"[bold red] Failed to copy to clipboard: {e}[/bold red]")


def markdown(summary_text_only: str, tree_text_only: str, console: Console, file_name: Optional[str] = DEFAULT_MARKDOWN_FILE) -> None:
    try:
        if file_name is None:
            file_name = DEFAULT_MARKDOWN_FILE

        if Path(file_name).suffix.lower() != ".md":
            file_name += ".md"

        with open(file_name, "w", encoding="utf-8") as f:
            f.write(f"{HEADING}\n")
            f.write(f"```text\n{tree_text_only}\n```\n\n")
            f.write(f"```text\n{summary_text_only}\n```\n")

        console.print(f"[bold green]Markdown saved to {file_name}![/bold green]")
    except Exception as e:
        console.print(f"[bold red] Failed to download the markdown file: {e}[/bold red]")


def handle_copy(tree_text:str, console:Console) -> None:
    """Ask if the user want the information copy to his/her clipboard"""
    print("")
    if Confirm.ask("Do you want to copy the tree structure to clipboard?"):
        copy(tree_text, console)
    else:
        console.print("[yellow]Skip copying to clipboard.[/yellow]")        

def handle_markdown(summary_text_only:str, tree_text_only:str, console:Console) ->None:
    """Ask if the user wants the information delivered in a markdown file"""
    print("")
    if Confirm.ask("Do you want to download the tree structure as a Markdown?"):
        file_name = input("Name your file: ")
        print("")
        while not Confirm.ask(f"Are you sure you want to name the file {file_name}?"):
            file_name = input("Name your file: ")
            print("")
        markdown(summary_text_only, tree_text_only, console, file_name)
    else:
        console.print("[yellow]Skip downloading markdown file.[/yellow]")
