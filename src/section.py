# core/section.py
from pathlib import Path
from subprocess import run
from typing import Any, List

from sh import Command
from mongoengine import Document
from mongoengine.fields import IntField, ListField, StringField
from num2words import num2words
from rich import inspect, print
from rich.panel import Panel
from rich.progress import Progress
from rich.text import Text

import src.book as Book
from src.atlas import max_title, sg
from src.log import BASE, console, log, logpanel, time
from src.myaml import dump, dumps, load, loads

# .┌─────────────────────────────────────────────────────────────────┐.#
# .│                            Section                              │.#
# .└─────────────────────────────────────────────────────────────────┘.#

# >  Static Variables
BOOK_DIR = f"{BASE}/books/"
img = (
    f'<figure>\n\t<img src="../Images/gem.gif" alt="gem" width="120" height="60" />\n  '
)


class InvalidPartException(Exception):
    pass


class SectionNotFound(Exception):
    pass


class MMDConversionException(Exception):
    pass


class MMDConversionError(Exception):
    pass


class Section(Document):
    """
    A Section is a collection of Chapters.
    """

    section = IntField(min_value=1, max_value=17)
    title = StringField()
    book = IntField(min_value=1, max_value=10)
    chapters = ListField(IntField())
    start = IntField(min_value=1)
    end = IntField(max_value=3462)
    filename = StringField()
    mmd = StringField()
    mmd_path = StringField()
    md_path = StringField()
    md = StringField()
    html_path = StringField()
    html = StringField()
    section_files = ListField(StringField())

    def __int__(self):
        return self.section

    def __str__(self):
        return self.title


@log.catch
def generate_section_book(section: int) -> int:
    """
    Determine the book of a given section.

    Args:
        `section` (int): The given section.

    Returns:
        `book` (int): The book of the given section.
    """
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
            raise SectionNotFound(f"Section {section} does not exist.")


@log.catch
def get_section_book(section: int) -> int:
    """
    Retrieve the book of the given section from MongoDB.

    Args:
        `section` (int): The given section.

    Returns:
        `book` (int): The book of the given section.
    """
    sg()
    doc = Section.objects(section=section).first()  # type: ignore
    if doc.book:
        return doc.book
    else:
        return generate_section_book(section)


@log.catch
def generate_section_part(section: int) -> int:
    """

    Determine the section Part number of its book (if it's books has more than one section.)

    Args:
        `section` (int):
            The section for which were are looking for.

    Returns:
        `part` (int):
            The given section's part number. If the given section's book contains only one section, `get_part()` will return `0`.
    """
    match section:
        case 1 | 2 | 3:
            return 0
        case 4 | 6 | 8 | 10 | 12 | 14 | 16:
            return 1
        case 5 | 7 | 9 | 11 | 13 | 15 | 17:
            return 2
        case _:
            raise InvalidPartException(f"Section {section} is not a valid section.")


@log.catch
def get_section_part(section: int) -> int:
    """
    Retrieve the part of the given section from MongoDB.

    Args:
        `section` (int): The given section.

    Returns:
        `part` (int): The part of the given section.
    """
    sg()
    doc = Section.objects(section=section).first()  # type: ignore
    if doc.part:
        return doc.part
    else:
        return generate_section_part(section)


@log.catch
def generate_part_word(section: int) -> str:
    """

    Generate the proper case of the spelled fersion od the partnu

    Args:
        `section` (int):
            The section for which were are looking for.

    Returns:
        `part` (int):
            The given section's part number. If the given section's book contains only one section, `get_part()` will return `0`.
    """
    match section:
        case 1 | 2 | 3:
            return "n/a"
        case 4 | 6 | 8 | 10 | 12 | 14 | 16:
            return "One"
        case 5 | 7 | 9 | 11 | 13 | 15 | 17:
            return "Two"
        case _:
            raise InvalidPartException(f"Section {section} is not a valid section.")


@log.catch
def get_section_part_word(section: int) -> str:
    """
    Retrieve the part word of the given section from MongoDB.

    Args:
        `section` (int): The given section.

    Returns:
        `part` (str): The part word of the given section.
    """
    sg()
    doc = Section.objects(section=section).first()  # type: ignore
    if doc.part_word:
        return doc.part_word
    else:
        return generate_part_word(section)


