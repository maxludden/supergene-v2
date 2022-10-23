# tasks/book_tasks.py
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from multiprocessing import cpu_count
from pathlib import Path
from time import perf_counter

from rich import print
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress
from rich.text import Text
from sh import Command, RunningCommand
from src.atlas import max_title, sg
from src.book import (
    Book,
    book_gen,
    generate_book_cover,
    generate_book_cover_path,
    generate_book_default,
    generate_book_end,
    generate_book_output,
    generate_book_sections,
    generate_book_start,
    generate_book_title,
    generate_book_uuid,
    generate_book_word,
)
from maxcolor import console, log


def finished(task: str, line: int):
    """Finished task"""
    console.log(
        Panel(
            f"[bold bright_white]Finished {task}[/]",
            title=f"[#00ff00]✔ Finished[/]",
            title_align="left",
            border_style="green",
            subtitle=f"[#096809]tasks/book_tasks.py [/][#FFF]|[/][#00ff00] Line {line}[/]",
            subtitle_align="right",
            width=80,
        )lI'm
_1    )


@log.catch
def book_covers():
    with Progress(console=console) as progress:
        task = progress.add_task("Generating book covers", total=10)
        books = book_gen()
        for book in books:

            generate_book_cover(book)
            progress.update(task, advance=1)
    finished("Generated Book Covers", 46)


@log.catch
def book_cover_paths():
    with Progress(console=console) as progress:
        task = progress.add_task("Generating book cover paths", total=10)
        books = book_gen()
        for book in books:

            generate_book_cover_path(book)
            progress.update(task, advance=1)
    finished("Generated Book Cover Paths", 56)


@log.catch
def book_defaults():
    with Progress(console=console) as progress:
        task = progress.add_task("Generating book defaults", total=10)
        books = book_gen()
        for book in books:

            generate_book_default(book)
            progress.update(task, advance=1)
    finished("Generated Book Defaults", 66)


@log.catch
def book_ends():
    with Progress(console=console) as progress:
        task = progress.add_task("Generating book ends", total=10)
        books = book_gen()
        for book in books:

            generate_book_end(book)
            progress.update(task, advance=1)
    finished("Generated Book Ends", 76)


@log.catch
def book_outputs():
    with Progress(console=console) as progress:
        task = progress.add_task("Generating book outputs", total=10)
        books = book_gen()
        for book in books:

            generate_book_output(book)
            progress.update(task, advance=1)
    finished("Generated Book Outputs", 86)


@log.catch
def book_sections():
    with Progress(console=console) as progress:
        task = progress.add_task("Generating book sections", total=10)
        books = book_gen()
        for book in books:

            generate_book_sections(book)
            progress.update(task, advance=1)
    finished("Generated Book Sections", 96)


@log.catch
def book_starts():
    with Progress(console=console) as progress:
        task = progress.add_task("Generating book starts", total=10)
        books = book_gen()
        for book in books:

            generate_book_start(book)
            progress.update(task, advance=1)
    finished("Generated Book Starts", 106)


@log.catch
def book_titles():
    with Progress(console=console) as progress:
        task = progress.add_task("Generating book titles", total=10)
        books = book_gen()
        for book in books:

            generate_book_title(book)
            progress.update(task, advance=1)
    finished("Generated Book Titles", 115)


@log.catch
def book_uuids():
    with Progress(console=console) as progress:
        task = progress.add_task("Generating book uuids", total=10)
        books = book_gen()
        for book in books:

            generate_book_uuid(book)
            progress.update(task, advance=1)
    finished("Generated Book UUIDs", 125)


@log.catch
def book_words():
    with Progress(console=console) as progress:
        task = progress.add_task("Generating book words", total=10)
        books = book_gen()
        for book in books:

            generate_book_word(book)
            progress.update(task, advance=1)
    finished("Generated Book Words", 135)


def book_tasks():
    """Complete all Book Tasks."""
    book_covers()
    book_cover_paths()
    book_defaults()
    book_ends()
    book_outputs()
    book_sections()
    book_starts()
    book_titles()
    book_uuids()
    book_words()

    finished("Finished Book Tasks", 151)


if __name__ == "__main__":
    book_tasks()
