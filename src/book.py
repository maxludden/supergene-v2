# #src/book.py

from os import environ
from pathlib import Path
from re import L
from typing import List, Optional
from uuid import uuid4

import ujson
from dotenv import load_dotenv
from mongoengine import Document
from mongoengine.fields import IntField, ListField, StringField, UUIDField
from num2words import num2words
from rich import print
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress
from rich.style import Style
from rich.text import Text

from src.atlas import max_title, sg
from src.log import BASE, console, log

load_dotenv()


def book_panel(
    book: int,
    key: str = "Key",
    value: str | int | Path | Markdown | List = "Value",
    line: int = 1,
    title: Optional[str] = None,
    get: bool = False,
) -> Panel:
    if title:
        title = title
    else:
        title = f"Titlepage {book}"

    if get:
        get_verb = "Retrieved"
    else:
        get_verb = "Generated"

    if len(key) + len(str(value)) < 25:
        length_of_key = len(key)
        length_of_value = len(str(value))
        missing_char = 15 - length_of_key - length_of_value
        value = f"{value}{' ' * missing_char}"

    panel = Panel(
        f"[#eed4fc]{get_verb} {key}:[/][bold bright_white] {str(value)}[/]",
        title=Text(f"{title}", style=Style(color="#8e47ff", bold=True)),
        title_align="left",
        subtitle=f"[purple]src/book.py[/][#FFFFFF]|[/][#54c6ff]line {line}[/]",
        subtitle_align="right",
        border_style=Style(color="#5f00ff"),
        expand=False,
        width=80,
    )
    return panel


# . ##########################################. #
# .                                           . #
# .                                           . #
# .                                           . #
# .  888                          888         . #
# .  888 88e   e88 88e   e88 88e  888 ee      . #
# .  888 888b d888 888b d888 888b 888 P       . #
# .  888 888P Y888 888P Y888 888P 888 b       . #
# .  888 88"   "88 88"   "88 88"  888 8b      . #
# .                                           . #
# .                                           . #
# .                                           . #
# . ##########################################. #


class Book(Document):
    title = StringField(required=True, max_length=500)
    output = StringField()
    cover = StringField()
    cover_path = StringField()
    uuid = UUIDField(binary=False)
    default = StringField()
    start = IntField(min_value=1)
    end = IntField(max_value=3463)
    book = IntField()
    book_word = StringField(required=True)
    sections = ListField(IntField())

    def __int__(self) -> int:
        return int(self.book)  # type: ignore

    def __str__(self) -> str:
        return self.title


class book_gen:
    """Generator for book numbers."""

    def __init__(self) -> None:
        self.book = 1
        self.max = 10

    def __iter__(self):
        return self

    def __next__(self) -> int:
        return self.next()

    def next(self) -> int:
        if self.book > self.max:
            raise StopIteration
        else:
            self.book += 1
            return self.book - 1


@log.catch
def generate_book_title(book: int, save: bool = True) -> str:
    """
    Generate a book title from the book number.

    Args:
        `book` (int): The book number.

        `save` (bool): Whether to save the title to the database. Defaults to `True`.

    Returns:
        `str`: The book title.
    """
    title = ""
    match book:
        case 1:
            title = "First God's Sanctuary"
        case 2:
            title = "Second God's Sanctuary"
        case 3:
            title = "Third God's Sanctuary"
        case 4:
            title = "Fourth and Fifth Gods' Sanctuary"
        case 5:
            title = "Planet Kate and Narrow Moon"
        case 6:
            title = "Sky Palace, Blade, and Eclipse"
        case 7:
            title = "The Ice Blue Knights and The Extreme Kings"
        case 8:
            title = "They Systems of Chaos and The Very High"
        case 9:
            title = "Meeting God and Fighting Sacred"
        case 10:
            title = "The Universe of Kingdoms and Quin Kiu"
        case _:
            book = generate_book_title(int(input("Please enter a book number between 1 and 10: ")))  # type: ignore

    console.print(book_panel(book, "Title", title, 149))
    return title  # type: ignore