@log.catch
def generate_section_title(section: int, save: bool = True) -> str:
    """
    Generate the title for the given section.

    Args:
        `section` (int):
            The given section
        `save` (bool, optional):
            Whether to save the title to MongoDB. Defaults to False.

    Returns:
        `title` (str):
            The title for the given section.
    """
    match section:
        case 1:
            title = "First God's Sanctuary"
        case 2:
            title = "Second God's Sanctuary"
        case 3:
            title = "Third God's Sanctuary"
        case 4:
            title = "Part 1: Fourth God's Sanctuary"
        case 5:
            title = "Part 2: Fifth God's Sanctuary"
        case 6:
            title = "Part 1: Planet Kate"
        case 7:
            title = "Part 2: Narrow Moon"
        case 8:
            title = "Part 1: Sky Palace"
        case 9:
            title = "Part 2: Blade and Eclipse"
        case 10:
            title = "Part 1: The Ice Blue Knights"
        case 11:
            title = "Part 2: The Extreme Kings"
        case 12:
            title = "Part 1: The Systems of Chaos"
        case 13:
            title = "Part 2: The Very High"
        case 14:
            title = "Part 1: Meeting God"
        case 15:
            title = "Part 2: Fighting Sacred"
        case 16:
            title = "Part 1: The Universe of Kingdoms"
        case 17:
            title = "Part 2: Quin Kiu"
        case _:
            section = int(
                input(
                    "That is not a valid section. Please enter a valid section: (1-17) "
                )
            )
            title = generate_section_title(section)
    console.log(
        Panel(
            Text(f"Generated Title: {title}", justify="left", style="value"),
            title="['title']Section Title",
            border_style="key",
            title_align="left",
        )
    )
    if save:
        sg()
        doc = Section.objects(section=section).first()  # type: ignore
        doc.title = title
        doc.save()
    return title


@log.catch
def get_section_title(section: int) -> str:
    sg()
    doc = Section.objects(section=section).first()  # type: ignore
    if doc.title:
        return max_title(doc.title)
    else:
        return max_title(str(generate_section_title(section)))


@log.catch
def generate_section_filename(section: int, save: bool = True) -> str:
    """
    Generate the filename for the given section.

    Args:
        `section` (int): The given section.

    Returns:
        `filename` (str): The filename for the given section.
    """
    section_zfill = str(section).zfill(2)  # type: ignore
    section_filename = f"section-{section_zfill}"
    if save:
        sg()
        doc = Section.objects(section=section).first()  # type: ignore
        doc.filename = section_filename
        doc.save()
    return section_filename


@log.catch
def get_section_filename(section: int) -> str:
    """
    Retrieve the filename for the given section from MongoDB.

    Args:
        `section` (int): The given section.

    Returns:
        `filename` (str): The filename for the given section.
    """
    sg()
    doc = Section.objects(section=section).first()  # type: ignore
    if doc.filename:
        return doc.filename
    else:
        return generate_section_filename(section)


@log.catch
def generate_section_md_path(section: int, save: bool = True) -> Path:
    """
    Generate the md_path of the given section.

    Args:
        `section` (int): The given section.

    Returns:
        `md` (str): The filepath of the section's multimarkdown.
    """
    filename = get_section_filename(section)
    book = get_section_book(section)
    book_zfill = str(book).zfill(2)
    book_dir = f"book{book_zfill}"
    md_path = f"{BASE}/books/{book_dir}/md/{filename}.md"
    if save:
        sg()
        doc = Section.objects(section=section).first()  # type: ignore
        if doc is None:
            raise SectionNotFound(f"Section {section} not found.")
        else:
            doc.md_path = md_path
            doc.save()
            log.debug(f"Saved md_path for section {section} to MongoDB.")
    return Path(md_path)


@log.catch
def generate_html_path(section: int, save: bool = True) -> str:
    """
    Generate the html_path of the given section.

    Args:
        `section` (int):
            The given section.

    Returns:
        `md` (str):
            The filepath of the section's HTML.
    """
    filename = generate_section_filename(section)
    book = get_section_book(section)
    book_zfill = str(book).zfill(2)
    book_dir = f"book{book_zfill}"
    html_path = f"{BASE}/books/{book_dir}/html/{filename}.html"
    if save:
        sg()
        doc = Section.objects(section=section).first()  # type: ignore
        if doc:
            doc.html_path = html_path
            doc.save()
            log.debug(f"Saved html_path for section {section} to MongoDB.")
        else:
            raise SectionNotFound(f"Section {section} not found.")

    return html_path


