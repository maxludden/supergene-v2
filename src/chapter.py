# src/chapter.py

import os
import pathlib
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import cpu_count
from pathlib import Path
from __future__ import annotations

import sh
from dotenv import load_dotenv
from mongoengine import Document
from mongoengine.fields import IntField, StringField, URLField
from mongoengine.errors import DoesNotExist, NotUniqueError, ValidationError
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.style import Style
from rich.text import Text
from sh import Command
from tqdm.auto import tqdm, trange
from ujson import dump, load
from pydantic import BaseModel, HttpUrl

# > Get Log -------------------------------------------
try:
    from log import log
except ModuleNotFoundError:
    from src.log import log
except ImportError:
    from src.log import log

# > Get Super Gene & BASE -----------------------------
try:
    from atlas import BASE, sg
except ModuleNotFoundError:
    from src.atlas import BASE, sg
except ImportError:
    from src.atlas import BASE, sg

touch = Command("touch")
console = Console(width=110)
load_dotenv()


# > Custom Exceptions-----------------------------------
class ChapterNotFound(ValueError):
    """
    Custom ValueError for when a chapter is not found.

    Args:
        `ValueError` (Exception):
            Custom ValueError for when a chapter is not found.
    """
    pass

class SectionNotFound(ValueError):
    """
    Custom ValueError for when a section is not found.

    Args:
        `ValueError` (Exception):
            Custom ValueError for when a section is not found.
    """
    pass

class BookNotFound(DoesNotExist):
    """
    Custom MongoDB Exception for when a book is not found.

    Args:
        `DoesNotExist`` (MongoEngineException):
            Custom Exception for when a book is not found.
    """
    pass


# > Error Panel ----------------------------------------
def error_panel(msg: str, title: str="Error") -> Panel:
    """
    Create a panel for errors.

    Args:
        `msg` (str):
            The message to display in the panel.
        `title` (str):
            The title of the panel.
    """
    error_panel = Panel(
        Text(msg, style="bold red on white"),
        title = Text(
            title,
            style=Style(
                color="white",
                bgcolor="red",
                bold=True,
            ),
        ),
        title_align="left",
        style=Style(
            color="red",
            bgcolor="white",
            bold=True,
        ),
    )
    return error_panel


# > Chapter Model -------------------------------------
class Chapter(Document):
    """
    A MongoDB Document class to store chapter data.

    Args:
        `Document` (MongoEngine.Document):
            Subclassed from MongoENgine.Document.
    """

    chapter = IntField(min_value=1, max_value=3462, required=True, unique=True)
    section = IntField(min_value=1, max_value=17)
    book = IntField(min_value=1, max_value=10, required=True)
    title = StringField(max_length=500)
    text = StringField()
    filename = StringField()
    md_path = StringField()
    html_path = StringField()
    md = StringField()
    html = StringField()
    url = URLField()
    unparsed_text = StringField()
    parsed_text = StringField()


@log.catch
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
    if type(chapter) is int:
        chapter = int(chapter)
        log.debug(f"Called generate_section(chapter={chapter})")
        if chapter <= 424:
            return 1
        elif chapter <= 882:
            return 2
        elif chapter <= 1338:
            return 3
        elif chapter <= 1679:
            return 4
        elif chapter <= 1711:
            return 5
        elif chapter <= 1821:
            return 6
        elif chapter <= 1960:
            return 7
        elif chapter <= 2165:
            return 8
        elif chapter <= 2204:
            return 9
        elif chapter <= 2299:
            return 10
        elif chapter <= 2443:
            return 11
        elif chapter <= 2639:
            return 12
        elif chapter <= 2765:
            return 13
        elif chapter <= 2891:
            return 14
        elif chapter <= 3033:
            # Skip non-existent chapter 3095
            if chapter == 3095:
                log.warning(
                    f"Chapter {chapter} was inputted to generate_section().\nChapter {chapter} does not exist."
                )
                pass
            # Skip non-existent chapter 3117
            elif chapter == 3117:
                log.warning(
                    f"Chapter {chapter} was inputted to generate_section(). \nChapter {chapter} does not exist."
                )
                pass
            else:
                return 15
        elif chapter <= 3303:
            return 16
        elif chapter <= 3462:
            return 17
        else:
            msg = f"Chapter {chapter} does not exist."
            panel = error_panel(msg, title="Chapter Not Found")
            console.clear()
            console.print(panel)
            raise ChapterNotFound(msg)


@log.catch
def generate_book(chapter: int) -> int | None:
    """
    Generate the book that contains the given chapter.

    Raises:
        `ChapterNotFound`
            ValueError: Invalid Chapter Input.

    Returns:
        `book` (int | None):
            The book that contains the given chapter.
    """
    section = generate_section(chapter)
    if section is not None:
        if type(section) is int:
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
                    msg = f"Section {section} was not found."
                    panel = error_panel(msg, title="Section Not Found")
                    console.clear()
                    console.print(panel)
                    raise SectionNotFound(msg)
        else:
            msg = f"Section {section} is not an integer."
            panel = error_panel(msg, title="Invalid Section Type")
            console.clear()
            console.print(panel)
            raise SectionNotFound(msg)
    else:
        msg = f"Section {section} is None."
        panel = error_panel(msg, title="Section has no value.")
        console.clear()
        console.print(panel)
        raise SectionNotFound(msg)


