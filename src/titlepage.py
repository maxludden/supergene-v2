# core/titlepage.py

from json import dump
from subprocess import run

from mongoengine import Document
from mongoengine.fields import StringField, IntField
from num2words import num2words
from tqdm.auto import tqdm, trange
from alive_progress import alive_bar

from src.atlas import sg
from src.log import BASE, console, log, logpanel
from src.myaml import dump, dumps, load, loads


# .┌─────────────────────────────────────────────────────────────────┐.#
# .│                            Titlepage                            │.#
# .└─────────────────────────────────────────────────────────────────┘.#

class MMDConversionException(Exception):
    pass

class TitlepageNotFound(Exception):
    pass

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

def titlepage_panel(book: int,)


def generate_filename(book: int, save: bool = False) -> str:
    """
    Generates a filename for a given book's titlepage.

    Args:
        `book` (int):
            The book number.
        `save` (bool):
            Whether to save the filename to the database.

    Returns:
        `filename` (str):
            The filename.

    """
    book_str = str(book).zfill(2)
    filename = f'titlepage-{book_str}'

    if save:
        sg()
        doc = Titlepage.objects(book=book): # type: ignore
        doc.filename = filename
        doc.save()
        log.debug(f"Saved Book {book}'s titlepage to MongoDB. Filename:<code>\n{filename}</code>")
    return filename


def get_filename(book: int):
    sg()
    titlepage = Titlepage.objects(book=book).first()
    if titlepage is None:
        raise TitlepageNotFound(f"Titlepage for Book {book} not found.")
    return titlepage.filename



def generate_md_path(book: int, save: bool = False):
    """
    Generates a path for a given book's titlepage's Markdown file.

    Args:
        `book` (int):
            The book number.
        `save` (bool):
            Whether to save the path to the database.

    Returns:
        `md_path` (str):
            The path.

    """
    book_str = str(book).zfill(2)
    md_path = f'{BASE}/books/book{book_str}/md/{generate_filename(book)}.md'
    if save:
        sg()
        for titlepage in Titlepage.objects(book=book): # type: ignore
            titlepage.md_path = md_path
            titlepage.save()
            log.debug(f"Saved Book {book}'s titlepage to MongoDB. Markdown path:<code>\n{md_path}</code>")
    return md_path


def get_md_path(book: int):
    sg()
    titlepage = Titlepage.objects(book=book).first()
    if titlepage is None:
        raise TitlepageNotFound(f"Titlepage for Book {book} not found.")
    return titlepage.md_path



def generate_html_path(book: int, save: bool = False):
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
    book_str = str(book).zfill(2)
    html_path = f'{BASE}/books/book{book_str}/html/titlepage-{book_str}.html'
    if save:
        sg()
        for titlepage in Titlepage.objects(book=book): # type: ignore
            titlepage.html_path = html_path
            titlepage.save()
            log.debug(f"Saved Book {book}'s titlepage to MongoDB. HTML path:<code>\n{html_path}</code>")
    return html_path


def get_html_path(book: int):
    sg()
    titlepage = Titlepage.objects(book=book).first()
    if titlepage is None:
        raise TitlepageNotFound(f"Titlepage for Book {book} not found.")
    return titlepage.html_path



def generate_md(book: int, save: bool = False, write = False) -> str:
    '''
    Genereate the markdown for the given book's titlepage.

    Args:
        `book` (int):
            the given book
        `save` (bool, optional):
            Whether to save the titlepage markdown to MongoDB. Defaults to False.
        `write` (bool, optional):
            Whether to write the titlepage's markdown to disk. Defaults to False.
    Returns:
        `md` (str):
            The markdown.
    '''
    book_str = str(book).zfill(2)
    sg()
    titlepage = Titlepage.objects(book=book).first()
    if titlepage is None:
        raise TitlepageNotFound(f"Titlepage for book {book} not found.")
    else:
        title = titlepage.title
        text = titlepage.text
        book_word = titlepage.book_word

        img = f'<figure>\n\t<img class="titlepage" src="../Images/gem.gif" alt="gem" />\n</figure>\n'

        meta = f"---\nTitle: {title}\nBook: {book}\nCSS: ../Styles/styles.css\nviewport: width=device-width, initial-scale=1.0\n..."

        atx = f'\n# {title}\n<br />\n### Book {book_word}<br />{img}\n'

        TEXT = '<p class="title">Written by Twelve Winged Dark Seraphim</p>\n<p class="title">Complied and Edited by Max Ludden</p>'

        md = f'{meta}{atx}\n{TEXT}'

        titlepage.filename = generate_filename(book)
        log.debug(f'Generated titlepage file for book {book}.')

        titlepage.md_path = generate_md_path(book)
        log.debug(f'Genrated titlepage filepath for book {book}.')

        titlepage.html_path = generate_html_path(book)

        if save:
            titlepage.md = md
            titlepage.save()
            log.debug(f'Saved titlepage markdown for book {book}.')

        if write:
            with open(titlepage.md_path, 'w') as f:
                f.write(md)
                log.debug(f'Wrote titlepage markdown for book {book} to disk.')

        return md


