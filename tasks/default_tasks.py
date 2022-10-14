# tasks/default_tasks.py
from typing import List, Optional
from inspect import currentframe, getframeinfo
from time import sleep

import src.myaml as yaml
from rich import print
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress
from rich.style import Style
from rich.text import Text
from rich.traceback import install
from src.default import (
    Default,
    generate_default_book_word,
    generate_default_cover,
    generate_default_cover_path,
    generate_default_filename,
    generate_default_output,
    generate_default_section_chapters,
    generate_default_section_filenames,
    generate_default_section_filepaths,
    generate_default_sections,
    generate_default_input_files,
    generate_default_file
)
from src.log import console
from src.atlas import sg

install()

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
        task = progress.add_task(
            "[bold green]Generating Default Book Words...", total=10
        )
        for book in range(1, 11):
            progress.update(
                task,
                advance=1,
                description=f"[bold green]Generating Default Book Words... {book}/10",
            )
            book_word = str(generate_default_book_word(book, True)).capitalize()
            console.print(default_panel(book, "Generated Book Word", book_word, 53))
        console.print(finished("Book_Words", 70))


# generate_default_book_words()


def generate_default_outputs():
    """Generate default output for all books in the Atlas."""
    with Progress() as progress:
        task = progress.add_task("[bold green]Generating Default Output...", total=10)
        for book in range(1, 11):
            progress.update(
                task,
                advance=1,
                description=f"[bold green]Generating Default Output... {book}/10",
            )
            output = str(generate_default_output(book=book, save=True))  # type: ignore
        console.print(finished("Outputs", 85))


# generate_default_outputs()


def generate_default_filenames():
    """Generate default filename for all books in the Atlas."""
    with Progress() as progress:
        task = progress.add_task("[bold green]Generating Default Filename...", total=10)
        for book in range(1, 11):
            progress.update(
                task,
                advance=1,
                description=f"[bold green]Generating Default Filename... {book}/10",
            )
            filename = generate_default_filename(book=book, save=True)  # type: ignore
        console.print(finished("Filenames", 96))


# generate_default_filenames()


def generate_default_filepaths_task():
    """Generate the filepaths for all default files."""
    with Progress() as progress:
        task = progress.add_task(
            "[bold green]Generating Default Filepaths...", total=10
        )
        for book in range(1, 11):
            progress.update(
                task,
                advance=1,
                description=f"[bold green]Generating Default Filepaths... {book}/10",
            )
            filepath = generate_default_file(book=book, save=True)  # type: ignore

        frameinfo = getframeinfo(currentframe()) # type: ignore
        current_lineno = int(frameinfo.lineno) + 2
        console.print(finished("Filepaths", current_lineno))

generate_default_filepaths_task()


def generate_default_covers():
    """Generate default cover for all books in the Atlas."""
    with Progress() as progress:
        task = progress.add_task("[bold green]Generating Default Cover...", total=10)
        for book in range(1, 11):
            progress.update(
                task,
                advance=1,
                description=f"[bold green]Generating Default Cover... {book}/10",
            )
            cover = generate_default_cover(book=book, save=True)  # type: ignore
        console.print(finished("Covers", 107))


# generate_default_covers()


def generate_default_cover_paths():
    """Generate default cover path for all books."""
    with Progress() as progress:
        task = progress.add_task(
            "[bold green]Generating Default Cover Path...", total=10
        )
        for book in range(1, 11):
            progress.update(
                task,
                advance=1,
                description=f"[bold green]Generating Default Cover Path... {book}/10",
            )
            cover_path = generate_default_cover_path(book=book, save=True)  # type: ignore
        console.print(finished("Cover Paths", 122))


# generate_default_cover_paths()


def generate_default_sections_task():
    """Generate default sections for all books."""
    with Progress() as progress:
        task = progress.add_task("[bold green]Generating Default Sections...", total=10)
        for book in range(1, 11):
            progress.update(
                task,
                advance=1,
                description=f"[bold green]Generating Default Sections... {book}/10",
            )
            sections = generate_default_sections(book)  # type: ignore
        console.print(finished("Sections", 135))


# generate_default_sections_task()


