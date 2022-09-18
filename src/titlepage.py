# core/titlepage.py

import ujson
from pathlib import Path
from typing import Optional
from mongoengine import Document
from mongoengine.fields import IntField, StringField
from num2words import num2words
from rich import inspect, print
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress
from rich.text import Text
from rich.style import Style
from sh import Command, RunningCommand

import myaml
from src.atlas import sg
from src.log import BASE, console, log, logpanel

# .┌─────────────────────────────────────────────────────────────────┐.#
# .│                            Titlepage                            │.#
# .└─────────────────────────────────────────────────────────────────┘.#

class MMDConversionException(Exception):
    pass

class TitlepageNotFound(Exception):
    pass

TEXT = '### Written by Twelve Winged Dark Seraphim\n ### Complied and Edited by Max Ludden'

class Titlepage(Document):
    book = IntField(required=True, unique=True, min_value=1, max_value=10)
    book_word = StringField(max_length=20)
    title = StringField(required=True, max_length=500)
    text = StringField()
    filename = StringField()
    md_path = StringField()
    html_path = StringField()
    md = StringField()
    html = StringField()

    def __int__(self):
        return self.book

def titlepage_panel(book: int, key: str = "Key", value: str | int | Markdown = "Value", line: int = 1, title: Optional[str] = None, get: bool = False, width = 60) -> Panel:
    if title:
        title = title
    else:
        title = f"Titlepage {book}"

    if get:
        get_verb = "Retrieved"
    else:
        get_verb = "Generated"

    panel = Panel(
        f"[#eed4fc]{get_verb} {key}:[/][bold bright_white] {str(value)}[/]",
        title=Text(f"{title}", style=Style(color="#8e47ff", bold=True)),
        title_align="left",
        subtitle=f"[purple]src/titlepage.py[/][#FFFFFF]|[/][#54c6ff]line {line}[/]",
        subtitle_align="right",
        border_style=Style(color="#5f00ff"),
        expand=False,
    )
    return panel


def generate_titlepage_filename(book: int, save: bool = True) -> str:
    """
    Generates a filename for a given book's titlepage.

    Args:
        `book` (int):
            The book number.
        `save` (bool):
            Whether to save the filename to the database. Defaults to True

    Returns:
        `filename` (str):
            The filename.

    """
    book_zfill = str(book).zfill(2)
    filename = f'titlepage-{book_zfill}'

    if save:
        sg()
        doc = Titlepage.objects(book=book).first() # type: ignore # type: ignore
        doc.filename = filename
        doc.save()
        log.debug(f"Saved Book {book}'s titlepage to MongoDB. Filename:<code>\n{filename}</code>")

    console.print(
        titlepage_panel(book, "Filename", filename, 96), highlight=True
    )
    return filename


def get_titlepage_filename(book: int) -> str:
    sg()
    doc = Titlepage.objects(book=book).first() # type: ignore # type: ignore
    if doc is None:
        raise TitlepageNotFound(f"Titlepage for Book {book} not found.")
    console.print(
        titlepage_panel(book, "Filename", doc.filename, 107, get=True),highlight=True
    )
    return doc.filename



def generate_titlepage_md_path(book: int, save: bool = True) -> Path:
    """
    Generates a path for a given book's titlepage's Markdown file.

    Args:
        `book` (int):
            The book number.
        `save` (bool):
            Whether to save the path to the database. Defaults to `True`.

    Returns:
        `md_path` (str):
            The path.

    """
    book_zfill = str(book).zfill(2)
    filename = generate_titlepage_filename(book)
    md_path = f'{BASE}/books/book{book_zfill}/md/{filename}.md'

    if save:
        sg()
        doc =  Titlepage.objects(book=book).first() # type: ignore
        doc.md_path = md_path
        doc.save()
        log.debug(f"Saved Book {book}'s titlepage to MongoDB. Markdown path:<code>\n{md_path}</code>")

    console.print(
        titlepage_panel(book, "Markdown Path", md_path, 140), highlight=True
    )
    return Path(md_path)


def get_titlepage_md_path(book: int) -> Path:
    sg()
    doc = Titlepage.objects(book=book).first() # type: ignore
    if doc.md_path:

        console.print(
            titlepage_panel(book, "Markdown Path", doc.md_path, 151, get=True), highlight=True
        )
        return Path(doc.md_path)
    else:
        return generate_titlepage_md_path(book)



def generate_titlepage_html_path(book: int, save: bool = True):
    """
    Generates a path for a given book's titlepage's HTML file.

    Args:
        `book` (int):
            The book number.
        `save` (bool):
            Whether to save the path to the database.

    Returns:
        `html_path` (str):
            The path.

    """
    book_zfill = str(book).zfill(2)
    html_path = f'{BASE}/books/book{book_zfill}/html/titlepage-{book_zfill}.html'
    if save:
        sg()
        doc = Titlepage.objects(book=book).first() # type: ignore
        if doc:
            doc.html_path = html_path
            doc.save()
            log.debug(f"Saved Book {book}'s titlepage to MongoDB. HTML path:<code>\n{html_path}</code>")
        else:
            raise TitlepageNotFound(f"Titlepage for Book {book} not found.")

    console.print(
        titlepage_panel(book, "HTML Path", html_path, 187)
    )
    return Path(html_path)