def get_md(book: int):
    sg()
    titlepage = Titlepage.objects(book=book).first()
    if titlepage is None:
        raise TitlepageNotFound(f"Titlepage for book {book} not found.")
    return titlepage.md


def log_paths(book: int, titlepage: Titlepage, mmd_cmd: list[str]) -> None:
    '''
    Logs the md_path, html_path, and mmd shell coommand.

    Raises:
        `TitlepageNotFound` (exception)
             Unable to locate the give book.
    '''
    sg()
    titlepage = Titlepage.objects(book=int(book)).first()
    log.info (f"Titlepage MD Path:\n{titlepage.md_path}")
    log.info (f"Titlepage HTML Path:\n{titlepage.html_path}")
    log.info(f"Running multimarkdown command:\n{mmd_cmd}")


def generate_html(book: int, save: bool = False, test: bool = False) -> str:
    '''
    Generate the html for the given book's titlepage.

    Args:
        `book` (int):
            The given book
        `save` (bool, optional):
            Whether to save the html to MongoDB. Defaults to False.

    Returns:
        `html` (str):
            The html for the given book's titlepage.
    '''
    sg()
    titlepage = Titlepage.objects(book=book).first()
    if titlepage is None:
        raise TitlepageNotFound(f"Titlepage for book {book} not found.")
    else:
        with open (titlepage.md_path, 'w') as f:
            f.write(titlepage.md)


        #> Multimarkdown Shell Command
        mmd_cmd = [
            "multimarkdown",
            "-f",
            "--nolabels",
            "-o",
            f"{titlepage.html_path}",
            f"{titlepage.md_path}",
        ]
        if test: #> log paths
            log_paths(book, titlepage, mmd_cmd)

        #> Try the conversion command
        try:
            result = run(mmd_cmd)
            if result.returncode == 0:
                log.info(f"Book {book}'s Multimarkdown has been converted to HTML successfully.")
        except MMDConversionException as MMD:
            log.error (f"Titlepage MD Path:<code>\n{titlepage.md_path}</code>")
            log.error (f"Titlepage HTML Path:<code>\n{titlepage.html_path}</code>")
            log.error(f"Running multimarkdown command:<code>\n{mmd_cmd}</code>")
            raise MMD(f"Multimarkdown command failed with return code {result.returncode}.")

        else:
            #> Read the HTML file
            with open (titlepage.html_path, 'r') as f:
                html = f.read()

            if save:
                titlepage.html = html
                titlepage.save()

            return html



def generate_titlepages():
    with alive_bar(30, title=f'Generating Titlepages', bar='smooth', dual_line=True) as tbar:
        for book in range(1,11):
            sg()
            titlepage = Titlepage.objects(book=book).first()
            if titlepage is None:
                raise TitlepageNotFound(f"Titlepage for book {book} not found.")
            else:
                md = generate_md(book, save=True, write=True)
                tbar()
                tbar.text(f"\tGenerating HTML")
                html = generate_html(book, save=True)
                tbar()
                tbar.text(f"\tGenerating Markdown")
                if book<27:
                    next_book = book + 1
                    tbar()
                    tbar.title(f"Book {next_book}")
                else:
                    tbar()
                    tbar.title(f"Generated all titlepages.")
