# src/metadata.py
from pathlib import Path
from mongoengine import Document
from mongoengine.fields import IntField, StringField
from rich import print, inspect
from rich.text import Text
from rich.panel import Panel
from rich.progress import Progress


from src.atlas import max_title, sg
from src.book import Book
from src.log import BASE, console, log, logpanel
from src.myaml import load, loads, dump, dumps


class Metadata(Document):
    book = IntField()
    title = StringField()
    filename = StringField()
    filepath = StringField()
    html_path = StringField()
    text = StringField()
    meta = {'collection': 'metadata'}


def generate_meta_filename(book: int, save: bool = True):
    '''
    Generate the filename for the given book's Metadatadata.

    Args:
        `book` (int):
            The given book.

    Returns:
        `filename` (str):
            The filename for the given book's Metadatadata.
    '''
    #> Generate Filename
    filename =  f'meta{book}.yml'

    #> Update filename in MongoDB
    if save:
        sg()
        doc = Metadata.objects().first() # type: ignore
        doc.filename = filename
        doc.save()
        logpanel(f"Updated Book {book}'s Metadata's filename:\n{filename}", level='d')
    return filename


def get_meta_filename(book: int) -> str:
    '''
    Retrieve the given book's Metadata's filename from MongoDB.

    Args:
        `book` (int):
            The given book

    Returns:
        `filename` (str):
            The filename for the given book's Metadata.
    '''
    sg()
    doc = Metadata.objects(book=book).first() # type: ignore
    if doc.filename:
        logpanel(f"Retrieved Book {book}'s Metadata's filename from MongoDB.", level='d')
        return doc.filename
    else:
        filename = generate_meta_filename(book)
        logpanel(f"Generated Book {book}'s Metadata's filename: {filename}", level='d')
        return filename



def generate_meta_filepath(book: int, save: bool = True) -> Path:
    '''
    Generate filepath for the given book's metadata.

    Args:
        `book` (int):
            The given book.

    Returns:
        `filepath` (Path):
            The filepath for the given book's metadata.
    '''
    #> Generate filepath
    filename = generate_meta_filename(book)
    book_str = str(book).zfill(2)
    book_dir = f"book{book_str}"
    filepath = f"{BASE}/books/{book_dir}/yaml/{filename}"

    #> Update Filepath in MongoDB
    if save:
        sg()
        doc = Metadata.objects().first() # type: ignore
        doc.filepath = filepath
        doc.html_path = filepath
        doc.save()
        log.debug(f"Saved Book {book}' Metadata's filepath:\n{filepath}")
    return Path(filepath)


def get_meta_filepath(book: int) -> Path:
    '''
    Retrieve the filepath for the given book's Metadatadata from MongoDB.

    Args:
        `book` (int):
            The given book.

    Returns:
        `md_path` (str):
            The filepath of the given book's Metadatadata.
    '''
    sg()
    doc = Metadata.objects(book=book).first() # type: ignore
    if doc:
        logpanel(f"Retrieved Book {book}'s Metadata's filepath from MongoDB.", level='d')
        return doc.filepath
    else:
        filepath = generate_meta_filepath(book)
    return Path(filepath)


def generate_meta_title(book: int) -> str:
    '''
    Retrieve the given book's title from MongoDB.

    Args:
        `book` (int):
            The given book.

    Return:
        `title` (str):
            The title of the given book.
    '''
    #> Retrieve title from Book Collection
    sg()
    doc = Book.objects(book=book).first() # type: ignore
    title = max_title(doc.title)

    #> Update title in MongoDB
    doc = Metadata.objects().first() # type: ignore
    doc.title = title
    doc.save()

    return title


def generate_metadata(book: int, save: bool = False, write: bool = False):
    '''
    Generate the text for the given book's Metadatadata.

    Args:
        `book` (int):
            The given book.

    Return:
        `text` (str):
            The given book's Metadata's text.
    '''
    #> Retrieve Components from MongoDB
    author = 'Twelve Winged Dark Seraphim'
    sg()
    doc = Metadata.objects(book=book).first() # type: ignore
    #> Generate Text
    metadata_dict = {
        "title": doc.title,
        "author": author
    }
    metadata = dumps(metadata_dict)
    metadata_yaml = f"---\n{metadata}..."
    logpanel(f"Generated yaml text for book {book}'s Metadata.", level='d')
    inspect(metadata_yaml)

    #> Save text to MongoDB
    if save:
        doc.text = metadata_yaml
        doc.save()

    #> Write Text to Disk
    if write:
        with open(doc.filepath, 'w') as f:
            f.write(metadata_yaml)
            logpanel(f"Wrote yaml text for book {book}'s Metadata to disk.", level='d')

    return metadata_yaml


def get_meta_text(book: int) -> str:
    '''
    Retrieve the given book's metadata from MongoDB.

    Args:
        `book` (int): The given book.

    Returns:
        `metadata` (str): The metadata of the given book.
    '''
    sg()
    doc = Metadata.objects(book=book).first() # type: ignore
    if doc.text:
        logpanel(f"Retrieved Book {book}'s metadata from MongoDB.", level='d')
        return doc.text
    else:
        metadata = generate_metadata(book, save=True, write=True)
        logpanel(f"Generated Book {book}'s Metadata.", level='d')
        return metadata


def generate_all_metadata() -> None:
    '''
    Create the Metadatadata files for each book.
    '''
    with Progress(console=console, transient=True) as progress:
        write_meta = progress.add_task("[bold green]Creating Metadata...", total=12)
        for book in range(1, 11):
            sg()
            #> Generate new_metadata parameters from Book.
            doc = Metadata.objects(book=book).first() # type: ignore
            if doc.text:
                with open (doc.filepath, 'w') as outfile:
                    outfile.write(doc.text)
                    logpanel(f"Wrote Book {book}'s text to disk.", level='d')
                    progress.update(write_meta, advance=1)
            else:
                generate_metadata(book, save=True, write=True)
                progress.update(write_meta, advance=1)
        progress.update(write_meta, completed=True)
        console.log(
            Panel(
                Text(
                    "Created Metadata for all books.",
                    justify='left',
                    style='bright_white'
                ),
                title='[bold green]Success',
                border_style='#00FF00',
                padding=(1, 1),
                expand=False
            )
        )

# generate_all_metadata()