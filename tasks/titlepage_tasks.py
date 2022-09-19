# tasks/titlepage_tasks.py

from pathlib import Path

from rich import inspect, print
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress
from rich.style import Style
from rich.text import Text
from sh import Command, RunningCommand
from src.atlas import sg
from src.log import BASE, console, log, logpanel
from src.titlepage import (
    Titlepage,
    generate_titlepage_book_word,
    generate_titlepage_filename,
    generate_titlepage_html,
    generate_titlepage_html_path,
    generate_titlepage_md,
    generate_titlepage_md_path
)


def finished(task: str, line: int):
    """Finished task"""
    console.log(
        Panel(
            f"[bold bright_white]Finished {task}[/]",
            title = f"[#00ff00]✔ Finished[/]",
            title_align="left",
            border_style="green",
            subtitle=f"[#096809]tasks/titlepage_tasks.py [/][#FFF]|[/][#00ff00] Line {line}[/]",
            subtitle_align="right",
            width=60
        )
    )


def generate_titlepage_book_word_task():
    """Generate titlepage html"""
    with Progress(console=console) as progress:
        task = progress.add_task("[green]Generating titlepage html", total=10)

        for book in range(1, 10):
            generate_titlepage_book_word(book)
            progress.update(task, advance=1)
    finished("Generated Titlepage Book Words", 46)


def generate_titlepage_filename_task():
    """Generate titlepage filename"""
    with Progress(console=console) as progress:
        task = progress.add_task("[green]Generating titlepage filename", total=10)

        for book in range(1, 10):
            generate_titlepage_filename(book)
            progress.update(task, advance=1)
    finished("Generated Titlepage Filenames", 57)


def generate_titlepage_md_path_task():
    """Generate titlepage md path"""
    with Progress(console=console) as progress:
        task = progress.add_task("[green]Generating titlepage md path", total=10)

        for book in range(1, 10):
            generate_titlepage_md_path(book)
            progress.update(task, advance=1)
    finished("Generated Titlepage MD Paths", 68)


def generate_titlepage_html_path_task():
    """Generate titlepage html path"""
    with Progress(console=console) as progress:
        task = progress.add_task("[green]Generating titlepage html path", total=10)

        for book in range(1, 10):
            generate_titlepage_html_path(book)
            progress.update(task, advance=1)
    finished("Generated Titlepage HTML Paths", 79)


def generate_titlepage_md_task():
    """Generate titlepage md"""
    with Progress(console=console) as progress:
        task = progress.add_task("[green]Generating titlepage md", total=10)

        for book in range(1, 10):
            generate_titlepage_md(book)
            progress.update(task, advance=1)
    finished("Generated Titlepage MDs", 90)


def generate_titlepage_markdown_task():
    """Generate titlepage html"""
    with Progress(console=console) as progress:
        task = progress.add_task("[green]Generating titlepage html", total=10)

        for book in range(1, 10):
            generate_titlepage_html(book)
            progress.update(task, advance=1)
    finished("Generated Titlepage HTMLs", 101)


def generate_titlepage_html_task():
    """Generate titlepage html"""
    with Progress(console=console) as progress:
        task = progress.add_task("[green]Generating titlepage html", total=10)

        for book in range(1, 10):
            generate_titlepage_html(book)
            progress.update(task, advance=1)
    finished("Generated Titlepage HTMLs", 112)


if __name__ == "__main__":
    generate_titlepage_book_word_task()
    generate_titlepage_filename_task()
    generate_titlepage_md_path_task()
    generate_titlepage_html_path_task()
    generate_titlepage_md_task()
    generate_titlepage_html_task()
    generate_titlepage_book_word_task()