@log.catch
def get_book_title(book: int) -> str:
    """
    Retrieve the title of the given book from MongoDB.

    Args:
        `book` (int): The given book number.

    Returns:
        `title` (str): The title of the given book.
    """
    sg()
    doc = Book.objects(book=book).first()  # type: ignore
    if doc.title:
        title = doc.title

        console.print(book_panel(book, "Title", title, 169, get=True))
        return title  # type: ignore
    else:
        title = generate_book_title(book)
        return title


@log.catch
def generate_book_output(book: int, save: bool = True) -> str:
    """
    Generate the output filename for the given book.

    Args:
        `book` (int): The given book number.

        `save` (bool): Whether to save the output to the database. Defaults to `True`.

    Returns:
        `output` (str): The output filename for the given book.
    """
    sg()
    doc = Book.objects(book=book).first()  # type: ignore
    if doc.title:
        title = doc.title
        output = f"{title}.epub"
        console.print(book_panel(book, "Output", output, 194))
    return output  # type: ignore


@log.catch
def get_book_output(book: int) -> str:
    """
    Retrieve the output filename for the given book from MongoDB.

    Args:
        `book` (int): The given book number.

    Returns:
        `output` (str): The output filename for the given book.
    """
    sg()
    doc = Book.objects(book=book).first()  # type: ignore
    if doc.output:
        output = doc.output

        console.print(book_panel(book, "Output", output, 214, get=True))
        return output  # type: ignore
    else:
        output = generate_book_output(book)
        return output


@log.catch
def generate_book_cover(book: int, save: bool = True) -> str:
    """
    Generate the cover filename for the given book.

    Args:
        `book` (int): The given book number.

        `save` (bool): Whether to save the cover to the database. Defaults to `True`.

        `string` (bool): Whether to return a string or a Path object. Defaults to `False`.

    Returns:
        `cover` (Path | str): The cover filename for the given book.
    """
    cover = f"cover{book}.png"
    console.print(book_panel(book, "Cover", cover, 237))

    return cover


@log.catch
def get_book_cover(book: int) -> str:
    """
    Retrieve the cover filename for the given book from MongoDB.

    Args:
        `book` (int): The given book number.

    Returns:
        `cover` (str): The cover filename for the given book.
    """
    sg()
    doc = Book.objects(book=book).first()  # type: ignore
    if doc.cover:
        cover = doc.cover

        console.print(book_panel(book, "Cover", cover, 259, get=True))
        return cover  # type: ignore
    else:
        cover = generate_book_cover(book)
        return cover


@log.catch
def generate_book_cover_path(
    book: int, save: bool = True, string: bool = False
) -> Path | str:
    """
    Generate the cover path for the given book.

    Args:
        `book` (int): The given book number.

        `save` (bool): Whether to save the cover path to the database. Defaults to `True`.

        `string` (bool): Whether to return a string or a Path object. Defaults to `False`.

    Returns:
        `cover_path` (Path | str): The cover path for the given book.
    """
    book_zfill = str(book).zfill(2)
    book_dir = f"book(book_zfill)"
    cover = generate_book_cover(book)
    cover_path = f"{BASE}/books/{book_dir}/Images/{cover}"

    if save:
        sg()
        doc = Book.objects(book=book).first()  # type: ignore
        doc.cover_path = cover_path
        doc.save()

    if string:
        return cover_path

    console.print(book_panel(book, "Cover Path", cover_path, 287))

    return Path(cover_path)


@log.catch
def get_book_cover_path(book: int, string: bool = False) -> Path | str:
    """
    Retrieve the cover path for the given book from MongoDB.

    Args:
        `book` (int): The given book number.

        `string` (bool): Whether to return a string. Defaults to `False`.

    Returns:
        `cover_path` (Path): The cover path for the given book.
    """
    sg()
    doc = Book.objects(book=book).first()  # type: ignore
    if doc.cover_path:
        cover_path = doc.cover_path

        console.print(book_panel(book, "Cover Path", cover_path, 309, get=True))
        return Path(cover_path)  # type: ignore
    else:
        cover_path = generate_book_cover_path(book)
        return cover_path


