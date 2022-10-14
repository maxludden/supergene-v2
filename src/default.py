# src/default.py

from pathlib import Path
from typing import List, Optional, Any
from sh import Command, RunningCommand
from inspect import currentframe, getframeinfo
from time import sleep

from dotenv import load_dotenv
from mongoengine import Document
from mongoengine.fields import IntField, ListField, StringField
from num2words import num2words
from rich import print
from rich.text import Text
from rich.panel import Panel
from rich.style import Style
from rich.markdown import Markdown
from rich.progress import Progress
from rich.traceback import install

import src.book as bk
import src.chapter as ch
import src.endofbook as eob
import src.epubmetadata as epubmeta
import src.metadata as meta
import src.myaml as myaml
import src.section as sec
import src.titlepage as tp
import src.cover as cv
from src.atlas import max_title, sg
from src.log import BASE, console, log, logpanel

load_dotenv()
install()


class InvalidBookError(Exception):
    pass


# _. ───────────────── Default ──────────────────────────────────
class Default(Document):
    book = IntField(unique=True, min_value=1, max_value=10)
    book_word = StringField()
    content = StringField()
    cover = StringField()  # Cover image's filename
    cover_path = StringField()  # Cover image's path
    epubmetadata = StringField()
    filename = StringField()
    filepath = StringField()
    input_files = ListField(StringField())
    metadata = StringField()
    output = StringField()
    resource_paths = ListField(StringField())
    section1_chapters = ListField(IntField())
    section2_chapters = ListField(IntField())
    section1_filenames = ListField(StringField())
    section2_filenames = ListField(StringField())
    section1_filepaths = ListField(StringField())
    section2_filepaths = ListField(StringField())
    section_count = IntField(min_value=1, max_value=2)
    sections = ListField(IntField(min_value=1, max_value=17))

    # default_doc = StringField()
    # title = StringField()
    meta = {"collection": "default"}


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
        subtitle=f"[purple]src/default.py[/][#FFFFFF]|[/][#54c6ff]line {line}[/]",
        subtitle_align="right",
        border_style=Style(color="#5f00ff"),
        expand=True,
        width=80,
    )
    return panel


def get_linenumber() -> int:
    """
    Get the current line number.

    Returns:
        `line` (int): The current line number.
    """
    cf = currentframe()
    return cf.f_back.f_lineno  # type: ignore


def next_lineno() -> int:
    """
    Get the next line number.

    Returns:
        `line` (int): The next line number.
    """
    cf = currentframe()
    next_lineno = int(cf.f_back.f_lineno) + 1  # type: ignore
    return next_lineno


def generate_default_book(section: int, save: bool = False) -> int | None:
    """
    Generate the book of the given section.

    Args:
        `section` (int): The given section.

        `save` (bool, optional): Whether to save the given section's book to MongoDB. Defaults to True.

    Raises:
        'ValueError': If the given section is not between 1 and 17.

    Returns:
        `book` (int): The given section's book.
    """
    match int(section):
        case 1:
            book = 1
        case 2:
            book = 2
        case 3:
            book = 3
        case 4 | 5:
            book = 4
        case 6 | 7:
            book = 5
        case 8 | 9:
            book = 6
        case 10 | 11:
            book = 7
        case 12 | 13:
            book = 8
        case 14 | 15:
            book = 9
        case 16 | 17:
            book = 10
        case _:
            raise ValueError("Invalid Section Input.", f"Section: {section}")

    if save:
        sg()
        doc = Default.objects(book=book).first()  # type: ignore
        doc.book = book
        doc.save()
        # log.debug(f"Saved Book {book} for Section {section}.")

    line = next_lineno()
    console.print(default_panel(book, "Book from Section", book, line), highlight=True)

    return book


def get_default_book(section: int) -> int:
    """
    Retrieve the book of the given section from MongoDB.

    Args:
        `section` (int): The given section.

    Returns:
        `book` (int): The book of the given section.
    """
    sg()
    doc = Default.objects(section=section).first()  # type: ignore
    if doc.book:
        console.print(default_panel(section, "Book", doc.book, 158), highlight=True)
        return doc.book

    else:
        return generate_default_book(section)  # type: ignore


