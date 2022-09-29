# src/max_rich.py
from rich import inspect, print
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress
from rich.style import Style
from rich.table import Table
from rich.text import Text
from rich.theme import Theme
from rich.traceback import install
from rich.tree import Tree
from inspect import FrameInfo, stack
from pathlib import Path


def get_filepath(frame: int = 1) -> str:
    frame += 1
    return stack(context=-1)[frame].filename


def get_lineno(frame: int = 1) -> int:
    return stack(context=-1)[frame].lineno


def get_filename(frame: int = 1) -> str:
    return Path(get_filepath(frame)).name


def gen_panel(stack: FrameInfo = stack(context=-1)[0]):
    file = stack.filename
    line = stack.lineno
    panel = Panel(
        f"Lorum ipsum dolor sit amet",
        title="Current File & Line",
        title_align="left",
        border_style="#00FF00",
        expand=False,
        subtitle=f"[purple]{file}[/][#FFFFFF]|[/][#54c6ff]line {line}[/]",
    )


stack(context=-1)[0].lineno  # type: ignore

inspect(stack(context=-1))
