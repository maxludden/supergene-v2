# src/atlas.py

import os
import re
from pathlib import Path
from platform import platform
from typing import Optional
from urllib.request import urlopen

from dotenv import dotenv_values, load_dotenv
from mongoengine import connect, disconnect_all
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.style import Style
from rich.text import Text

load_dotenv()
console = Console(width=80)

# > BASE
def generate_base():
    """Generate base directory for the project."""
    if platform() == "Linux":
        ROOT = "home"
    else:
        ROOT = "Users"  # < Mac
    BASE = f"/{ROOT}/maxludden/dev/py/supergene"
    return BASE

BASE = generate_base()

# > Database
def generate_db_uri(database: str) -> str:
    """Generate the connection URI for the given database."""
    db_lower = database.lower()
    match db_lower:
        case "localdb":
            return "mongodb://localhost:27017/supergene"
        case "supergene":
            return str(os.environ.get("SUPERGENE"))
        case "make_supergene":
            return str(os.environ.get("MAKE_SUPERGENE"))
        case _:
            return "mongodb://localhost:27017/supergene"

def sg(db: str="LOCALDB"):
    '''
    Connect to the given MongoDB.

    Args:
        `db` (str, optional): The database to which you like to connect. Defaults to "LOCALDB".
    '''
    console.clear()
    disconnect_all()

    # > URI
    uri = generate_db_uri(db)
    connect_panel = Panel(
        Text(f"Connecting to {db}...", style="bold white"),
        title=Text("MongoDB", style="bold white"),
        title_align="left",
        style=Style(color="blue")
    )
    console.print(connect_panel)

    # > Connect
    try:
        connect(db="supergene",alias="LOCALDB",host=uri)
        success_panel = Panel(
            Text(f"Connected to MongoDB:{db}", style="bold white"),
            title=Text("MongoDB", style="bold white"),
            title_align="left",
            style=Style(color="green")
        )
        console.print(success_panel)
    except ConnectionFailure as cf:
        error_panel = Panel(
            Text(f"Connection to MongoDB:{db} failed", style="bold red on white"),
            title=Text("MongoDB", style="bold red on white"),
            title_align="left",
            style=Style(color="bold white on black")
        )
        console.print(error_panel)
        print(cf)