def generate_default_book_word(book: int, save: bool = True) -> str | None:  # type: ignore
    """
    Generates the book word of the given book.

    Args:
        `book` (int): The given book.

    Returns:
        `book_word` (str): The book word of the given book.
    """
    book_word = num2words(book, lang="en")
    if save:
        sg()
        doc = Default.objects(book=book).first()  # type: ignore
        doc.book_word = book_word
        doc.save()
        # log.debug(f"Saved Book Word {book_word} for Book {book}.")

    frameinfo = getframeinfo(currentframe())  # type: ignore
    next_lineno = int(frameinfo.lineno) + 2
    console.print(
        default_panel(book, "Book Word", book_word, next_lineno), highlight=True
    )
    return book_word


def get_default_book_word(book: int) -> str:  # type: ignore
    """
    Retrieve the book word of the given book from MongoDB.

    Args:
        `book` (int): The given book.

    Returns:
        `book_word` (str): The book word of the given book.
    """
    sg()
    doc = Default.objects(book=book).first()  # type: ignore
    if doc.book_word:
        frameinfo = getframeinfo(currentframe())  # type: ignore
        next_lineno = int(frameinfo.lineno) + 2
        console.print(
            default_panel(book, "Book Word", doc.book_word, next_lineno), highlight=True
        )
        return doc.book_word

    else:
        return generate_default_book_word(book)  # type: ignore


def generate_default_output(book: int, save: bool = True) -> str | None:  # type: ignore
    """
    Generate the output filename of the given book's default file.

    Args:
        `book` (int): The given book.

        `save` (bool, optional): Whether to save the given book's output path to MongoDB. Defaults to True.

    Returns:
        `output` (str): The output path of the given book.
    """
    sg()
    doc = bk.Book.objects(book=book).first()  # type: ignore
    title = doc.title

    output = f"{book} - {title}.epub"
    if save:
        sg()
        doc = Default.objects(book=book).first()  # type: ignore
        doc.output = output
        doc.save()
        # log.debug(f"Saved Output {output} for Book {book}.")

    frameinfo = getframeinfo(currentframe())  # type: ignore
    next_lineno = int(frameinfo.lineno) + 2
    console.print(default_panel(book, "Output", output, next_lineno), highlight=True)
    return output


def get_default_output(book: int) -> str | None:  # type: ignore
    """
    Retrieve the output filename of the given book's default file.

    Args:
        `book` (int): The given book.

    Returns:
        `output` (str): The output filename of the given book's default file.
    """
    sg()
    doc = Default.objects(book=book).first()  # type: ignore
    if doc.output:
        console.print(default_panel(book, "Output", doc.output, 251), highlight=True)
        return doc.output

    else:
        return generate_default_output(book)  # type: ignore


def generate_default_filename(book: int, save: bool = True) -> str:
    """
    Generates the filename of the given book's default file.

    Args:
        `book` (int): The given book.

    Returns:
        `filename` (str): The filename of the given book's default file. Defaults to `True`.
    """
    filename = f"sg{book}.yml"
    if save:
        sg()
        doc = Default.objects(book=book).first()  # type: ignore
        doc.filename = filename
        doc.save()
    # log.debug(f"Generated Book {book}filename for book {book}: {filename}")

    console.print(default_panel(book, "Filename", filename, 111), highlight=True)
    return filename


def get_default_filename(book: int) -> str:
    """
    Retrieves the filename of the given book's default file.

    Args:
        `book` (int): The given book.

    Returns:
        `filename` (str): The filename of the given book's default file.
    """
    sg()
    doc = Default.objects(book=book).first()  # type: ignore
    if doc.filename:
        filename = doc.filename
        # log.debug(f"Retrieved Book {book}'s Default File's Filename: {filename}")
        console.print(default_panel(book, "Filename", filename, 239), highlight=True)
        return filename

    else:
        filename = generate_default_filename(book)
        return filename


