# core/chapter.py

import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial
from itertools import chain
from ujson import dump, load
from multiprocessing import Pool, Process, Queue, cpu_count
from pathlib import Path
from subprocess import run

from dotenv import load_dotenv
from mongoengine import Document
from mongoengine.fields import IntField, StringField, URLField, ListField
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from sh import Command
from tqdm.auto import tqdm, trange
from rich import print
from rich.pretty import pprint
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.box import ROUNDED

from src.atlas import max_title, sg
from maxcolor import console

# .┌─────────────────────────────────────────────────────────────────┐.#
# .│                           Chapter                               │.#
# .└─────────────────────────────────────────────────────────────────┘.#
#
load_dotenv()
URI = os.getenv("SUPERGENE")


class ChapterNotFound(Exception):
    pass


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


def max_title(title: str):
    """
    Custom title case function.

    Args:
        title (str): The string you want to transform.

    Returns:
        str: The transformed string.
    """

    title = title.lower()
    articles = [
        "a",
        "an",
        "and",
        "as",
        "at",
        "but",
        "by",
        "en",
        "for",
        "if",
        "in",
        "nor",
        "of",
        "on",
        "or",
        "per",
        "the",
        "to",
        "vs",
    ]
    word_list = re.split(" ", title)
    final = [str(word_list[0]).capitalize()]
    for word in word_list[1:]:
        word = str(word)
        final.append(word if word in articles else word.capitalize())

    result = " ".join(final)

    return result


DRIVER_PATH = Path.cwd() / "driver" / "chromedriver"


def generate_unparsed_text(chapter: int) -> str:
    """
    Download the text of a chapter from the Super Gene website.

    Args:
        `chapter` (int): The chapter number.

    Returns:
        `unparsed_text` (str): The text of the chapter.
    """
    # Initial Variables
    chapter_str = str(chapter)

    lines = []
    title_prefix = "Super Gene Chapter "
    title_suffix = " Online | BestLightNovel.com"

    # Get URL
    sg()
    doc = Chapter.objects(chapter=chapter).first()  # type: ignore
    URL = doc.url

    # Chrome Webdriver
    PATH = str(DRIVER_PATH)
    options = ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(PATH, options=options)

    # Get Chapter Page
    driver.get(URL)

    # Get article title
    article_title = driver.title
    article_title = str(article_title)
    article_title = article_title.replace(title_prefix, "").replace(title_suffix, "")

    try:
        settings_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "SETTING"))
        )
        settings_button.click()

        change_bad_words_button = driver.find_element(
            By.XPATH, '//*[@id="trang_doc"]/div[6]/div[1]/div[2]/ul/li[5]/a'
        )
        change_bad_words_button.click()
        try:
            text = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "vung_doc"))
            )
            text = driver.find_element(By.ID, "vung_doc")
            paragraphs = text.find_elements(By.TAG_NAME, "p")
            text = ""
            for paragraph in paragraphs:
                text = str(text + paragraph.text + "\n\n")

            # Strip erroneous whitespace characters
            text = text.strip()

            # Save text to MongoDB
            doc.text = text
            doc.save()

        except:
            print("\n\n\nError 404\nUnable to locate text on page. Quitting Script.\n")
    finally:
        driver.quit()
    return doc.text