@log.catch
def generate_book_uuid(book: int) -> str:
    """
    Generate the UUID for the given book if it does not exist. Else retrieve it from MongoDB.

    Args:
        `book` (int): The given book number.

    Returns:
        `UUID` (str): The UUID for the given book.
    """
    sg()
    doc = Book.objects(book=book).first()  # type: ignore
    if doc.uuid:
        uuid = doc.uuid
    else:
        uuid = str(uuid4())
        doc.uuid = uuid
        doc.save()

    console.print(book_panel(book, "UUID", uuid, 347))
    return uuid


@log.catch
def get_book_uuid(book: int) -> str:
    """
    Retrieve the UUID for the given book from MongoDB.

    Args:
        `book` (int): The given book number.

    Returns:
        `UUID` (str): The UUID for the given book.
    """
    sg()
    doc = Book.objects(book=book).first()  # type: ignore
    if doc.uuid:
        uuid = doc.uuid

        console.print(book_panel(book, "UUID", uuid, 369, get=True))
        return uuid
    else:
        uuid = generate_book_uuid(book)
        return uuid


@log.catch
def generate_book_default(
    book: int, save: bool = True, string: bool = False
) -> Path | str:
    """
    Generate the path for the pandoc default doc of the given book.

    Args:
        `book` (int): The given book number.

        `save` (bool): Whether to save the default path to the database. Defaults to `True`.

        `string` (bool): Whether to return the path as a string. Defaults to `False`.

    Returns:
        `default` (Path | str): The default path for the given book.
    """
    book_zfill = str(book).zfill(2)
    book_dir = f"book(book_zfill)"
    default = f"{BASE}/books/{book_dir}/default.html"

    if save:
        sg()
        doc = Book.objects(book=book).first()  # type: ignore
        doc.default = default
        doc.save()

    if string:
        return default

    console.print(book_panel(book, "Default", default, 405))

    return Path(default)


@log.catch
def get_book_default(book: int, string: bool = False) -> Path | str:
    """
    Retrieve the default path for the given book from MongoDB.

    Args:
        `book` (int): The given book number.

        `string` (bool): Whether to return the path as a string. Defaults to `False`.

    Returns:
        `default` (Path): The default path for the given book.
    """
    sg()
    doc = Book.objects(book=book).first()  # type: ignore
    if doc.default:
        default = doc.default

        console.print(book_panel(book, "Default", default, 429, get=True))
        return Path(default)
    else:
        default = generate_book_default(book)
        return default


@log.catch
def generate_book_start(book: int, save: bool = True) -> int:
    """
    Generate the starting chapter of the given book.

    Args:
        `book` (int): The given book number.

        `save` (bool): Whether to save the starting chapter to the database. Defaults to `True`.

    Returns:
        `start` (int): The starting chapter of the given book.
    """
    match book:
        case 1:
            start = 1
        case 2:
            start = 425
        case 3:
            start = 883
        case 4:
            start = 1339
        case 5:
            start = 1712
        case 6:
            start = 1961
        case 7:
            start = 2205
        case 8:
            start = 2444
        case 9:
            start = 2766
        case 10:
            start = 3034
        case _:
            start = generate_book_start(
                int(
                    input(
                        "That is not a valid book number. Please enter a valid book number: "
                    )
                )
            )

    console.print(book_panel(book, "Start", start, 473))
    if save:
        sg()
        doc = Book.objects(book=book).first()  # type: ignore
        doc.start = start
        doc.save()

    return start


@log.catch
def get_book_start(book: int) -> int:
    """
    Retrieve the starting chapter of the given book from MongoDB.

    Args:
        `book` (int): The given book number.

    Returns:
        `start` (int): The starting chapter of the given book.
    """
    sg()
    doc = Book.objects(book=book).first()  # type: ignore
    if doc.start:
        start = doc.start

        console.print(book_panel(book, "Start", start, 495, get=True))
        return start
    else:
        start = generate_book_start(book)
        return start