def generate_default_cover_filename(book: int) -> str:
    """
    Generates the cover filename of the given book.

    Args:
        `book` (int): The given book.

    Returns:
        `cover` (str): The cover filename of the given book.
    """
    cover = f"cover{book}.jpg"
    # log.debug(f"Generated Book {book}'s Cover: {cover}")
    console.print(default_panel(book, "Cover", cover, 273), highlight=True)
    return cover  # type: ignore


def generate_default_filepath(
    book: int, save: bool = True, string: bool = False
) -> Path | str:
    """
    Generates the filepath of the given book's default file.

    Args:
        `book` (int): The given book.

        `save` (bool, optional): Whether to save the filepath to MongoDB. Defaults to False.

        `string` (bool, optional): Whether to return the filepath as a string. Defaults to `False`.

    Returns:
        `filepath` (Path | str): The filepath of the given book's default file.
    """
    book_zfill = str(book).zfill(2)
    book_dir = f"book{book_zfill}"
    filename = generate_default_filename(book, save=False)
    filepath = f"{BASE}/books/{book_dir}/{filename}.yml"
    # log.debug(f"Generated filepath:\n<code>{filepath}</code>")
    if save:
        sg()
        doc = Default.objects(book=book).first()  # type: ignore
        doc.filepath = filepath
        doc.save()
        # log.debug(f"Saved Book {book}'s Default File's Filepath.")
    if string:
        return filepath

    console.print(default_panel(book, "Filepath", filepath, 145), highlight=True)
    return Path(filepath)


def get_default_filepath(book: int, string: bool = False) -> Path | str:
    """
    Retrieves the filepath of the given book's default file.

    Args:
        `book` (int): The given book.

        `string` (bool, optional): Whether to return the filepath as a string. Defaults to `False`.

    Returns:
        `filepath` (Path | str): The filepath of the given book's default file.
    """
    sg()
    doc = Default.objects(book=book).first()  # type: ignore
    if doc.filepath:
        filepath = doc.filepath
        # log.debug(f"Retrieved Book {book}'s Default File's Filepath: {filepath}")
        console.print(default_panel(book, "Filepath", filepath, 168), highlight=True)
        if string:
            return filepath

        return Path(filepath)

    else:
        filepath = generate_default_filepath(book)
        return filepath


def generate_default_sections(book: int, save: bool = True) -> List[int]:
    """
    Generates a list of sections of a given book.

    Args:
        `book` (int): The given book.

        `save` (bool, optional): Whether to save the given book's sections to MongoDB. Defaults to True.

    Returns:
        `sections` (list[int]): The sections of a given book.
    """
    sections = []
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
            sections = generate_default_sections(
                int(
                    input(f"{book} is not a valid book. Please input an integer 1-10: ")
                )
            )

    if save:
        sg()
        doc = Default.objects(book=book).first()  # type: ignore
        doc.sections = sections
        doc.save()
        # log.debug(f"Saved Book {book}'s Default File's Sections: {sections}")

    console.print(default_panel(book, "Sections", sections, 295), highlight=True)
    return sections


def get_default_sections(book: int) -> list[int]:
    """
    Retrieve the sections of the given book from MongoDB

    Args:
        `book` (int): The given book.

    Returns:
        `sections` (list[int]): The sections of the given book.
    """
    sg()
    doc = Default.objects(book=book).first()  # type: ignore
    if doc.sections:
        console.print(
            default_panel(book, "Sections", doc.sections, 314), highlight=True
        )
        return doc.sections

    else:
        return generate_default_sections(book)  # type: ignore


def generate_default_cover(book: int, save: bool = True) -> str:
    """
    Generate the filename of the given book's coverpage.

    Args:
        `book` (int):
            The given book.

    Returns:
        `cover` (str):
            The filename of the given book's coverpage.
            Example: `cover1.png'
    """
    cover = f"cover{book}.png"
    if save:
        sg()
        doc = Default.objects(book=book).first()  # type: ignore
        doc.cover = cover
        doc.save()
        # log.debug(f"Saved Book {book}'s Default File's Cover: {cover}")

    console.print(default_panel(book, "Cover", cover, 393), highlight=True)
    return cover


