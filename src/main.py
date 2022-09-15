from os import environ
from pathlib import Path

from rich import inspect, print
from rich.markdown import Markdown
from rich.style import Style
from rich.text import Text
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
for doc in tqdm(Chapter.objects(), unit='ch', desc='Updating chapters'):# type: ignore
    if doc:
        text_path = generate_text_path(doc)
        doc.text_path = text_path
        with open (text_path, 'w') as f:
            f.write(doc.text)
        doc.save()