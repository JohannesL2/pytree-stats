from __future__ import annotations

from pathlib import Path
from rich.console import Console
from rich.prompt import Confirm
import pyperclip

from app.global_ import HEADING

console = Console(record=True)

def handle_copy(tree_text) -> None:
    """Ask if the user want the information copy to his/her clipboard"""
    print("")
    if Confirm.ask("Do you want to copy the tree structure to clipboard?"):
        try:
            
            pyperclip.copy(tree_text)
            console.print("[bold green] Copied to clipboard![/bold green]")
        except Exception as e:
            console.print(f"[bold red] Failed to copy to clipboard: {e}[/bold red]")
    else:
        console.print("[yellow]Skip copying to clipboard.[/yellow]")        

def handle_markdown(summary_text_only:str, tree_text_only:str) ->None:
    """Ask if the user wants the information delivered in a markdown file"""
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
            console.print(f"[bold red] Failed to download the markdown file: {e}[/bold red]")
    else:
        console.print("[yellow]Skip downloading markdown file.[/yellow]")