def get_default_cover(book: int) -> str:
    """
    Retrieve the filename fo the given book's coverpage from MongoDB.

    Args:
        `book` (int): The given book.

    Returns:
        `cover` (str): The filename fo the given book's coverpage retrieved from MongoDB. Example `cover1.png`
    """
    sg()
    doc = Default.objects(book=book).first()  # type: ignore
    if doc.cover:
        console.print(default_panel(book, "Cover", doc.cover, 410), highlight=True)
        return doc.cover

    else:
        return generate_default_cover(book)


def generate_default_cover_path(
    book: int, save: bool = True, string: bool = False
) -> Path | str:
    """
    Generate the filepath for the cover page of the given book.

    Args:
        `book` (int): The given book.

        `save` (bool, optional): Whether to save the given book's coverpage filepath to MongoDB. Defaults to True.

        `string` (bool, optional): Whether to return the filepath as a string. Defaults to False.

    Returns:
        `cover_path` (Path | str): The filepath of the cover page from the given book.
    """
    cover = cv.generate_filename(book)
    book_zfill = str(book).zfill(2)
    book_dir = f"book{book_zfill}"
    cover_path = f"{BASE}/books/{book_dir}/Images/{cover}"
    # /Users/maxludden/dev/py/supergene/books/book01/Images/cover1.png

    if save:
        sg()
        doc = Default.objects(book=book).first()  # type: ignore
        doc.cover_path = cover_path
        doc.save()
        # log.debug(f"Saved Book {book}'s Default File's Cover Path: {cover_path}")

    console.print(default_panel(book, "Cover Path", cover_path, 446), highlight=True)

    if string:
        return cover_path

    else:
        return Path(cover_path)


def get_default_cover_path(book: int, string: bool = False) -> Path | str:
    """
    Retrieve the filepath of the cover page of the given book from MongoDB.

    Args:
        `book` (int): The given book.

        `string` (bool, optional): Whether to return the filepath as a string. Defaults to False.

    Returns:
        `cover_path` (Path | str): The filepath of the cover page of the given book retrieved from MongoDB.
    """
    sg()
    doc = Default.objects(book=book).first()  # type: ignore
    if doc.cover_path:
        console.print(
            default_panel(book, "Cover Path", doc.cover_path, 471), highlight=True
        )
        if string:
            return doc.cover_path
        else:
            return Path(doc.cover_path)

    else:
        cover_path = generate_default_cover_path(book, True)
        if string:
            return cover_path
        else:
            return Path(cover_path)


def generate_default_output(book: int, save: bool = False) -> str:
    """
    Generate the filename for the the ePub of the given book.

    Args:
        `book` (int): The given book.

    Returns:
        `output` (str): filename for the given book's epub.
    """
    sg()
    doc = bk.Book.objects(book=book).first()  # type: ignore
    if doc.title:
        output = f"{book} - {doc.title}.epub"

    else:
        title = bk.generate_book_title(book)
        output = f"{book} - {title}.epub"

    console.print(default_panel(book, "Output", output, 505), highlight=True)

    if save:
        sg()
        doc = Default.objects(book=book).first()  # type: ignore
        doc.output = output
        doc.save()
        # log.debug(f"Saved Book {book}'s Default File's Output: {output}")

    return output


def get_default_output(book: int) -> str:
    """
    Retrieve the filename for the given book's epub from MongoDB.

    Args:
        `book` (int): The given book.

    Returns:
        `output` (str): The filename for the given book's epub retrieved
    """
    sg()
    doc = Default.objects(book=book).first()  # type: ignore
    if doc.output:
        console.print(default_panel(book, "Output", doc.output, 530), highlight=True)
        return doc.output

    else:
        return generate_default_output(book)


def generate_default_section_part(section: int) -> int:
    """
    Generate the part number for the given section.

    Args:
        `section` (int): The given section.

    Returns:
        `part` (int): The part number for the given section.
    """
    match section:
        case 1 | 2 | 3 | 4 | 6 | 8 | 10 | 12 | 14 | 16:
            part = 1
        case 5 | 7 | 9 | 11 | 13 | 15 | 17:
            part = 2
        case _:
            raise ValueError(f"Section {section} is not a valid section number.")
    return part


