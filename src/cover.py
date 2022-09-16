# core/cover.py
from mongoengine import Document
from mongoengine.fields import IntField, StringField
from ujson import dump, load

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


def create_coverpage():
    # > Loop threw books and read coverpage
    coverpages = {}
    books = range(1, 11)
    for book in books:
        book = int(book)
        book_dir = str(book).zfill(2)
        filename = f"cover{book}.html"
        html_path = f"{BASE}/books/book{book_dir}/html/{filename}"

        html = f"""<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head>
    <meta charset="utf-8"/>
    <meta name="book" content="{book}"/>
    <link type="text/css" rel="stylesheet" href="../Styles/style.css"/>
    <meta name="viewport" content="width=device-width"/>
    <title>Cover {book}</title>
</head>

<body class="cover">
    <p class="cover">
        <img class="cover" alt="Cover Page" src="../Images/cover{book}.png" />
    </p>
</body>
"""
        with open ('json/coverpages.json', 'r') as infile:
            coverpages = dict(load(infile))
            coverpages[book] = {
                "book": book,
                "filename": filename,
                "html_path": html_path,
                "html": html,
            }
            inspect(coverpages)
        with open("json/coverpages.json", "w") as outfile:
            dump(coverpages, outfile, indent=4)


def generate_filename(book: int):
    return f"cover{book}.html"


def get_filename(book: int):
    sg()
    for doc in Coverpage.objects(book=book):  # type: ignore
        return doc.filename


def generate_html_path(book: int):
    filename = get_filename(book)
    book_dir = str(book).zfill(2)
    html_path = f"{BASE}/books/book{book_dir}/html/{filename}"
    return html_path


def save_html_path(book: int):
    html_path = generate_html_path(book)
    sg()
    for doc in Coverpage.objects(book=book):  # type: ignore
        doc.html_path = html_path
        doc.save()
        log.info(f"Saved Book {book}'s html_path to MongoDB.")


def get_html_path(book: int):
    sg()
    for doc in Coverpage.objects(book=book):  # type: ignore
        return doc.html_path


def update_html_path(book: int):
    sg()
    for doc in Coverpage.objects(book=book):  # type: ignore
        doc.html_path = generate_html_path(doc.book)
        doc.save()
