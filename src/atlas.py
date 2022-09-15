# src/atlas.py

import os
import re
from pathlib import Path
from platform import platform
from typing import Optional
from urllib.request import urlopen

from dotenv import dotenv_values, load_dotenv
import mongoengine
from mongoengine import connect
from pymongo.errors import ConnectionFailure
from rich import print
from rich.panel import Panel
from rich.style import Style
from rich.text import Text

try:
    from log import log, console
except ModuleNotFoundError:
    from .log import log, console
except ImportError:
    from src.log import log, console

load_dotenv()

# > BASE
def generate_base():
    """Generate base directory for the project."""
    BASE = Path.cwd()
    return BASE


BASE = generate_base()

# > Database
def generate_db_uri(database: str) -> str:
    """Generate the connection URI for the given database."""
    db_lower = database.lower()
    match db_lower:
        case "localdb":
            return "mongodb://localhost:27017/SUPERGENE"
        case "supergene":
            return str(os.environ.get("SUPERGENE"))
        case "make_supergene":
            return str(os.environ.get("MAKE_SUPERGENE"))
        case _:
            return "mongodb://localhost:27017/supergene"


@log.catch
def sg(db: str = "LOCALDB"):
    """
    Connect to the given MongoDB.

    Args:
        `db` (str, optional): The database to which you like to connect. Defaults to "LOCALDB".
    """
    mongoengine.disconnect()  # type: ignore

    # > URI
    uri = generate_db_uri(db)

    # > Connect
    try:
        connect(db="SUPERGENE", host=uri)
        # success_panel = Panel(
        #     Text(f"Connected to MongoDB:{db}", style="bold white"),
        #     title=Text("MongoDB", style="bold white"),
        #     title_align="left",
        #     style=Style(color="green"),
        # )
        # console.print(success_panel)
    except ConnectionFailure as cf:
        error_panel = Panel(
            Text(f"Connection to MongoDB:{db} failed", style="bold red on white"),
            title=Text("MongoDB", style="bold red on white"),
            title_align="left",
            style=Style(color="bold white on black"),
        )
        console.print(error_panel)
        console.print(cf)


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