def generate_default_section_chapters(section: int, save: bool = True) -> list[str]:
    """
    Generate the chapters for the given section.

    Args:
        `section` (int): The given section.

        `save` (bool, optional): Whether to save the given section's chapters to MongoDB. Defaults to True.

    Returns:
        `chapters` (list[str]): The chapters for the given section.
    """
    book = generate_default_book(section)
    sg()
    section_doc = sec.Section.objects(book=book).first()  # type: ignore
    section_chapters = section_doc.chapters

    sg()
    default_doc = Default.objects(book=book).first()  # type: ignore
    part = generate_default_section_part(section)
    match part:
        case 1:
            default_doc.section1_chapters = section_chapters
        case 2:
            default_doc.section2_chapters = section_chapters
        case _:
            raise ValueError(f"Part {part} is not a valid part number.")
    default_doc.save()

    frameinfo = getframeinfo(currentframe())  # type: ignore
    current_lineno = int(frameinfo.lineno) + 2
    console.print(
        default_panel(section, "Chapters", section_chapters, current_lineno),
        highlight=True,
    )

    return section_chapters


def generate_default_section_filenames(section: int, save: bool = True) -> list[str]:  # type: ignore
    """
    Generate the filenames for the given section.

    Args:
        `section` (int): The given section.

        `save` (int): Whether to save the given section's filenames to MongoDB.
    """
    book = generate_default_book(section)
    part = generate_default_section_part(section)
    section_zfill = str(section).zfill(2)

    sg()
    default_doc = Default.objects(book=book).first()  # type: ignore
    match part:
        case 1:
            section1_filenames = [f"section-{section_zfill}.html"]
            for chapter in default_doc.section1_chapters:
                chapter_zfill = str(chapter).zfill(4)
                section1_filenames.append(f"chapter-{chapter_zfill}.html")
            default_doc.section1_filenames = section1_filenames
            default_doc.save()

            frameinfo = getframeinfo(currentframe())  # type: ignore
            current_lineno = int(frameinfo.lineno) + 2
            console.print(
                default_panel(section, "Filenames", section1_filenames, current_lineno),
                highlight=True,
            )

            return section1_filenames

        case 2:
            section2_filenames = [f"section-{section_zfill}.html"]
            for chapter in default_doc.section2_chapters:
                chapter_zfill = str(chapter).zfill(4)
                section2_filenames.append(f"chapter-{chapter_zfill}.html")
            default_doc.section2_filenames = section2_filenames
            default_doc.save()

            frameinfo = getframeinfo(currentframe())  # type: ignore
            current_lineno = int(frameinfo.lineno) + 2
            console.print(
                default_panel(section, "Filenames", section2_filenames, current_lineno),
                highlight=True,
            )

            return section2_filenames


def get_default_section_filenames(section: int) -> list[str]:
    """
    Retrieve the filenames for the given section from MongoDB.

    Args:
        `section` (int): The given section.

    Returns:
        `filenames` (list[str]): The filenames for the given section retrieved.
    """
    book = generate_default_book(section)
    part = generate_default_section_part(section)
    sg()
    default_doc = Default.objects(book=book).first()  # type: ignore
    match part:
        case 1:
            filenames = default_doc.section1_filenames
        case 2:
            filenames = default_doc.section2_filenames
        case _:
            raise ValueError(f"Part {part} is not a valid part number.")

    frameinfo = getframeinfo(currentframe())  # type: ignore
    current_lineno = int(frameinfo.lineno) + 3
    console.print(
        default_panel(section, "Filenames", filenames, current_lineno), highlight=True
    )
    return filenames


