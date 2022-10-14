# supergene/src/endofbook.py

import sys
from json import dump, load
from subprocess import run

from dotenv import load_dotenv
from mongoengine import Document
from mongoengine.fields import IntField, StringField
from num2words import num2words
from tqdm.auto import tqdm

from src.atlas import sg
from src.book import Book
from src.log import BASE, console, log
from src.chapter import max_title

load_dotenv()


# .#########################################
# .                                        #
# .  888'Y88              888              #
# .  888 ,'Y 888 8e   e88 888              #
# .  888C8   888 88b d888 888              #
# .  888 ",d 888 888 Y888 888              #
# .  888,d88 888 888  "88 888              #
# .                                        #
# .                                        #
# .             dP,e,                      #
# .   e88 88e   8b "                       #
# .  d888 888b 888888                      #
# .  Y888 888P  888                        #
# .   "88 88"   888                        #
# .                                        #
# .                                        #
# .  888 88b,                     888      #
# .  888 88P'  e88 88e   e88 88e  888 ee   #
# .  888 8K   d888 888b d888 888b 888 P    #
# .  888 88b, Y888 888P Y888 888P 888 b    #
# .  888 88P'  "88 88"   "88 88"  888 8b   #
# .                                        #
# .#########################################


# . ───────────────── EndofBook ──────────────────────────────────
class EndOfBook(Document):
    """End of Book Class"""

    book = IntField(required=True, unique=True)
    book_word = StringField()
    title = StringField(required=True, max_length=500)
    text = StringField()
    filename = StringField()
    mmd_path = StringField()
    html_path = StringField()
    mmd = StringField()
    html = StringField()
    meta = {"collection": "endofbook"}


def generate_filename(book: int):
    """
    Generate the filename of the given book's endofbook.

    Args:
        `book` (int):
            The given book.

    Returns:
        `filename` (str):
            The filename of the given book's endofbook.
    """
    book = str(book).zfill(2)  # type: ignore
    return f"endofbook-{book}"


def generate_md_path(book: int):
    """
    Generate the md_path of the given book's endofbook.

    Args:
        `book` (int):
            The given book.

    Returns:
        `filename` (str):
            The md_path of the given book's endofbook.
    """
    filename = get_filename(book)
    book = str(book).zfill(2)  # type: ignore
    return f"/{BASE}/books/book{book}/md/{filename}.md"


def generate_html_path(book: int):
    """
    Generate the html_path of the given book's endofbook.

    Args:
        `book` (int):
            The given book.

    Returns:
        `filename` (str):
            The html_path of the given book's endofbook.
    """
    filename = get_filename(book)
    book = str(book).zfill(2)  # type: ignore
    return f"{BASE}/books/book{book}/html/{filename}.html"


def generate_book_word(book: int):
    """Retrieves the written represintation to the given book."""
    book_word = num2words(book).capitalize()
    return book_word


def get_title(book: int):
    """Retrieves the title of the given book."""
    sg()
    for doc in Book.objects(book=book):  # type: ignore
        return max_title(doc.title)


def get_next_book(book: int):
    next_book = book + 1
    return next_book


def get_next_book_word(book: int):
    next_book_word = num2words(book + 1).capitalize()
    return next_book_word


def get_next_title(book: int):
    next_book = book + 1
    next_title = get_title(next_book)
    return next_title


def get_text(book: int):
    """Retrieves the text for the last page of the given book.

    Args:
        `book` (int):
            The given EndOfBook's Book.
    """
    if book < 10:
        book_word = generate_book_word(book)
        next_book_word = get_next_book_word(book)
        next_title = get_next_title(book)

        text = f"#### The End of Book {book_word}"
        text = f"{text}\n##### The story continues in Book {next_book_word}:"
        text = f"{text}\n#### {next_title}\n"
    elif book == 10:
        text = f"End of the Supergene's Last Book."
    else:
        error = f"Invalid input to endofbook.get_text: {book}."
        log.error(error)
        sys.exit(error)


def get_filename(book: int):
    """Generates the filename of the given book (without extension)."""
    book = str(book).zfill(2)  # type: ignore
    return f"endofbook-{book}"