def vog(text):
    text = str(text)
    blockquote_regex = [
        r"\n(^\".*?killed.*?beast soul.*?point.*?\")$",
        r"\n(^\".*?flesh.*?point.*?\")$",
        r"\n(^\".*?Xenogeneic.*?hunted.*?gene.*?\")$",
        r"\n(^\".*?hunted.*?:.*?beast soul.*?\")$",
        r"\n(^\".*?killed.*?beast soul.*?inedible.*?\")$",
        r"\n(^\".*?beast soul.*?:.*?\")$",
        r"\n(^\".*?beast soul.*?;.*?\")$",
        r"\n(^\".*?:.*?gene lock.*?\")$",
        r"\n(^\".*?gene.*?\+\d+.*?\")$",
        r"\n(^\".*?hunted.*?found.*?.*?\")$",
        r"\n(^\".*?body.*?evol.*?success.*?\")$",
        r"\n(^\".*?consumed.*?geno point.*?\")$",
        r"\n(^\".*?;.*?status.*?\")$",
        r"\n(^\".*?retrieve.*?beast soul.*?from.*?\")$",
        r"\n(^\".*?obtained.*?random.*?\")$",
        r"\n(^\".*?absorb.*?geno point.*?\")$",
        r"\n(^\".*?announce.*?:.*?\")$",
        r"\n(^\".*?eaten\..*?geno point.*?\")$",
        r"\n(^\".*?egg broken.*?identi.*?\")$",
        r"\n(^\".*?Identifying.*?beast soul.*?\")$",
        r"\n(^\".*?beast soul.*?identi.*?gained.*?\")$",
        r"\n(^\".*?killed.*?beast soul.*?life essence.*?\")$",
        r"\n(^\".*?evolution.*?super body.*?\")$",
        r"^(\".*?killed.*?beast soul.*?geno core.*?flesh.*?\")$",
        r"\n(^\"Deified Gene.*?+1.*?\")$",
        r"\n(^\"God.*?Evolu.*?\")$",
    ]
    matches = []
    for regex in blockquote_regex:
        matches = re.findall(regex, text, re.I | re.M)
        if matches:
            for match in matches:
                block = str("> " + match)
                block = block.title()
                text = re.sub(match, block, text, re.I, re.M)
            duplicate_regex = r"^(> > )\""
            duplicate_results = re.findall(duplicate_regex, text, re.I | re.M)
            if duplicate_results:
                for x in duplicate_results:
                    rep_str = r"> "
                    text = re.sub(x, rep_str, text, re.I | re.M)
    return text


def badWords(text: str):
    badWords = {
        "shit1": {"regex": r"sh\*t", "replacement": "shit"},
        "shit2": {"regex": r"s\*#t", "replacement": "shit"},
        "shit3": {"regex": r"Sh\*t", "replacement": "Shit"},
        "shit4": {"regex": r"S\*#t", "replacement": "Shit"},
        "fuck1": {"regex": r"f\*#k", "replacement": "fuck"},
        "fuck2": {"regex": r"f\*ck", "replacement": "fuck"},
        "fuck3": {"regex": r"F\*#k", "replacement": "Fuck"},
        "fuck4": {"regex": r"F\*ck", "replacement": "Fuck"},
        "bitch1": {"regex": r"b\*tch", "replacement": "bitch"},
        "bitch2": {"regex": r"B\*tch", "replacement": "Bitch"},
        "ass1": {"regex": r" \*ss ", "replacement": " ass "},
        "ass2": {"regex": r"\n\*ss ", "replacement": "\nAss "},
        "ass3": {"regex": r"\. \*ss ", "replacement": ". Ass "},
    }
    keys = badWords.keys()
    for key in keys:
        regex = badWords[key]["regex"]
        results = re.findall(regex, text, re.I)
        if results:
            replacement = badWords[key]["replacement"]
            for x in results:
                text = re.sub(regex, replacement, text, re.I)
                log.info("\n\t\t\tUpdated " + regex + " -> " + replacement)
    return text


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
            log.warning(
                f"Chapter {chapter} was inputted to generate_section().\nChapter {chapter} does not exist."
            )
        elif chapter == 3117:
            log.warning(
                f"Chapter {chapter} was inputted to generate_section(). \nChapter {chapter} does not exist."
            )
            pass
        else:
            return 15
    elif chapter <= 3303:  # book10
        return 16
    elif chapter <= 3462:  # book10
        return 17
    else:
        raise ValueError("Invalid Chapter", f"\nChapter: {chapter}")


def get_section(chapter: int) -> int | None:
    """
    Retrieve the section of a given chapter from MongoDB.

    Args:
        `chapter` (int):
            The given chapter.

    Raises:
        ValueError: Invalid Chapter number

    Returns:
        `section` (int):
            The section of the given chapter.
    """
    sg()
    for doc in Chapter.objects(chapter=chapter):  # type: ignore
        return doc.section


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
    section = get_section(chapter)
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


def get_book(chapter: int) -> int | None:
    """
    Retrieve the book for the given chapter from MongoDB.

    Args:
        `chapter` (int):
            The given chapter.

    Returns:
        `book` (int):
            The book for the given chapter.
    """
    sg()
    for doc in Chapter.objects(chapter=int(chapter)):  # type: ignore
        return doc.book


def get_title(chapter: int) -> str | None:
    """
    Retrieve the Title of the given chapter from MongoDB.

    Args:
        `chapter` (int):
            The given chapter.

    Returns:
        `title` (str):
            The title of the given chapter.
    """
    sg()
    for doc in Chapter.objects(chapter=chapter):  # type: ignore
        title = max_title(doc.title)
        return title


