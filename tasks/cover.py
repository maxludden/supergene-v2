from enum import IntEnum
from pathlib import Path

from rich import print
from rich.panel import Panel
from rich.progress import Progress
from rich.text import Text
from src.atlas import sg
from src.cover import (Coverpage, generate_html, generate_html_path, get_html,
                       get_html_path)
from src.log import BASE, console, log

choices = [1,2,3,4,5,6,7,8,9,10]

class InvalidBook(ValueError):
    pass

def generate_covers():
    with Progress(console=console,) as progress:
        covers = progress.add_task("[white]Creating Covers...", total=10)

        for book in range(1,11):
            sg()
            doc = Coverpage.objects(book=book).first() # type: ignore
            if doc:
                html_path = generate_html_path(book)
                html = generate_html(book)

                progress.advance(covers)
                console.log(
                    Panel(
                        Text(
                            f"Created cover for Book {doc.book}.",
                            justify="left",
                            style="white",
                        ),
                        title=Text(f"Created Cover", style="bold green"),
                        title_align="left",
                        expand=False,
                        border_style="green",
                    )
                )
