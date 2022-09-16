from pathlib import Path
from typing import List
import re

from rich import inspect, print
from rich.panel import Panel
from rich.progress import Progress
from rich.text import Text
from src.atlas import sg
from src.chapter import Chapter, generate_text_path
from src.log import BASE, console, log

sg()
with Progress(console=console) as progress:
    add_tags = progress.add_task("[white]Adding tags", total=3460)

    table_regex = re.compile(r"<table class=\"(?P<tag>.*?)\">[\S|\s]*?</table>", re.IGNORECASE)
    blockquote_regex = re.compile(r'^>.*$', re.MULTILINE)
    for doc in Chapter.objects():  # type: ignore
        found_tag = False
        text_path = Path(doc.text_path)
        with open(text_path, "r") as infile:
            text = infile.read()
        matches = re.finditer(table_regex, text)
        if matches:
            found_tag = True
            for matchnum, match in enumerate(matches, start=1):
                tag = match.group("tag")
                doc.tags.append(tag)
                doc.save()
        matches = re.findall(blockquote_regex, text)
        if matches:
            found_tag = True
            doc.tags.append('vog')
            doc.save()
        if found_tag:
            if len(doc.tags) > 1:
                tags = str(', '.join(doc.tags))
                title = "Added Tags"
            elif len(doc.tags) == 1:
                tags = str(doc.tags[0])
                title = "Added Tag"
            console.log(
                Panel(
                    Text(
                        f"Found [cyan]{tags}[/] in Chapter {doc.chapter}. Updated MongoDB.", # type: ignore
                        justify="left",
                        style="white"
                    ),
                    title=Text(
                        f"{title}", # type: ignore
                        style="bold green",
                    ),
                    title_align="left",
                    expand=False,
                    border_style="green"
                )
            )
        progress.advance(add_tags)

with Progress(console=console) as progress:
    dedup_tags = progress.add_task("[white]De-dublicating tags", total=3460)

    for doc in Chapter.objects():  # type: ignore
        doc.tags = list(set(doc.tags))
        doc.save()
        progress.advance(dedup_tags)