def generate_filename(chapter: int) -> str:
    """
    Generate the filename for the given chapter.

    Args:
        `chapter` (int):
            The given chapter.

    Returns:
        `filename` (str):
            the filename (without extension) for the given chapter.
    """
    chapter_str = str(chapter).zfill(4)
    return f"chapter-{chapter_str}"


def get_filename(chapter: int) -> str | None:
    """
    Retrieve the filename of the given chapter from MongoDB.

    Args:
        `chapter` (int):
            The given chapter.

    Returns:
        `filename` (str):
            The filename of the given chapter without a file extension.
    """
    sg()
    for doc in Chapter.objects(chapter=chapter):  # type: ignore
        return doc.filename


def generate_md_path(chapter: int) -> str:
    """
    Generates the path to where the given chapter's multimarkdown will be stored.

    Args:
        `chapter` (int)
            The given chapter.

    Returns:
        `md_path` (str):
            The filepath of the the given chapter's multimarkdown.
    """
    # > Generate book and filename from the given chapter
    book = get_book(chapter)
    filename = get_filename(chapter)

    # > Pad the chapter number to four digits
    book_zfill = str(book).zfill(2)
    book_dir = f"book{book_zfill}"

    md_path = f"{BASE}/books/{book_dir}/md/{filename}.md"
    return md_path


def get_md_path(chapter: int) -> Path | None:
    """
    Retrieve the path of the the given chapter's multimarkdown from MongoDB.

    Args:
        `chapter` (int):
            The given chapter.

    Returns:
        `md_path` (str):
            The filepath for the given chapter.
    """
    sg()
    for doc in Chapter.objects(chapter=chapter):  # type: ignore
        return doc.md_path


def generate_html_path(chapter: int) -> str:
    """
    Generates the path to where the given chapter's HTML will be stored.

    Args:
        `chapter` (int)
            The given chapter.

    Returns:
        `html_path` (str):
            The filepath to the given chapter's HTML.
    """
    book = get_book(chapter)
    filename = get_filename(chapter)

    book_zfill = str(book).zfill(2)
    book_dir = f"book{book_zfill}"

    html_path = f"{BASE}/books/{book_dir}/html/{filename}.html"
    return html_path


def get_html_path(chapter: int) -> Path | None:
    """
    Retrieve the filepath of the given chapter from MongoDB.

    Args:
        `chapter` (int):
            The given chapter.

    Returns:
        `html_path` (str):
            The filepath of the given chapter.
    """
    sg()
    for doc in Chapter.objects(chapter=chapter):  # type: ignore
        return Path(doc.html_path)


def generate_text_path(chapter: int) -> str:
    """
    Generates the path to where the given chapter's text will be stored.

    Args:
        `chapter` (int)
            The given chapter.

    Returns:
        `text_path` (str):
            The filepath to the given chapter's text.
    """
    book = get_book(chapter)
    filename = get_filename(chapter)

    book_zfill = str(book).zfill(2)
    book_dir = f"book{book_zfill}"

    text_path = f"{BASE}/books/{book_dir}/text/{filename}.txt"
    return text_path


def get_text_path(chapter: int) -> str | None:
    """
    Retrieve the filepath of the given chapter from MongoDB.

    Args:
        `chapter` (int):
            The given chapter.

    Returns:
        `text_path` (str):
            The filepath of the given chapter.
    """
    sg()
    for doc in Chapter.objects(chapter=chapter):  # type: ignore
        return doc.text_path


def generate_md(chapter: int, save: bool = False, write: bool = False) -> str | None:
    """
    Generates the multimarkdown string for the given chapter. Saves the markdown string to disk (md_path) as well as to MongoDB.

    Requires an active connection to MongoDB.

    Args:
        `chapter` (int):
            The given chapter.
        `save` (bool):
            Whether or not to save the markdown string to MongoDB.
        `write` (bool):
            Whether or not to write the markdown string to disk.

    Returns:
        `md` (str):
            The multimarkdown for the given chapter.
    """
    sg()
    for doc in Chapter.objects(chapter=chapter):  # type: ignore
        # Books 4-10 have two sections a piece
        title = max_title(doc.title)
        # > Multimarkdown Metadata
        meta = f"---\nTitle:{title} \nChapter:{doc.chapter} \nSection:{doc.section} \nBook:{doc.book} \nCSS:../Styles/style.css \nviewport: width=device-width\n---\n  \n"

        # > ATX Headers
        img = """<figure>\n\t<img src="../Images/gem.gif" alt="gem" id="gem" width="120" height="60" />\n</figure>\n  \n"""

        atx = f"## {title}\n### Chapter {doc.chapter}\n  \n{img}\n  \n"

        # > Chapter Text
        text = f"{doc.text}"

        # > Concatenate Multimarkdown
        md = f"{meta}{atx}{text}"

        if save:
            doc.md = md
            doc.save()

        if write:
            with open(doc.md_path, "w") as outfile:
                outfile.write(md)
                log.debug("Wrote Chapter {doc.chapter}'s multimarkdown to disk.")
        return md