@log.catch
def generate_section_start(section: int, save: bool = True) -> int:
    """
    Generate the first chapter of the given section.

    Args:
        `section` (int): The given section.

        `save` (bool): Wether to save the given section's starting chapter to MongoDB. Defaults to True.

    Returns:
        `section.start` (int): The first chapter of the given section.
    """
    match section:
        case 1:
            start = 1
        case 2:
            start = 425
        case 3:
            start = 883
        case 4:
            start = 1339
        case 5:
            start = 1680
        case 6:
            start = 1712
        case 7:
            start = 1822
        case 8:
            start = 1961
        case 9:
            start = 2166
        case 10:
            start = 2205
        case 11:
            start = 2300
        case 12:
            start = 2444
        case 13:
            start = 2640
        case 14:
            start = 2766
        case 15:
            start = 2892
        case 16:
            start = 3034
        case 17:
            start = 3304
        case _:
            section = int(
                input(
                    "That is not a valid section. Please enter a valid section: (1-17) "
                )
            )
            start = generate_section_start(section)
    if save:
        sg()
        doc = Section.objects(section=section).first()  # type: ignore
        doc.start = start
        doc.save()
    return start


@log.catch
def get_section_start(section: int) -> int:
    """
    Determine the chapter the sections starts at.

    Args:
        `section` (int):
            The given section.

    Returns:
        `start` (int):
            The chapter the given section begins.
    """
    sg()
    doc = Section.objects(section=section).first()  # type: ignore
    if doc.start:
        return doc.start
    else:
        return generate_section_start(section)


@log.catch
def generate_section_end(section: int, save: bool = True) -> int:
    """
    Generate the last chapter of the given section.

    Args:
        `section` (int): The given section.
        `save` (bool, optional): Whether to save the last chapter of the given section to MongoDB. Defaults to True.

    Returns:
        `section.end` (int): The last chapter of the given section.
    """
    match section:
        case 1:
            end = 424
        case 2:
            end = 882
        case 3:
            end = 1338
        case 4:
            end = 1679
        case 5:
            end = 1711
        case 6:
            end = 1821
        case 7:
            end = 1960
        case 8:
            end = 2165
        case 9:
            end = 2204
        case 10:
            end = 2299
        case 11:
            end = 2443
        case 12:
            end = 2639
        case 13:
            end = 2765
        case 14:
            end = 2891
        case 15:
            end = 3033
        case 16:
            end = 3303
        case 17:
            end = 3462
        case _:
            section = int(
                input(
                    "That is not a valid section. Please enter a valid section: (1-17) "
                )
            )
            end = generate_section_end(section)
    if save:
        sg()
        doc = Section.objects(section=section).first()  # type: ignore
        doc.end = end
        doc.save()
    return end


@log.catch
def get_section_end(section: int) -> int:
    """
    Determine the chapter the section ends.

    Args:
        `section` (int): The given section.

    Returns:
        `end` (int): The last chapter of the given section.
    """
    sg()
    doc = Section.objects(section=section).first()  # type: ignore
    if doc.end:
        return doc.end
    else:
        return generate_section_end(section)


@log.catch
def generate_section_md(section: int, save: bool = True, write: bool = True) -> str:
    """
    Generate the markdown for Section {section}'s Section Page.

    Args:
        `section` (int): The given section.

        `save` (bool, Optional): Whether to save the Section Page Markdown to MongoDB. Defaults to True.

        `write` (bool): Whether to write the Section Page's Markdown to Disk. Defaults to True.

    Returns:
        `md` (str): The markdown of the given section's Section Page.
    """
    sg()
    doc = Section.objects(section=section).first()  # type: ignore
    if doc is None:
        raise SectionNotFound(f"Section {section} not found.")
    else:
        log.debug(f"Section {section} Document:<code>\n{doc}\n</code>")
        title = doc.title
        book = doc.book
        book_word = str(num2words(book)).capitalize()
        start = doc.start
        end = doc.end
        md_path = doc.md_path
        part = generate_section_part(section)

        # > Yaml Frontmatter Metadata
        meta = f"---\nTitle: {title}\nBook: {book}\nPart: {part}\nCSS: ../Styles/style.css\nviewport: width=device-width, initial-scale=1.0\n...\n  \n"

        # > Atx Heading
        atx = f'# {title}\n\n<figure>\n\t<img src="../Images/gem.gif" alt="Spinning Black Gem" width="120" height="60" />\n</figure>\n\n'

        # > Text
        text = f'<p class="section-title">Written by Twelve Winged Dark Seraphim</p>\n'
        text = (
            f'{text}\n<p class="section-title">Formatted and Edited by Max Ludden</p>'
        )

        md = f"{meta}{atx}{text}"

        if save:
            doc.md = md
            doc.save()
            log.info(f"Saved md for section {section} to MongoDB.")

        if write:
            with open(md_path, "w") as infile:
                infile.write(md)
                log.debug(f"Wrote md for section {section} to {md_path}.")

        return md


@log.catch
def get_section_md(section: int):
    """
    Retrieve the multimarkdown for the given section from MongoDB.

    Args:
        `section` (int):
            The given section.

    Returns:
        `md` (str):
            The multimarkdown for the given section.
    """
    sg()
    doc = Section.objects(section=section).first()  # type: ignore
    if doc.md:
        return doc.md
    else:
        return generate_section_md(section)