def generate_default_section_filepaths(section: int, save: bool = True) -> list[str]:  # type: ignore
    """
    Generate the filepaths for the given section.

    Args:
        `section` (int): The given section.

    Return:
        `filepaths` (list[Path] | list[str]): The filepaths for the given section.
    """
    book = generate_default_book(section)
    part = generate_default_section_part(section)
    html_path = "{.}/html/"

    sg()
    default_doc = Default.objects(book=book).first()  # type: ignore
    match part:
        case 1:
            section1_filepaths = []
            for filename in default_doc.section1_filenames:
                section1_filepaths.append(f"{html_path}{filename}")

            if save:
                default_doc.section1_filepaths = section1_filepaths
                default_doc.save()

            frameinfo = getframeinfo(currentframe())  # type: ignore
            current_lineno = int(frameinfo.lineno) + 2
            console.print(
                default_panel(section, "Filepaths", section1_filepaths, current_lineno),
                highlight=True,
            )

            return section1_filepaths

        case 2:
            section2_filepaths = []
            for filename in default_doc.section2_filenames:
                section2_filepaths.append(f"{html_path}{filename}")
            default_doc.save()

            if save:
                default_doc.section2_filepaths = section2_filepaths
                default_doc.save()

            frameinfo = getframeinfo(currentframe())  # type: ignore
            current_lineno = int(frameinfo.lineno) + 2
            console.print(
                default_panel(section, "Filepaths", section2_filepaths, current_lineno),
                highlight=True,
            )

            return section2_filepaths


def get_default_section_filepaths(section: int) -> list[str]:
    """
    Retrieve the filepaths for the given section.
    """
    book = generate_default_book(section)
    part = generate_default_section_part(section)

    sg()
    default_doc = Default.objects(book=book).first()  # type: ignore
    match part:
        case 1:
            filepaths = default_doc.section1_filepaths
        case 2:
            filepaths = default_doc.section2_filepaths
        case _:
            raise ValueError(f"Part {part} is not a valid part number.")

    frameinfo = getframeinfo(currentframe())  # type: ignore
    current_lineno = int(frameinfo.lineno) + 3
    console.print(
        default_panel(section, "Filepaths", filepaths, current_lineno, get=True),
        highlight=True,
    )
    return filepaths


def generate_default_input_files(book: int, save: bool = True) -> list[str]:
    """
    Generate the input files for the given book.

    Args:
        `book` (int): The given book.

        `save` (bool): Whether to save the input files to MongoDB.

    Returns:
        `input_files` (list[str]): The input files for the given book.
    """
    book_zfill = str(book).zfill(2)
    input_files = [f"cover{book}.html", f"titlepage-{book_zfill}.html"]

    sg()
    default_doc = Default.objects(book=book).first()  # type: ignore
    match default_doc.section_count:
        case 1:
            for filename in default_doc.section1_filenames:
                input_files.append(filename)
        case 2:
            for filename in default_doc.section1_filenames:
                input_files.append(filename)
            for filename in default_doc.section2_filenames:
                input_files.append(filename)

    input_files.append(f"endofbook={book_zfill}.html")

    if save:
        default_doc.input_files = input_files
        default_doc.save()

    frameinfo = getframeinfo(currentframe())  # type: ignore
    current_lineno = int(frameinfo.lineno) + 2
    console.print(
        default_panel(book, "Input Files", input_files, current_lineno), highlight=True
    )

    return input_files  # type: ignore


def get_input_files(book: int) -> list[str]:
    """
    Retrieve the input files for the given book from MongoDB.

    Args:
        `book` (int): The given book.

    Returns:
        `input_files` (list[str]): The input files for the given book.
    """
    sg()
    doc = Default.objects(book=book).first()  # type: ignore
    if doc.input_files:
        return doc.input_files
    else:
        return generate_default_input_files(book, True)