def get_md(chapter: int) -> str | None:
    """
    Retrieve the multimarkdown for the given chapter from MongoDB.

    Args:
        `chapter` (int):
            The given chapter.

    Returns:
        `md` (str):
            The multimarkdown of the given chapter.
    """
    sg()
    for doc in Chapter.objects(chapter=chapter):  # type: ignore
        return doc.md


def generate_html(chapter: int, save: bool = False) -> str | None:
    """
    Generate the HTML for a given chapter. Save the given chapter's HTML to disk (html_path) as well as to MongoDB.

    Args:
        `chapter` (int):
            The MongoDB Chapter document for the given chapter.

    Returns:
        `html` (str):
            The HTML for the given chapter.
    """
    mmd = Command("multimarkdown")
    mmd = mmd.bake("-f", "--nolables", "-o")
    sg()
    for doc in Chapter.objects(chapter=chapter):  # type: ignore
        md_cmd = [
            "multimarkdown",
            "-f",
            "--nolabels",
            "-o",
            f"{doc.html_path}",
            f"{doc.md_path}",
        ]
        log.debug(f"Markdown Path: {doc.md_path}")
        log.debug(f"HTML Path: {doc.html_path}")
        log.debug(f"Multimarkdown Command: {md_cmd})")
        try:
            result = run(md_cmd)

        except OSError as ose:
            raise OSError(ose)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as e:
            log.error(e)
            sys.exit(
                "Error occurred in the process of creating HTML for Chapter {doc.chapter}"
            )

        else:
            log.debug(f"Result of MD Command: {result.__str__}")

        if save:
            with open(doc.html_path, "r") as infile:
                html = infile.read()  # type: ignore
            log.debug(f"Saved Chapter {chapter}'s HTML to disk.")

            doc.html = html
            doc.save()
            log.debug(f"Saved Chapter {chapter}'s HTML to MongoDB.")
            return html


def get_html(chapter: int) -> str | None:
    """
    Retrieve the HTML of the given chapter from MongoDB.

    Args:
        `chapter` (int):
            The given chapter.

    Returns:
        `html` (str):
            The HTML of the given chapter.
    """
    sg()
    for doc in Chapter.objects(chapter=chapter):  # type: ignore
        return doc.html


def write_md(chapter: int) -> None:
    """
    Retrieves the given chapter's multimarkdown from MongoDB and writes it to disk (md_path)

    Args:
        `chapter` (int):
            The given chapter
    """
    sg()
    for doc in Chapter.objects(chapter=chapter):  # type: ignore
        log.debug(f"MD Path: {doc.md_path}")
        length = len(doc.md)
        log.debug(f"Markdown Length: {length}")

        with open(doc.md_path, "w") as outfile:
            outfile.write(doc.md)
    log.debug(f"Wrote Chapter {chapter}'s Multimarkdown to Disk.")


def make_chapters() -> None:
    """
    Generate the values needed to create the chapter.
    """
    sg()
    for doc in tqdm(Chapter.objects(), unit="ch", desc="Creating Chapters"):  # type: ignore
        chapter = doc.chapter
        log.debug(f"Accessed Chapter {chapter}'s MongoDB Document.")

        # > Section
        section = generate_section(chapter)
        log.debug(f"Chapter {chapter}'s section: {section}")
        doc.section = section
        log.debug(f"Updated Chapter {chapter}'s {section}.")

        # > Book
        book = generate_book(chapter)
        log.debug(f"Chapter {chapter}'s book: {book}")
        doc.book = book
        log.debug(f"Updated Chapter {chapter}'s {book}.")

        # > Title
        title = get_title(chapter)
        log.debug(f"Chapter {chapter}'s title: {title}")
        doc.title = title
        log.debug(f"Updated Chapter {chapter}'s {title} in MongoDB.")

        # > Filename
        filename = generate_filename(chapter)
        log.debug(f"Chapter {chapter}'s Filename: {filename}")
        doc.filename = filename
        log.debug(f"Updated Chapter {chapter}'s filename in MongoDB")

        # > Md_path
        md_path = generate_md_path(chapter)
        log.debug(f"Chapter {chapter}'s Multimarkdown Path: {md_path}")
        doc.md_path = md_path
        log.debug(f"Updated Chapter {chapter}'s Multimarkdown filepath.")

        # > Html_path
        html_path = generate_html_path(chapter)
        log.debug(f"Chapter {chapter}'s html_path: {html_path}")
        doc.html_path = html_path
        log.debug(f"Updated Chapter {chapter}'s {html_path}.")

        doc.save()

        log.debug(f"Finished Chapter {chapter}.")


