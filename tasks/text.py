# tasks/md.py
from pathlib import Path

from rich import print
from rich.panel import Panel
from rich.progress import Progress
from rich.text import Text
from sh import Command
from src.atlas import sg
from src.chapter import (Chapter, generate_html, generate_md, get_html_path,
                         get_md_path, get_text_path, chapter_gen)
import src.chapter as chapter
from src.log import BASE, console, log

class TextFileNotFound(Exception):
    pass

class ChapterNotFound(Exception):
    pass

class MarkdownGenerationError(Exception):
    pass


with Progress(console=console) as progress:
    read_text = progress.add_task("Reading text...", total=3460)

    chapters = chapter.chapter_gen()
    for chapter in chapters:
        sg()
        doc = Chapter.objects(chapter=chapter).first() # type: ignore
        if doc:
            text_path = Path(str(get_text_path(int(doc))))
            if text_path.exists():
                with open(text_path, "r") as f:
                    doc.text = str(f.read())
                    doc.save()
                    console.log(
                        Panel(
                            Text(
                                f"Read text for doc {doc.chapter}. Updated MongoDB.",
                                justify="left",
                                style="white",
                            ),
                            title=Text(
                                f"Reading Text",
                                style="bold green"
                            ),
                            title_align="left",
                            expand=False,
                            border_style="#00ff00",
                        )
                    )
                    log.debug(f"Read text for Chapter {doc.chapter}. Updated MongoDB.")
            else:
                raise TextFileNotFound(f"Text file not found for doc {doc.chapter}.")
        else:
            raise ChapterNotFound(f"doc {doc.chapter} not found.")

        progress.advance(read_text)
