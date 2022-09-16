from os import environ
from pathlib import Path

from rich import inspect, print
from rich.markdown import Markdown
from rich.style import Style
from rich.text import Text
from rich.panel import Panel
from rich.theme import Theme
from mongoengine import connect, ValidationError
from tqdm.auto import tqdm
import ujson
from alive_progress import alive_bar

from atlas import sg
from chapter import (
    Chapter,
    chapter_gen,
    generate_md_path,
    generate_html_path,
    generate_text_path,
    generate_md,
    generate_html,
)
from log import console, log
from myaml import dump, load, safe_dump, safe_load

sg()
doc = Chapter.objects(chapter=1).first() # type: ignore
text_path = generate_text_path(doc.chapter)
md_path = generate_md_path(doc.chapter)
with open (text_path, 'r') as infile:
    text = infile.read()

doc.text = text
doc.save()

md = str(generate_md(doc.chapter, save=True, write=True))
doc.md = md
doc.save()

with open(md_path, "w") as outfile:
    outfile.write(md)

console.log(
    Panel(
        Text(
            f"Generated markdown for doc {doc.chapter}. Updated MongoDB.",
            justify="left",
            style="white",
        ),
        title=Text(
            f"Generate Markdown",
            style="bold green"
        ),
        title_align="left",
        expand=False,
        border_style="#00ff00",
    )
)