def verify_chapters() -> None:
    """
    Update all the values of each chapter dict.
    """
    sg()
    for doc in tqdm(Chapter.objects(), unit="ch", desc="updating paths"):  # type: ignore
        chapter = doc.chapter

        # > Section
        if doc.section != "":
            section = doc.section
        else:
            section = generate_section(chapter)
        doc.section = section
        log.debug(f"Section: {section}")

        # > Book
        if doc.book != "":
            book = doc.book
        else:
            book = generate_book(chapter)
        doc.book = book
        log.debug(f"Book: {book}")

        # > Md_path
        if doc.md_path != "":
            md_path = doc.md_path
        else:
            md_path = generate_md_path(chapter)
        doc.md_path = md_path
        log.debug(f"MD Path: {md_path}")

        # > HTML_path
        if doc.html_path != "":
            html_path = doc.html_path
        else:
            html_path = generate_html_path(chapter)
        doc.html_path = html_path
        log.debug(f"HTML Path: {html_path}")

        # > MD
        if doc.md != "":
            md = doc.md
        else:
            md = generate_md(chapter)
        doc.md = md
        length = len(str(md))
        log.debug(f"MD length: {length}")

        # > HTML
        if doc.html != "":
            html = doc.html
        else:
            html = generate_html(chapter)
        doc.html = html
        length = len(str(html))
        log.debug(f"HTML Length: {length}")

        doc.save()
        log.info(f"Finished chapter {chapter}")


def nb() -> None:
    sg("LOCALDB")

    nb = "Nyoi-Bo"
    for doc in tqdm(Chapter.objects(), unit="ch", desc=f"fixing {nb}"):  # type: ignore
        chapter = doc.chapter
        if nb in doc.unparsed_text:
            log.debug(f"Working on Chapter {chapter}")
            text = doc.unparsed_text
            split_text = text.split("\n\n")
            save = False
            for i, line in enumerate(split_text, start=1):
                if i == 1:
                    if nb in line:
                        line = ""
                        log.info(f"Fixed {nb} in Chapter {chapter}")
                        save = True
                    if "Translator" in line:
                        line = ""
                        log.info(f"Fixed Translator in Chapter {chapter}")
                        save = True
                if i == 2:
                    if nb in line:
                        line = ""
                        log.info(f"Fixed {nb} in Chapter {chapter}")
                        save = True
                    if "Translator" in line:
                        line = ""
                        log.info(f"Fixed Translator in Chapter {chapter}")
                        save = True
            if save:
                doc.unparsed_text = "\n\n".join(split_text)
                doc.save()
                log.info(f"Saved Chapter {chapter}")


def remove_translator(chapter: int) -> str | None:
    sg("LOCALDB")
    doc = Chapter.objects(chapter=chapter).first()  # type: ignore
    if doc is None:
        raise ChapterNotFound(f"Unable to find chapter {chapter}")
    translator = "Translator: Nyoi-Bo Studio Editor: Nyoi-Bo Studio\n\n"
    if translator in doc.unparsed_text:
        doc.unparsed_text = doc.unparsed_text.replace(translator, "")
        doc.save()
        log.info(f"Removed Translator from Chapter {chapter}")


def verify_nyoi(chapter: int) -> str | None:
    """
    Determine if a given chapter contains the Nyoi-Bo.

    Args:
        `chapter` (int):
            The given chapter

    Raises:
        `ChapterNotFound`:
            Custom exception if the given chapter is not able to be found.

    Returns:
        `chapter` (Optional[int]):
            The given chapter's number if the Nyoi-Bo is found.
    """
    sg("LOCALDB")
    doc = Chapter.objects(chapter=chapter).first()  # type: ignore
    if doc is None:
        raise ChapterNotFound(f"Unable to find chapter {chapter}")
    if "Nyoi-Bo" in doc.unparsed_text:
        log.info(f"Chapter {doc.chapter} contains Nyoi-Bo")
        return doc.chapter
    return None
