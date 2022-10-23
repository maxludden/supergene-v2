# src/epubmeta.py
import os
from pathlib import Path
from this import d
from tkinter import N

from mongoengine import Document
from mongoengine.fields import IntField, StringField
from num2words import num2words
from rich import print, inspect
from rich.panel import Panel
from rich.pretty import pprint
from rich.progress import Progress

from src.myaml import dump, dumps, load, loads
from src.atlas import sg
from maxcolor import console, log, logpanel


class Epubmeta(Document):
    book = IntField(unique=True, required=True)
    book_word = StringField(max_length=25)
    title = StringField()
    cover_path = StringField()
    filename = StringField()
    html_path = StringField()
    filepath = StringField()
    text = StringField()
    meta = {"collection": "epubmetadata"}


def generate_epubmeta_filename(book: int, save: bool = True) -> str:
    """
    Generate the filename for the given book's Epub metadata.

    Args:
        `book` (int):
            The given book.
        `save` (bool):
            Whether to save the filename to MongoDB.

    Returns:
        `filename` (str):
            The filename for the given book's Epub metadata.
    """
    # > Generate Filename
    filename = f"epub-meta{book}.yaml"

    # > Update filename in MongoDB
    if save:
        sg()
        for doc in Epubmeta.objects():  # type: ignore
            doc.filename = filename
            doc.save()

    return filename


def get_epubmeta_filename(book: int) -> str | None:
    """
    Retrieve the given book's Epub metadata's filename from MongoDB.

    Args:
        `book` (int):
            The given book
    returns:
        `filename` (str):
            The given book's Epub metadata's filename.
    """
    sg()
    for doc in Epubmeta.objects(book=book):  # type: ignore
        return str(doc.filename)


def generate_epubmeta_filepath(book: int, save: bool = False) -> Path:
    """
    Generate the filepath for the given book's Epub metadata.

    Args:
        `book` (int):
            The given book
    returns:
        `filepath` (str):
            The filepath for the given book's Epub metadata.
    """
    book_str = str(book).zfill(2)
    filepath = f"{BASE}/books/book{book_str}/yaml/epub-meta{book}.yml"
    logpanel(
        f"Generated Book {book}' Epub metadata's filepath: \n{filepath}", level="d"
    )
    if save:
        sg()
        for doc in Epubmeta.objects(book=book):  # type: ignore
            doc.filepath = filepath
            doc.save()

    return Path(filepath)


def generate_epubmeta_html_path(book: int, save: bool = False) -> Path:
    """
    Generate the html path for the given book's Epub metadata.

    Args:
        `book` (int):
            The given book
    returns:
        `html_path` (str):
            The html path for the given book's Epub metadata.
    """
    book_str = str(book).zfill(2)
    html_path = f"{BASE}/book{book_str}/html/epub-meta{book}.html"
    logpanel(
        f"Generated Book {book}' Epub metadata's html path: \n{html_path}", level="d"
    )
    if save:
        sg()
        for doc in Epubmeta.objects(book=book):  # type: ignore
            doc.html_path = html_path
            doc.save()
    return Path(html_path)


def get_filepath(book: int) -> Path | None:
    """
    Retrieve the given book's Epub metadata's filepath from MongoDB.

    Args:
        `book` (int):
            The given book

    Returns:
        `filepath` (str):
            The given book's Epub metadata's filepath.
    """
    sg()
    for doc in Epubmeta.objects(book=book):  # type: ignore
        if doc:
            return Path(doc.filepath)
        else:
            return generate_epubmeta_filepath(book)


def get_html_path(book: int) -> Path | None:
    """
    Retrieve the given book's Epub metadata's html path from MongoDB.

    Args:
        `book` (int):
            The given book

    Returns:
        `html_path` (str):
            The given book's Epub metadata's html path.
    """
    sg()
    doc = Epubmeta.objects(book=book).first()  # type: ignore
    if doc:
        return Path(doc.html_path)
    else:
        return generate_epubmeta_html_path(book)