def get_mmd_path(book: int):
    """Generates the filepath for mmd of the given book's last page.

    Args:
        `book` (int):
            The book of the given last page.

    Returns:
        `html_path (int):
            The filepath of the given last pages multimarkdown.
    """
    base = "/Users/maxludden/dev/py/supergene/books/"
    book = str(book).zfill(2)  # type: ignore
    mmd_path = f"{BASE}/book{book}/mmd/endofbook-{book}.mmd"
    return mmd_path


def get_html_path(book: int):
    """Generates the filepath for html of the given book's last page.

    Args:
        `book` (int):
            The book of the given last page.

    Returns:
        `html_path (int):
            The filepath of the given last pages HTML.
    """
    book = f"{BASE}/books/book{str(book).zfill(2)}"  # type: ignore
    html_path = f"{book}/html/endofbook-{book}.html"
    return html_path


def get_mmd_text(book: int):
    """Generates the text for the given book's last page.

    Args:
        book (int): The book of the give last page.

    Returns:
        str: The give last page's multimarkdown text.
    """
    if book < 10:
        next_book_word = get_next_book_word(book)
        next_title = get_next_title(book)
        text = f"##### The Story Continues in Book {next_book_word}"
        text = f"{text}\n#### {next_title}..."

    elif book == 10:
        text = f"##### The Final Book of Supergene"
        text = f"{text}\n ### The End"

    else:
        error = f"Invalid input to endofbook.make_mmd: {book}."
        log.error(error)
        sys.exit(error)

    return text


def generate_html(book: int, save: bool = True, write: bool = True):
    """Generates the multimarkdown string for the given books last page. Saved the MMD to MongoDB and to Disk.

    Args:
        `book` (int):
            The last page's book.

        `save` (bool):
            Whether or not to save the End of Book HTML to MongoDB.

        `write` (bool):
            Whether or not to write the End of Book HTML to Disk.

    Returns:
        'mmd' (str):
            The multimarkdown for the given book's last page.
    """
    sg()
    for doc in EndOfBook.objects(book=book):  # type: ignore
        log.debug(f"Accessed Book {book}'s EndOfBook in MongoDB.")
        title = doc.title
        book_word = doc.book_word
        book_str = str(book).zfill(2)  # type: ignore
        light_img = f"{BASE}/books/book{book_str}/Images/eob{book}-light.png"
        dark_img = f"{BASE}/books/book{book_str}/Images/eob{book}-dark.png"

        html = f"""<!DOCTYPE html>
<html class="eob" xmlns="http://www.w3.org/1999/xhtml" lang="en">
  <head>
    <meta charset="utf-8" />
    <title>{title}</title>
    <meta name="book" content="{book}" />
    <link type="text/css" rel="stylesheet" href="style.css" />
    <meta name="viewport" content="width=device-width" />
  </head>
  <body class="cover">
    <h2 class="eob">{title}</h2>
    <p class="eob">End of Book {book_word} of Super Gene</p>
      <picture class="eob">
        <source srcset="../Images/eob{book}-dark.png"
          alt="End of Book {book}"
          media="(prefers-color-scheme: dark)"/>
          <img class="cover" alt="End of Book {book} Page" src="../Images/eob{book}-light.png" />
      </picture>
    <p class="eob">Written by Twelve Winged Burning Seraphim</p>
    <p class="eob">Compiled and Edited by Max Ludden</p>
  </body>
</html>
"""

        # > Save the End of Book HTML to MongoDB
        if save:
            log.debug(f"Saving End of Book {book} to MongoDB.")
            doc.html = html
            doc.save()
            log.debug(f"Saved End of Book {book} to MongoDB.")

        if write:
            log.debug(f"Writing End of Book {book} to Disk.")
            path = f"{BASE}/books/book{book_str}/html/endofbook-{book_str}.html"
            with open(path, "w") as outfile:
                outfile.write(html)
            log.debug(f"Wrote End of Book {book} to Disk.")
        return html


def make_endofbooks():
    sg()
    for doc in tqdm(EndOfBook.objects(), unit="books", desc="eobs"):  # type: ignore
        book = doc.book
        html = generate_html(book, save=True, write=True)
        log.debug(f"Generated Book {book}'s End of Book's HTML.")