def generate_book_dir(chapter: int) -> Path | None:
    """
    Generate the book directory.

    Returns:
        `book_dir` (str):
            The book directory.
    """
    book = generate_book(chapter)
    if book:
        if type(book) is int:
            book = int(book)
            book_zfill = str(book).zfill(2)  # example "02"
            book_dir = Path.cwd() / "books" / f"book{book_zfill}"
            book_dir_panel = Panel(
                Text(f"{book_dir}", style="bold white on blue"),
                title=Text(
                    "Book Directory",
                    style=Style(color="blue", bgcolor="white", bold=True),
                ),
                title_align="left",
                border_style=Style(color="blue", bgcolor="white", bold=True),
            )
            print(book_dir_panel)
            return book_dir
    else:
        msg = f"Book {book} is not an integer."
        panel = error_panel(msg, title="Invalid Book.")
        console.clear()
        console.print(panel)
        raise BookNotFound(msg)


@log.catch
def generate_filename(chapter: int) -> str | None:
    """
    Generate the filename for the given chapter.

    Raises:
        `ChapterNotFound`
            ValueError: Chapter {chapter} is invalid.

    Returns:
        `filename` (str | None):
            The filename for the given chapter.
    """
    # > Validate chapter
    if chapter in range(1, 3463):
        # > Skip non-existent chapter 3095
        if chapter == 3095:
            msg = f"Chapter {chapter} does not exist."
            panel = error_panel(msg, title="Chapter Not Found")
            raise ChapterNotFound(msg)
        # > Skip non-existent chapter 3117
        if chapter == 3117:
            msg = f"Chapter {chapter} does not exist."
            panel = error_panel(msg, title="Chapter Not Found")
            raise ChapterNotFound(msg)
        chapter_str = str(chapter)
        chapter_zfill = chapter_str.zfill(4)
        filename = f"chapter-{chapter_zfill}"
        return filename


@log.catch
def generate_md_path(chapter: int) -> Path | None:
    """
    Generate the path to the markdown file.

    Returns:
        `md_path` (Path | None):
            The path to the markdown file.
    """
    book_dir = generate_book_dir(chapter)
    assert type(book_dir) is Path, f"book_dir is not a Path object."

    filename = generate_filename(chapter)
    if filename:
        md_path = book_dir / "md" / f"{filename}.md"
        if md_path.exists():
            return md_path
        else:
            md_path.mkdir(parents=True, exist_ok=True)
            touch(md_path)
            return md_path


@log.catch
def generate_html_path(chapter: int) -> Path | None:
    """
    Generate the path to the HTML file.

    Returns:
        `html_path` (Path | None):
            The path to the HTML file.
    """
    console.clear()

    book_dir = generate_book_dir(chapter)
    assert type(book_dir) is Path, f"book_dir is not a Path object."

    filename = generate_filename(chapter)
    if filename:
        html_path = book_dir / "html" / f"{filename}.html"
        if html_path.exists():
            return html_path
        else:
            html_path.mkdir(parents=True, exist_ok=True)
            touch(html_path)
            return html_path


def url_from_db(chapter: int) -> str | None:
    '''
    Retrieve the given chapter's URL from the Database.

    Args:
        `chapter` (int):
            The given chapter.


    Returns:
        `` (str | None):
            _description_
    '''
def get_url(chapter: int, from_db=True) -> str | None:
    """
    Get the URL for the given chapter.

    Returns:
        `url` (str | None):
            The URL for the given chapter.
    """
    if from_db:
        try:
            sg()
            url = Chapter.objects(chapter=chapter).first().url # type: ignore
            if url:
                return url
        except




    sg()
    if from_db:
        chapter_doc = Chapter.objects(chapter=chapter).first()  # type: ignore
        url = chapter_doc.url
        if url:
            return url
        elif not url:
            msg = f"URL for chapter {chapter} not found in database."
            panel = error_panel(msg, title="URL not in MongoDB")
            console.print(panel)

        else:
            with open("json/toc.json", "r") as infile:
                url = dict(load(infile))[str(chapter)]["url"]
                if url:
                    return url
                elif not url:
                    msg = f"URL for chapter {chapter} not found in TOC.json."
                    panel = error_panel(msg, title="URL Not Found")
                    console.print(panel)
                else:
                    # > Generate URL
                    url = (
                        f"https://bestlightnovel.com/novel_888112448/chapter_{chapter}"
                    )

                    return url


class chapter_gen:
    """
    Generator for chapter_numbers.
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