def generate_default_section_chapters_task():
    """Generate default section chapters for all books."""
    with Progress() as progress:
        task = progress.add_task(
            "[bold green]Generating Default Section Chapters...", total=17
        )
        for section in range(1, 18):
            progress.update(
                task,
                advance=1,
                description=f"[bold green]Generating Section {section} Chapters...",
            )

            section_chapters = generate_default_section_chapters(section)  # type: ignore
        console.print(finished("Section Chapters", 150))


# generate_default_section_chapters_task()


def generate_default_section_filenames_tasks():
    """Generate default section filenames for all book sections."""
    with Progress() as progress:
        task = progress.add_task(
            "[bold green]Generating Default Section Filenames...", total=17
        )
        for section in range(1, 18):
            progress.update(
                task,
                advance=1,
                description=f"[bold green]Generating Section {section} Filenames...",
            )
            section_filenames = generate_default_section_filenames(section)  # type: ignore

        frameinfo = getframeinfo(currentframe()) # type: ignore
        current_lineno = int(frameinfo.lineno) + 2
        console.print(finished("Section Filenames", current_lineno))


# generate_default_section_filenames_tasks()


def generate_default_section_filepaths_task():
    """Generate default section filepaths for all book sections."""
    with Progress() as progress:
        task = progress.add_task(
            "[bold green]Generating Default Section Filepaths...", total=17
        )
        for section in range(1, 18):
            progress.update(
                task,
                advance=1,
                description=f"[bold green]Generating Section {section} Filepaths...",
            )
            section_filepaths = generate_default_section_filepaths(section)  # type: ignore

        frameinfo = getframeinfo(currentframe()) # type: ignore
        current_lineno = int(frameinfo.lineno) + 2
        console.print(finished("Section Filepaths", current_lineno))


# generate_default_section_filepaths_task()


def generate_default_input_files_task():
    """Generate the input files for the default files."""
    with Progress() as progress:
        task = progress.add_task(
            "[bold green]Generating Default Input Files...", total=10
        )
        for book in range(1, 11):
            progress.update(
                task,
                advance=1,
                description=f"[bold green]Generating Book {book}'s Input Files...",
            )
            input_files = generate_default_input_files(book)  # type: ignore
            sleep(1)

        frameinfo = getframeinfo(currentframe()) # type: ignore
        current_lineno = int(frameinfo.lineno) + 2
        console.print(finished("Input Files", current_lineno))


# generate_default_input_files_task()


def generate_default_resource_files_task():
    """Generate the resource files for the default files."""
    with Progress() as progress:
        task = progress.add_task(
            "[bold green]Generating Default Resource Files...", total=10
        )
        for book in range(1, 11):
            progress.update(
                task,
                advance=1,
                description=f"[bold green]Generating Book {book}'s Resource Files...",
            )
            resource_files = generate_default_resource_files(book)  # type: ignore
            sleep(0.25)

        frameinfo = getframeinfo(currentframe()) # type: ignore
        current_lineno = int(frameinfo.lineno) + 2
        console.print(finished("Resource Files", current_lineno))


# generate_default_resource_files_task()

def generate_default_files_task():
    """Generate the default files for all books."""
    with Progress() as progress:
        task = progress.add_task("[bold green]Generating Default Files...", total=10)

        for book in range(1, 11):
            progress.update(
                task,
                advance=1,
                description=f"[bold green]Generating Book {book}'s Default Files...",
            )
            default_file = generate_default_file(book)  # type: ignore
            sleep(0.25)

        frameinfo = getframeinfo(currentframe()) # type: ignore
        current_lineno = int(frameinfo.lineno) + 2
        console.print(finished("Default Files", current_lineno))

# generate_default_files_task()


def write_default_files():
    with Progress() as progress:
        task = progress.add_task("[bold green]Writing Default Files...", total=10)

        for book in range(1, 11):
            progress.update(
                task,
                advance=1,
                description=f"[bold green]Writing Book {book}'s Default Files...",
            )
            sg()
            default_doc = Default.objects(book=book).first() # type: ignore
            filepath = default_doc.filepath
            content = default_doc.content
            with open (filepath, "w") as outfile:
                outfile.write(content)

            frameinfo = getframeinfo(currentframe()) # type: ignore
            current_lineno = int(frameinfo.lineno) + 2
            console.print(finished(f"Book {book} Default File", current_lineno))

        frameinfo = getframeinfo(currentframe()) # type: ignore
        current_lineno = int(frameinfo.lineno) + 2
        console.print(finished("Default Files", current_lineno))


write_default_files()