def generate_default_resource_files(book: int, save: bool = True) -> list[str]:
    """
    Generate the resource files for the given book.

    Args:
        `book` (int): The given book.

        `save` (bool): Whether to save the resource files to MongoDB.

    Returns:
        `resource_files` (list[str]): The resource files for the given book.
    """
    resource_files = ["."]
    sg()
    doc = Default.objects(book=book).first()  # type: ignore

    # > Images
    resource_files.append(f"${{.}}/Images/cover{book}.png")
    resource_files.append("${.}/Images/title.png")
    resource_files.append("${.}/Images/gem.gif")

    # > CSS and Fonts
    resource_files.append("${.}/Styles/style.css")
    resource_files.append("${.}/Styles/Urbanist-Regular.ttf")
    resource_files.append("${.}/Styles/Urbanist-Italic.ttf")
    resource_files.append("${.}/Styles/Urbanist-Thin.ttf")
    resource_files.append("${.}/Styles/Urbanist-ThinItalic.ttf")
    resource_files.append("${.}/Styles/White Modesty.ttf")

    # > Metadata
    resource_files.append(f"${{.}}/yaml/epub-meta{book}.yml")
    resource_files.append(f"${{.}}/yaml/meta{book}.yml")

    # > Section(s)
    section_count = doc.section_count
    match section_count:
        case 1:
            for filepath in doc.section1_filepaths:
                resource_files.append(filepath)
        case 2:
            for filepath in doc.section1_filepaths:
                resource_files.append(filepath)
            for filepath in doc.section2_filepaths:
                resource_files.append(filepath)
        case _:
            raise ValueError(
                f"Section count {section_count} is not a valid section count."
            )

    # > End of Book
    book_zfill = str(book).zfill(2)
    resource_files.append(f"${{.}}/html/endofbook-{book_zfill}.html")

    if save:
        sg()
        doc.resource_paths = resource_files
        doc.save()

    return resource_files


def get_resource_files(book: int) -> list[str]:
    """
    Retrieve the resource files for the given book from MongoDB.

    Args:
        `book` (int): The given book.

    Returns:
        `resource_files` (list[str]): The resource files for the given book.
    """
    sg()
    doc = Default.objects(book=book).first()  # type: ignore
    if doc.resource_files:
        return doc.resource_files
    else:
        return generate_default_resource_files(book, True)


def generate_default_file(book: int, save: bool = True, write: bool = True) -> str:
    sg()
    doc = Default.objects(book=book).first()  # type: ignore
    output = doc.output
    file = f"---\nfrom: html\nto: epub\n\noutput-file: {output}\n\ninput-files:\n"

    # > Input Files
    input_files = doc.input_files
    for input_file in input_files:
        file = f"{file}- {input_file}\n"

    # > Standalone
    file = f"{file}\n\nstandalone: true\nself-contained: true\n\nresource-path:\n"

    # > Resource Files
    resource_paths = doc.resource_paths
    for resource_path in resource_paths:
        file = f"{file}- ${resource_path}\n"

    # > toc and metadata
    file = f"{file}\n\ntoc: true\ntoc-depth: 2\n\nepub-chapter-level: 2\n"
    file = f"{file}epub-cover-image: cover{book}.png\n\nepub-fonts:\n"
    file = f"{file}- Urbanist-Regular.ttf\n- Urbanist-Italic.ttf\n- Urbanist-Thin.ttf\n"
    file = f"{file}- Urbanist-ThinItalic.ttf\n- White Modesty.ttf\n\n"
    file = f"{file}epub-metadata: epub-meta{book}.yml\n\n"
    file = f"{file}metadata-files:\n- meta{book}.yml\n"
    file = f"{file}- epub-meta{book}.yml\n\n"
    file = f"{file}css-files:\n- style.css\n..."

    if save:
        sg()
        doc = Default.objects(book=book).first()  # type: ignore
        doc.content = file
        doc.save()

    if write:
        filepath = BASE / "yaml" / f"sg{book}.yml"
        with open(filepath, "w") as outfile:
            outfile.write(file)

    return file


def get_default_file(book: int) -> str:
    """
    Retrieve the default file for the given book from MongoDB.

    Args:
        `book` (int): The given book.

    Returns:
        `file` (str): The default file for the given book.
    """
    sg()
    doc = Default.objects(book=book).first()  # type: ignore
    if doc.content:
        return doc.content
    else:
        return generate_default_file(book, True, True)


# sg()
# section_doc = sec.Section.objects(section=17).first() # type: ignore
# chapters = section_doc.chapters

# sg()
# default_doc = Default.objects(book=10).first() # type: ignore
# default_doc.section2_chapters = chapters
# default_doc.save()

# frameinfo = getframeinfo(currentframe()) # type: ignore
# current_lineno = int(frameinfo.lineno) + 2
# console.print(
#     default_panel(
#         10,
#         "section2_chapters",
#         chapters,
#         current_lineno
#     )
# )