def get_titlepage_html_path(book: int) -> Path:
    '''
    Retrieve the html path for the given book's titlepage.

    Args:
        `book` (int): The given book.

    Returns:
        `html_path` (Path): The path to the given book's titlepage's HTML file.
    '''
    sg()
    doc = Titlepage.objects(book=book).first() # type: ignore
    if doc.html_path:

        console.print(
            titlepage_panel(book, "HTML Path", doc.html_path, 208, get=True)
        )
        return Path(doc.html_path)
    else:
        return generate_titlepage_html_path(book)



def generate_titlepage_md(book: int, save: bool = True, write = True) -> str | None:
    '''
    Generate the markdown for the given book's titlepage.

    Args:
        `book` (int): The given book.

        `save` (bool, optional):  Whether to save the titlepage markdown to MongoDB. Defaults to `True`.

        `write` (bool, optional): Whether to write the titlepage's markdown to disk. Defaults to `True`.

    Returns:
        `md` (str): The markdown of the given book's titlepage.
    '''
    book_zfill = str(book).zfill(2)
    sg()
    doc = Titlepage.objects(book=book).first() # type: ignore
    if doc:
        title = doc.title
        text = doc.text
        book_word = doc.book_word

        img = f'<figure>\n\t<img class="titlepage" src="../Images/gem.gif" alt="gem" />\n</figure>\n'

        meta = f"---\nTitle: {title}\nBook: {book}\nCSS: ../Styles/styles.css\nviewport: width=device-width, initial-scale=1.0\n..."

        atx = f'\n# {title}\n<br />\n### Book {book_word}<br />{img}\n'

        text = 'FOOTER'

        md = f'{meta}{atx}\n\n{text}'

        doc.filename = generate_titlepage_filename(book)
        log.debug(f"Generated Book {book}'s titlepage's filename.")

        doc.md_path = generate_titlepage_md_path(book)
        log.debug(f'Generated titlepage filepath for book {book}.')

        doc.html_path = generate_titlepage_html_path(book)

        if save:
            doc.md = md
            doc.save()
            log.debug(f'Saved titlepage markdown for book {book}.')

        if write:
            with open(doc.md_path, 'w') as f:
                f.write(md)
                log.debug(f'Wrote titlepage markdown for book {book} to disk.')

        console.print(
            titlepage_panel(book, "Markdown", md, 267), highlight=True
        )
        return md


def get_titlepage_md(book: int) -> str:
    sg()
    doc = Titlepage.objects(book=book).first() # type: ignore
    if doc.md:
        console.print(
            titlepage_panel(book, "Markdown", Markdown(doc.md), 277, get=True)
        )
        return doc.md

    else:
        return str(generate_titlepage_md(book))


def generate_titlepage_html(book: int, save: bool = True) -> str | None:
    '''
    Generate the html for the given book's titlepage.

    Args:
        `book` (int):
            The given book
        `save` (bool, optional):
            Whether to save the html to MongoDB. Defaults to `True`.

    Returns:
        `html` (str):
            The html for the given book's titlepage.
    '''
    #. Create MMD Command
    multimarkdown = Command('multimarkdown')
    mmd = multimarkdown.bake('-f', '--nolables', '-o')

    #. Connect to MongoDB
    sg()
    doc = Titlepage.objects(book=book).first() # type: ignore

    # > Define save conditions
    def save_titlepage_html(result: RunningCommand | None, book: int) -> str | None:
        sg()
        doc = Titlepage.objects(book=book).first() # type: ignore
        if result.exit_code == 0: # type: ignore
            with open (doc.html_path, 'r') as infile:
                html = infile.read()
                html = html.replace('<p>FOOTER</p>', doc.footer)
                doc.html = html
                doc.save()
                log.debug(f"Saved Book {book}'s titlepage HTML to MongoDB.")

                return html

    doc.md_path = generate_titlepage_md_path(book)
    doc.html_path = generate_titlepage_html_path(book)
    doc.save()
    html = save_titlepage_html(mmd(doc.md_path, doc.html_path), book)
    footer = """ 	<div class="footer">
		<h3>Written by Twelve Winged Dark Seraphim</h3>

		<h3>Formatted and Edited by Max Ludden</h3>
	</div>"""
    html = str(html).replace('<p>FOOTER</p>', footer)
    
    console.print(
        titlepage_panel(book, "HTML", f'\n\n{html}', 315)
    )
    return html
