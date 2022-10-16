from concurrent.futures import (ProcessPoolExecutor, ThreadPoolExecutor,
                                as_completed)
from multiprocessing import cpu_count
from pathlib import Path
from time import perf_counter
import os

from pymongo.errors import ConnectionFailure
from mongoengine import Document, connect
from mongoengine.fields import IntField, ListField, StringField, URLField
from rich import print
from rich.box import ROUNDED
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress
from rich.text import Text
from rich.style import Style
from sh import Command



console = Console()

def generate_section(chapter: int) -> int | None:
    """
    Determines the given chapter's section.

    Args:
        `chapter` (int):
            The given chapter.

    Raises:
        `ValueError`: Invalid Chapter Number

    Returns:
        `section` (int):
            The section that the given chapter belongs to.
    """
    chapter = int(chapter)
    if chapter <= 424:  # book1
        return 1
    elif chapter <= 882:  # book2
        return 2
    elif chapter <= 1338:  # book3
        return 3
    elif chapter <= 1679:  # book4
        return 4
    elif chapter <= 1711:  # book4
        return 5
    elif chapter <= 1821:  # book5
        return 6
    elif chapter <= 1960:  # book5
        return 7
    elif chapter <= 2165:  # book6
        return 8
    elif chapter <= 2204:  # book6
        return 9
    elif chapter <= 2299:  # book7
        return 10
    elif chapter <= 2443:  # book7
        return 11
    elif chapter <= 2639:  # book8
        return 12
    elif chapter <= 2765:  # book8
        return 13
    elif chapter <= 2891:  # book9
        return 14
    elif chapter <= 3033:  # book9
        if chapter == 3095:
            pass
        elif chapter == 3117:
            pass
        else:
            return 15
    elif chapter <= 3303:  # book10
        return 16
    elif chapter <= 3462:  # book10
        return 17
    else:
        raise ValueError("Invalid Chapter", f"\nChapter: {chapter}")

def generate_book(chapter: int) -> int | None:
    """
    Generate the book for a given chapter.

    Args:
        `chapter` (int):
            The given chapter.

    Raises:
        `ValueError`: Invalid Section Number

    Returns:
        `book` (int):
            The book of the given chapter
    """
    section = generate_section(chapter)
    match section:
        case 1:
            return 1
        case 2:
            return 2
        case 3:
            return 3
        case 4 | 5:
            return 4
        case 6 | 7:
            return 5
        case 8 | 9:
            return 6
        case 10 | 11:
            return 7
        case 12 | 13:
            return 8
        case 14 | 15:
            return 9
        case 16 | 17:
            return 10
        case _:
            raise ValueError("Invalid Section", f"\nSection: {section}")

def generate_db_uri(database: str) -> str:
    """Generate the connection URI for the given database."""
    db_lower = database.lower()
    match db_lower:
        case "localdb":
            return "mongodb://localhost:27017/SUPERGENE"
        case "supergene":
            return str(os.environ.get("SUPERGENE"))
        case "make_supergene":
            return str(os.environ.get("MAKE_SUPERGENE"))
        case _:
            return "mongodb://localhost:27017/supergene"

def sg(db: str = "LOCALDB"):
    """
    Connect to the given MongoDB.

    Args:
        `db` (str, optional): The database to which you like to connect. Defaults to "LOCALDB".
    """
    mongoengine.disconnect()  # type: ignore

    # > URI
    uri = generate_db_uri(db)

    # > Connect
    try:
        connect(db="SUPERGENE", host=uri)
        # success_panel = Panel(
        #     Text(f"Connected to MongoDB:{db}", style="bold white"),
        #     title=Text("MongoDB", style="bold white"),
        #     title_align="left",
        #     style=Style(color="green"),
        # )
        # console.print(success_panel)
    except ConnectionFailure as cf:
        error_panel = Panel(
            Text(f"Connection to MongoDB:{db} failed", style="bold red on white"),
            title=Text("MongoDB", style="bold red on white"),
            title_align="left",
            style=Style(color="bold white on black"),
        )
        console.print(error_panel)
        console.print(cf)

