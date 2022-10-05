from pathlib import Path
from typing import Any, List, Optional

import src.myaml as yaml
from rich import print
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress
from rich.style import Style
from rich.text import Text
from src.atlas import max_title, sg
from src.default import Default, generate_default_output, generate_default_book_word, generate_default_filename, generate_default_cover,generate_default_cover_path, generate_default_sections, generate_default_section_filenames, generate_default_section_filepaths
from src.log import BASE, console, log


def default_panel(
    book: int,
    key: str = "Key",
    value: str | int | List | Markdown = "Value",
    line: int = 1,
    title: Optional[str] = None,
    get: bool = False,
) -> Panel:
    if title:
        title = title
    else:
        title = f"Book {book}'s Default File"

    if get:
        get_verb = "Retrieved"
    else:
        get_verb = "Generated"

    panel = Panel(
        f"[#eed4fc]{get_verb} {key}:[/][bold bright_white] {str(value)}[/]",
        title=Text(f"{title}", style=Style(color="#8e47ff", bold=True)),
        title_align="left",
        subtitle=f"[purple]tasks/default_tasks.py[/][#FFFFFF]|[/][#54c6ff]line {line}[/]",
        subtitle_align="right",
        border_style=Style(color="#5f00ff"),
        expand=True,
        width=80,
    )
    return panel


def finished(key: str, line: int) -> Panel:
    panel = Panel(
        f"[#eed4fc]Finished [/][bold bright_white] {key}[/]",
        title=Text(f"Default File Task", style=Style(color="#8e47ff", bold=True)),
        title_align="left",
        subtitle=f"[purple]tasks/default_tasks.py[/][#FFFFFF]|[/][#54c6ff]line {line}[/]",
        subtitle_align="right",
        border_style=Style(color="#5f00ff"),
        expand=True,
        width=80,
    )
    return panel

def generate_default_book_words():
    """Generate default book words for all books in the Atlas."""
    with Progress() as progress:
        task = progress.add_task("[bold green]Generating Default Book Words...", total=10)
        for book in range(1, 11):
            progress.update(task, advance=1, description=f"[bold green]Generating Default Book Words... {book}/10")
            book_word = str(generate_default_book_word(book, True)).capitalize()
            console.print(default_panel(book, "Generated Book Word", book_word, 53))
            log.info(f"Generated default book word for book {book}: {book_word}")
        console.print(
            finished("Book_Words", 70)
        )

# generate_default_book_words()

def generate_default_outputs():
    """Generate default output for all books in the Atlas."""
    with Progress() as progress:
        task = progress.add_task("[bold green]Generating Default Output...", total=10)
        for book in range(1, 11):
            progress.update(task, advance=1, description=f"[bold green]Generating Default Output... {book}/10")
            output = str(generate_default_output(book=book, save=True)) # type: ignore
        console.print(
            finished("Outputs", 85)
        )

# generate_default_outputs()

def generate_default_filenames():
    """Generate default filename for all books in the Atlas."""
    with Progress() as progress:
        task = progress.add_task("[bold green]Generating Default Filename...", total=10)
        for book in range(1, 11):
            progress.update(task, advance=1, description=f"[bold green]Generating Default Filename... {book}/10")
            filename = generate_default_filename(book=book, save=True) # type: ignore
        console.print(
            finished("Filenames", 96)
        )

# generate_default_filenames()

def generate_default_covers():
    """Generate default cover for all books in the Atlas."""
    with Progress() as progress:
        task = progress.add_task("[bold green]Generating Default Cover...", total=10)
        for book in range(1, 11):
            progress.update(task, advance=1, description=f"[bold green]Generating Default Cover... {book}/10")
            cover = generate_default_cover(book=book, save=True) # type: ignore
        console.print(
            finished("Covers", 107)
        )

# generate_default_covers()

def generate_default_cover_paths():
    """Generate default cover path for all books."""
    with Progress() as progress:
        task = progress.add_task("[bold green]Generating Default Cover Path...", total=10)
        for book in range(1, 11):
            progress.update(task, advance=1, description=f"[bold green]Generating Default Cover Path... {book}/10")
            cover_path = generate_default_cover_path(book=book, save=True) # type: ignore
        console.print(
            finished("Cover Paths", 122)
        )

# generate_default_cover_paths()

def generate_default_sections_task():
    """Generate default sections for all books."""
    with Progress() as progress:
        task = progress.add_task("[bold green]Generating Default Sections...", total=10)
        for book in range(1, 11):
            progress.update(task, advance=1, description=f"[bold green]Generating Default Sections... {book}/10")
            sections = generate_default_sections(book) # type: ignore
        console.print(
            finished("Sections", 135)
        )

# generate_default_sections_task()

def generate_default_chapters_task():
    """Generate chapters for all books."""
    with Progress() as progress:
        task = progress.add_task("[bold green]Generating Default Chapters...", total=10)
        for book in range(1, 11):
            progress.update(task, advance=1, description=f"[bold green]Generating Default Chapters... {book}/10")
            chapters = generate_default_chapters(book) # type: ignore
        console.print(
            finished("Chapters", 148)
        )

def generate_default_section_filenames_task():
    """Generate default section filenames for all sections."""
    with Progress() as progress:
        task = progress.add_task("[bold green]Generating Default Section Filenames...", total=17)
        for section in range(1, 18):
            progress.update(task, advance=1, description=f"[bold green]Generating Default Section Filenames... {section}/17")
            section_filenames = generate_default_section_filenames(section) # type: ignore
        console.print(
            finished("Section Filenames", 148)
        )

# generate_default_section_filenames_task()