@log.catch
def generate_book_end(book: int, save: bool = True) -> int:
    """
    Generate the finishing chapter of the given book.

    Args:
        `book` (int): The given book.

        `save` (bool, optional): Wether to save the finishing chapter to MongoDB. Defaults to True.

    Returns:
        `end` (int): The finishing chapter of the given book.
    """
    match book:
        case 1:
            end = 424
        case 2:
            end = 882
        case 3:
            end = 1338
        case 4:
            end = 1711
        case 5:
            end = 1960
        case 6:
            end = 2204
        case 7:
            end = 2443
        case 8:
            end = 2765
        case 9:
            end = 3033
        case 10:
            end = 3462
        case _:
            end = generate_book_end(
                int(
                    input(
                        "That is not a valid book number. Please enter a valid book number: "
                    )
                )
            )

    console.print(book_panel(book, "End", end, 547))
    if save:
        sg()
        doc = Book.objects(book=book).first()  # type: ignore
        doc.end = end
        doc.save()

    return end


@log.catch
def get_book_end(book: int) -> int:
    """
    Retrieve the finishing chapter of the given book from MongoDB.

    Args:
        `book` (int): The given book number.

    Returns:
        `end` (int): The finishing chapter of the given book.
    """
    sg()
    doc = Book.objects(book=book).first()  # type: ignore
    if doc.end:
        end = doc.end

        console.print(book_panel(book, "End", end, 574, get=True))
        return end

    else:
        end = generate_book_end(book)
        return end


@log.catch
def generate_book_word(book: int, save: bool = True) -> str:
    """
    Generate the word for the given book.

    Args:
        `book` (int): The given book number.

        `save` (bool): Whether to save the word to the database. Defaults to `True`.

    Returns:
        `word` (str): The word for the given book.
    """
    book_word = str(num2words(book)).capitalize()

    if save:
        sg()
        doc = Book.objects(book=book).first()  # type: ignore
        doc.book_word = book_word
        doc.save()

    console.print(book_panel(book, "Book Word", book_word, 603))
    return book_word


@log.catch
def generate_book_sections(book: int, save: bool = True) -> List[int]:
    """
    Generate the sections of the given book.

    Args:
        `book` (int): The given book.

        `save` (bool, optional): Whether to save the given book's sections to MongoDB. Defaults to `True`.

    Returns:
        `sections` (List[int]): The sections of the given book.
    """
    match book:
        case 1:
            sections = [1]
        case 2:
            sections = [2]
        case 3:
            sections = [3]
        case 4:
            sections = [4, 5]
        case 5:
            sections = [6, 7]
        case 6:
            sections = [8, 9]
        case 7:
            sections = [10, 11]
        case 8:
            sections = [12, 13]
        case 9:
            sections = [14, 15]
        case 10:
            sections = [16, 17]
        case _:
            sections = generate_book_sections(
                int(
                    input(
                        "That is not a valid book number. Please enter a valid book number: "
                    )
                )
            )

    console.print(book_panel(book, "Sections", sections, 645))

    if save:
        sg()
        doc = Book.objects(book=book).first()  # type: ignore
        doc.sections = sections
        doc.save()

    return sections


@log.catch
def get_book_sections(book: int) -> List[int]:
    """
    Retrieve the sections of the given book from MongoDB.

    Args:
        `book` (int): The given book number.

    Returns:
        `sections` (List[int]): The sections of the given book.
    """
    sg()
    doc = Book.objects(book=book).first()  # type: ignore
    if doc.sections:
        sections = doc.sections

        console.print(book_panel(book, "Sections", sections, 673, get=True))
        return sections
    else:
        sections = generate_book_sections(book)
        return sections


books = book_gen()
for book in books:
    console.print(book_panel(book, "Book", book, 706), width=60)