class Chapter(Document):
    chapter = IntField(required=True, unique=True)
    section = IntField()
    book = IntField(min_value=1, max_value=10, required=True)
    title = StringField(max_length=500, required=True)
    text = StringField()
    filename = StringField()
    md_path = StringField()
    html_path = StringField()
    text_path = StringField()
    md = StringField()
    html = StringField()
    url = URLField()
    unparsed_text = StringField()
    parsed_text = StringField()
    tags = ListField(StringField(max_length=50))

    def __rich_repr__(self):
        table = Table(
            title=Text(f"Chapter {self.chapter}", style="bold cyan"),
            show_header=True,
            header_style="bold magenta",
            box=ROUNDED,
        )

        table.add_column("Key", style="dim", width=12)
        table.add_column("Value", style="dim")
        table.add_row("Chapter", f"{self.chapter}")
        table.add_row("Section", f"{self.section}")
        table.add_row("Book", f"{self.book}")
        table.add_row("Title", f"{self.title}")
        table.add_row("Filename", f"{self.filename}")
        table.add_row("MD Path", f"{self.md_path}")
        table.add_row("HTML Path", f"{self.html_path}")

        repr_md = Markdown(str(self.md))

        console.print(table)
        console.print(repr_md)

    def __int__(self):
        return self.chapter

    def __str__(self):
        return self.text


class chapter_gen:
    """
    Generator for chapter numbers.
    """

    def __init__(self, start: int = 1, end: int = 3462):
        self.start = start
        self.end = end
        self.chapter_number = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.chapter_number >= 3462:
            raise StopIteration
        elif self.chapter_number == 3094:
            # Skipping chapter 3095
            # 3094 + 1 + 1 = 3096
            self.chapter_number += 2
            return self.chapter_number
        elif self.chapter_number == 3116:
            # Skipping chapter 3117
            # 3116 + 1 + 1 = 3118
            self.chapter_number += 2
            return self.chapter_number
        else:
            self.chapter_number += 1
            return self.chapter_number

    def __len__(self):
        return self.end - self.start + 1

class HTMLGenerationError(Exception):
    pass


class ChapterNotFound(Exception):
    pass


class HtmlProgress(Progress):
    def get_renderables(self):
        yield Panel(self.make_tasks_table(self.tasks))


chapters = chapter_gen()


def generate_filename(chapter: int) -> str:
    return f"chapter-{str(chapter).zfill(4)}"


def generate_md_path(chapter: int) -> Path:
    BASE = Path.cwd()
    book = generate_book(chapter)
    book_zfill = str(book).zfill(2)
    book_dir = f"book{book_zfill}"
    filename = generate_filename(chapter)
    return BASE / "books" / book_dir / "md" / f"{filename}.md"


def generate_html_path(chapter: int) -> Path:
    BASE = Path.cwd()
    book = generate_book(chapter)
    book_zfill = str(book).zfill(2)
    book_dir = f"book{book_zfill}"
    filename = generate_filename(chapter)
    return BASE / "books" / book_dir / "html" / f"{filename}.html"


def generate_html(chapter: int, save: bool = True):
    start = perf_counter()
    sg()
    doc = Chapter.objects(chapter=chapter).first()  # type: ignore
    if doc:
        html_path = generate_html_path(doc.chapter)
        md_path = generate_md_path(doc.chapter)

        if md_path.exists():
            multimarkdown = Command("multimarkdown")
            mmd = multimarkdown.bake(
                "-f",
                "--nolabels",
                "-o",
            )
            result = mmd(html_path, md_path)
            if result.exit_code == 0:  # type: ignore

                if save:
                    sg()
                    doc = Chapter.objects(chapter=chapter).first()  # type: ignore
                    with open(html_path, "r") as infile:
                        doc.html = infile.read()

            else:
                raise HTMLGenerationError(
                    f"Error generating HTML for doc {doc.chapter}."
                )

        else:
            raise ChapterNotFound(f"Markdown file not found for doc {doc.chapter}.")
    else:

        raise ChapterNotFound(f"Chapter {doc.chapter} not found.")
    end = perf_counter()
    duration = end - start

    return duration


if __name__ == "__main__":
    start = perf_counter()
    durations = []
    with Progress(console=console) as progress:
        task = progress.add_task("Generating HTML...", total=3462)
        with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
            futures = [executor.submit(generate_html, chapter) for chapter in chapters]
            for future in as_completed(futures):
                progress.advance(task)
    end = perf_counter()
    total_duration = end - start
    sum = sum(durations)
    avg = sum / 3462
    msg = f"Generated HTML for all chapters in {end - start:0.4f} seconds. Average time per chapter: {avg:0.6f} seconds."
    console.print(
        Panel(
            Text(msg, justify="left", style="white"),
            title=Text(f"Generated Chapter HTML", style="bold green"),
            title_align="left",
            expand=False,
            border_style="#00ff00",
        )
    )
