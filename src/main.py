from os import environ
from pathlib import Path

import ujson as json
from mongoengine import ValidationError
from src.max_rich import *

import src.myaml as yaml
from atlas import sg

from log import BASE, console, log
from rich import inspect as rinspect
from inspect import stack


def gen_panel(content: str = "Sample text for a panel", file: str = get_filename(0), line: int = get_lineno(0)) -> Panel:
    panel =  Panel(
        f"[italic bright_white]{content}[/italic bright_white]",
        title="",
        title_align="left",
        border_style="blue",
        expand=False,
        subtitle=f"[purple]{file}[/][#FFFFFF]|[/][#54c6ff]line {line}[/]",
    )
    return panel


print(gen_panel())
