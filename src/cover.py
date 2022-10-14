# core/cover.py
from mongoengine import Document
from mongoengine.fields import IntField, StringField
from ujson import dump, load
from pathlib import Path

from rich import print, inspect
from rich.text import Text
from rich.panel import Panel
from rich.progress import Progress


from src.atlas import sg
from src.log import BASE, console, log

# . ───────────────── Cover ──────────────────────────────────


class Coverpage(Document):
    book = IntField()
    filename = StringField()
    filepath = StringField()
    html_path = StringField()
    html = StringField()
    meta = {"collection": "coverpage"}


def generate_filename(book: int) -> str:
    filename = f"cover{book}.html"
    sg()

    doc = Coverpage.objects(book=book).first()  # type: ignore
    if doc:
        doc.filename = filename
        doc.save()
        log.debug(f"Saved Book {book}'s cover's filename to MongoDB.")
        console.log(
            Panel(
                Text(
                    f"Saved Book {book}'s cover's coverpage filename to MongoDB.",
                    justify="left",
                    style="white",
                ),
                title=Text(f"Generate Filename", style="green"),
                title_align="left",
                border_style="#00FF00"
            )
        )
    return f"cover{book}.html"


def get_filename(book: int) -> str:
    sg()
    doc = Coverpage.objects(book=book).first()  # type: ignore
    if str(doc.filename):
        return str(doc.filename)
    else:
        return str(generate_filename(book))


def generate_html_path(book: int) -> Path:
    filename = get_filename(book)
    book_dir = str(book).zfill(2)
    html_path = f"{BASE}/books/book{book_dir}/html/{filename}"
    sg()
    doc = Coverpage.objects(book=book).first()  # type: ignore
    if doc:
        doc.html_path = html_path
        doc.save()
        log.debug(f"Saved Book {book}'s html path to MongoDB.")
        console.log(
            Panel(
                Text(
                    f"Saved Book {book}'s coverpage html path to MongoDB.",
                    justify="left",
                    style="white",
                ),
                title=Text(f"Generate HTML Path", style="green"),
                title_align="left",
                border_style="#00FF00"
            )
        )
    return Path(html_path)


def get_html_path(book: int) -> Path:
    sg()
    doc = Coverpage.objects(book=book).first()  # type: ignore
    if str(doc.html_path):
        return Path(str(doc.html_path))
    else:
        return generate_html_path(book)


def generate_html(book: int, save: bool = True, write: bool = True) -> str:
    html = f"""<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head>
    <meta charset="utf-8"/>
    <meta name="book" content="{book}"/>
    <link type="text/css" rel="stylesheet" href="style.css"/>
    <meta name="viewport" content="width=device-width"/>
    <title>Cover {book}</title>
</head>

<body class="cover">
    <p class="cover">
        <img class="cover" alt="Cover Page" src="../Images/cover{book}.png" />
    </p>
</body>
"""
    if save:
        sg()
        doc = Coverpage.objects(book=book).first()  # type: ignore
        if doc:
            doc.html = html
            doc.html_path = str(generate_html_path(book))
            doc.save()
            msg = f"Saved Book {book}'s coverpage html to MongoDB."
            log.debug(msg)
            console.log(
                Panel(
                    Text(
                        msg,
                        justify="left",
                        style="white",
                    ),
                    title=Text(f"Generate HTML", style="green"),
                    title_align="left",
                    border_style="#00FF00"
                )
            )
    if write:
        html_path = get_html_path(book)
        with open(html_path, "w") as outfile:
            outfile.write(html)
            msg = f"Saved Book {book}'s coverpage html to {html_path}."
            log.debug(msg)
            console.log(
                Panel(
                    Text(
                        msg,
                        justify="left",
                        style="white",
                    ),
                    title=Text(f"Generate HTML", style="green"),
                    title_align="left",
                    border_style="#00FF00"
                )
            )
    return html


def get_html(book: int) -> str:
    sg()
    doc = Coverpage.objects(book=book).first()  # type: ignore
    if doc.html:
        return str(doc.html)
    else:
        return generate_html(book)