def generate_cover_path(book: int, save: bool = True) -> Path:
    """
    Generate the cover path for the given book's Epub metadata.

    Args:
        `book` (int):
            The given book.
        `save` (bool, optional):
            Weather or not to save the coverpage to MongoDB. Defaults to True.

    Returns:
        `cover_path` (Path):
            The filepath of the coverpage for the given book's Epub metadata.
    """
    book_str = str(book).zfill(2)
    cover_path = f"{BASE}/book{book_str}/cover.jpg"
    logpanel(f"Generated Book {book}' Epub Metadata's cover path:\n{cover_path}")

    if save:
        sg()
        for doc in Epubmeta.objects(book=book):  # type: ignore
            doc.cover_path = cover_path
            doc.save()
            logpanel(f"Saved Book {book}'s cover path to MongoDB.", level="d")

    return Path(cover_path)


def get_cover_path(book: int) -> Path:
    """
    Retrieve the given book's Epub metadata's cover path from MongoDB.

    Args:
        `book` (int):
            The given book

    Returns:
        `cover_path` (str):
            The given book's Epub metadata's cover path.
    """
    sg()
    doc = Epubmeta.objects(book=book).first()  # type: ignore
    if doc:
        return Path(doc.cover_path)
    else:
        return generate_cover_path(book)


def generate_epubmeta(book: int, save: bool = True, write: bool = True) -> None:
    """
    Generate the ePub metadata for the given book.

    Args:
        `book` (int):
            The given book.
        `save` (bool):
            Whether to save the text to MongoDB. Defaults to False.
        `write` (bool):
            Whether to write the text to a file. Defaults to False.
    Returns:
        `text` (str):
            The text for the given book's Epub metadata.
    """
    sg()
    doc = Epubmeta.objects(book=book).first()  # type: ignore
    if doc:
        title = doc.title
        book_word = doc.book_word
        author = "Twelve Winged Dark Seraphim"

        epub_meta = {
            "title": [
                {"type": "main", "text": title},
                {"type": "subtitle", "text": f"Book {book_word}"},
            ],
            "creator": [
                {"role": "author", "text": author},
                {"role": "editor", "text": "Max Ludden"},
            ],
            "css": ["style.css"],
            "cover-image": f"cover{book}.png",
            "ibooks": [
                {"version": "4.4"},
                {"specified-fonts": True},
                {"iphone-orientation-lock": "portrait-only"},
                {"scroll-axis": "vertical"},
            ],
            "belongs-to-collection": "Super Gene",
            "group-position": book,
            "page-progression-direction": "ltr",
        }

        filepath = generate_epubmeta_filepath(book, save=save)
        epub_meta_yaml = dumps(epub_meta)
        text = f"---\n{epub_meta_yaml}...\n"
        inspect(text, console=console)
        logpanel(f" Generated ePub metadata for book {book}.", level="d")

        if save:
            doc.text = text
            doc.save()
            logpanel(f"Saved Book {book}'s epub metadata to MongoDB.", level="d")

        if write:
            with open(filepath, "w") as outfile:
                outfile.write(text)
                logpanel(f"Wrote Book {book}'s epub metadata to file.", level="d")


def generate_yaml_dir(book: int) -> None:
    """
    Generate a directory for the given book's yaml files.

    Args:
        `book` (int):
            The given book.
    """
    book_str = str(book).zfill(2)
    yaml_dir = f"{BASE}/books/book{book_str}/yaml"
    if not os.path.exists(yaml_dir):
        os.makedirs(yaml_dir)
        logpanel(f"Created yaml directory for book {book}.", level="d")
    else:
        logpanel(f"Yaml directory for book {book} already exists.", level="d")


def generate_all_epubmeta() -> None:
    """
    Generate all of the ePub metadata for all of the books.
    """
    for book in (1, 11):
        generate_yaml_dir(book)
        generate_epubmeta_filepath(book, save=True)
        generate_epubmeta(book, save=True, write=True)
