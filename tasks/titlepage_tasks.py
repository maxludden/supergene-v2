# tasks/titlepage_tasks.py

from pathlib import Path

from rich import inspect, print
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress
from rich.style import Style
from rich.text import Text
from sh import Command, RunningCommand
from src.atlas import sg
from src.log import BASE, console, log, logpanel
from src.titlepage import (
    Titlepage,
    generate_titlepage_book_word,
    generate_titlepage_filename,
    generate_titlepage_html,
    generate_titlepage_html_path,
    generate_titlepage_md,
    generate_titlepage_md_path,
)