@log.catch
def generate_section_html_path(section: int, save: bool = True) -> Path:
    """
    Generate the path to the HTML file for the given section.

    Args:
        `section` (int): The given section.

        'save' (bool, optional): Whether to save the HTML path to MongoDB. Defaults to True.

    Returns:
        `html_path` (Path): The path to the HTML file for the given section.
    """
    filename = get_section_filename(section)
    book_zfill = str(get_section_book(section)).zfill(2)
    book_dir = f"book{book_zfill}"
    html_path = f"{BASE}/books/{book_dir}/{filename}.html"
    if save:
        sg()
        doc = Section.objects(section=section).first()  # type: ignore
        doc.html_path = html_path
        doc.save()
    return Path(html_path)


@log.catch
def get_section_html_path(section: int) -> Path:
    """
    Retrieve the HTML path for the given section from MongoDB.

    Args:
        `section` (int): The given section.

    Returns:
        `html_path` (Path): The path to the HTML file for the given section.
    """
    sg()
    doc = Section.objects(section=section).first()  # type: ignore
    if doc.html_path:
        return Path(doc.html_path)
    else:
        return generate_section_html_path(section)


@log.catch
def generate_section_html(section: int, save: bool = True) -> str | None:
    """
    Generate the given section's HTML from it's markdown.

    Args:
        `book` (int): The given book.

        `save` (bool, optional): Whether to save the HTML to MongoDB. Defaults to True.

    Returns:
        `html` (str): The HTML for the given section.
    """
    multimarkdown = Command("multimarkdown")
    mmd = multimarkdown.bake("-f", "--nolabels", "-o")
    sg()
    doc = Section.objects(section=section).first()  # type: ignore
    if doc.md_path:
        if doc.html_path:
            try:
                result = mmd(doc.html_path, doc.md_path)
            except:
                raise MMDConversionError(f"Failed to convert {doc.md_path} to HTML.")
        else:
            doc.html_path = generate_section_html_path(section)
            try:
                result = mmd(doc.html_path, doc.md_path)
            except:
                raise MMDConversionError(f"Failed to convert {doc.md_path} to HTML.")
    else:
        doc.md_path = generate_section_md_path(section)
        if doc.html_path:
            try:
                result = mmd(doc.html_path, doc.md_path)
            except:
                raise MMDConversionError(f"Failed to convert {doc.md_path} to HTML.")
        else:
            doc.html_path = generate_section_html_path(section)
            try:
                result = mmd(doc.html_path, doc.md_path)
            except:
                raise MMDConversionError(f"Failed to convert {doc.md_path} to HTML.")

    if result.exit_code == 0:  # type: ignore
        with open(doc.html_path, "r") as infile:
            html = infile.read()
            if save:
                doc.html = html
                doc.save()
                log.info(f"Saved HTML for section {section} to MongoDB.")
            return html


@log.catch
def get_section_html(section: int) -> str | None:
    """
    Retrieve the HTML for the given section from MongoDB.

    Args:
        `section` (int): The given section.

    Returns:
        `html` (str): The HTML for the given section.
    """
    sg()
    doc = Section.objects(section=section).first()  # type: ignore
    if doc.html:
        return doc.html
    else:
        return generate_section_html(section)


@log.catch
def generate_section_chapters(section: int, save: bool = True) -> List[int] | None:
    """
    Generate the chapter numbers for the given section.

    Args:
        `section` (int): The given section.

        `save` (bool, optional): Whether to save the chapter numbers to MongoDB. Defaults to True.

    Returns:
        `chapters` (List[int]): The chapter numbers for the given section.
    """
    sg()
    doc = Section.objects(section=section).first() #type: ignore
    if doc:
        start = doc.start
        end = doc.end
        chapters = []
        for ch in range(start, end + 1):
            if ch == 3095 | ch == 3117:
                continue
            else:
                chapters.append(ch)
        if save:
            doc.chapters = chapters
            doc.save()
            logpanel(f"Saved chapters for section {section} to MongoDB.")
        return chapters
    else:
        raise SectionNotFound(f"Section {section} not found in MongoDB.")


@log.catch
def get_section_chapters(section: int) -> List[int] | None:
    """
    Retrieve the chapter numbers for the given section from MongoDB.

    Args:
        `section` (int): The given section.

    Returns:
        `chapters` (List[int]): The chapter numbers for the given section.
    """
    sg()
    doc = Section.objects(section=section).first() # type: ignore
    if doc.chapters:
        return doc.chapters
    else:
        return generate_section_chapters(section)
