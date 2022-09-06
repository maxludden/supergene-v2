# src/chapter.py

import os
import pathlib
import re
from pathlib import Path
from typing import Callable, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import cpu_count

from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.style import Style
from mongoengine import Document
from mongoengine.fields import (
    EnumField,
    IntField,
    StringField,
    URLField,
    DateTimeField,
    UUIDField,
)
from tqdm.auto import tqdm, trange
from dotenv import load_dotenv
import sh
from sh import touch

console = Console(width=110)

try:
    from log import log
except ModuleNotFoundError:
    from src.log import log
except ImportError:
    from src.log import log


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


def error_panel(msg: str, title: str = "Error") -> Panel:
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
        title=Text(
            title,
            style=Style(
                color="white",
                bgcolor="red",
                bold=True,
            ),
        ),
        title_align="left",
        border_style=Style(
            color="red",
            bgcolor="white",
            bold=True,
        ),
    )
    return error_panel


class Chapter(Document):
    """A class/model representing a chapter in a book."""

    chapter = IntField(required=True, unique=True)
    section = IntField(min_value=1, max_value=17, required=True)
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
    meta = {
        "collection": "chapter",
        "abstract": True,
    }

    @log.catch
    def generate_section(self) -> int | None:
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
        if type(self.chapter) is int:
            chapter = int(self.chapter)
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
    def generate_book(self) -> int | None:
        """
        Generate the book that contains the given chapter.

        Raises:
            `ChapterNotFound`
                ValueError: Invalid Chapter Input.

        Returns:
            `book` (int | None):
                The book that contains the given chapter.
        """
        section = self.generate_section()
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

    def generate_book_dir(self) -> Path | None:
        """
        Generate the book directory.

        Returns:
            `book_dir` (str):
                The book directory.
        """
        if self.book:
            if type(self.book) is int:
                book = int(self.book)
                book_zfill = str(book).zfill(2)
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
                return book_dir
        else:
            book = self.generate_book()
            if type(book) is int:
                book = int(book)
                book_zfill = str(book).zfill(2)
                book_dir = Path.cwd() / "books" / f"book{book_zfill}"
                return book_dir

    @log.catch
    def generate_filename(self) -> str | None:
        """
        Generate the filename for the given chapter.

        Raises:
            `ChapterNotFound`
                ValueError: Chapter {chapter} is invalid.

        Returns:
            `filename` (str | None):
                The filename for the given chapter.
        """
        if self.chapter:
            if self.chapter in range(1, 3463):
                if self.chapter == 3095:
                    msg = f"Chapter {self.chapter} does not exist."
                    panel = error_panel(msg, title="Chapter Not Found")
                    raise ChapterNotFound(msg)
                if self.chapter == 3117:
                    msg = f"Chapter {self.chapter} does not exist."
                    panel = error_panel(msg, title="Chapter Not Found")
                    raise ChapterNotFound(msg)
                chapter_str = str(self.chapter)
                chapter_zfill = chapter_str.zfill(4)
                filename = f"chapter-{chapter_zfill}"
                return filename

    @log.catch
    def generate_md_path(self) -> Path | None:
        """
        Generate the path to the markdown file.

        Returns:
            `md_path` (Path | None):
                The path to the markdown file.
        """
        book_dir = self.generate_book_dir()
        assert type(book_dir) is Path, f"book_dir is not a Path object."

        filename = self.generate_filename()
        if filename:
            md_path = book_dir / "md" / f"{filename}.md"
            if md_path.exists():
                return md_path
            else:
                md_path.mkdir(parents=True, exist_ok=True)
                sh.touch(md_path)


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
