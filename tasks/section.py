# tasks/section.py
from pathlib import Path

from rich import inspect, print
from rich.panel import Panel
from rich.progress import Progress
from rich.text import Text
from rich.style import Style
from rich.markdown import Markdown
from src.atlas import sg
from src.chapter import Chapter
from src.log import BASE, console, log, logpanel
from src.section import (
    Section,
    generate_section_start,
    generate_section_end,
    generate_section_title,
    generate_section_filename,
    generate_section_md_path,
    generate_section_html_path,
    generate_section_chapters,
    generate_section_part,
    generate_section_part_word,
    generate_section_md,
    generate_section_html,
)
key = Style(color = '#5f00ff', italic=True)
value = Style(color = "#eed4fc", bold=True)
title = Style(color = "#8e47ff", bold=True)


def generate_section_starts():
    """Generate section Starts."""
    with Progress(console=console) as progress:
        task = progress.add_task("[bold green]Generating Section Starts...", total=17)

        for section in range(1,18):
            sg()
            doc = Section.objects(section=section).first() # type: ignore
            if doc:
                doc.start = generate_section_start(section)
                doc.save()
                progress.update(task, advance=1)
    console.print(
        Panel(
            Text("Generated Section's Starting Chapters", style="value"),
            title=Text("Generated Section Start", style="title"),
            title_align="left",
            border_style="key",
        )
    )

def generate_section_ends():
    """Generate section Ends."""
    with Progress(console=console) as progress:
        task = progress.add_task("[bold green]Generating Section Ends...", total=17)

        for section in range(1,18):
            sg()
            doc = Section.objects(section=section).first() # type: ignore
            if doc:
                doc.end = generate_section_end(section)
                doc.save()
                progress.update(task, advance=1)

def generate_section_titles():
    """Generate section Titles."""
    with Progress(console=console) as progress:
        task = progress.add_task("[bold green]Generating Section Titles...", total=17)

        for section in range(1,18):
            sg()
            doc = Section.objects(section=section).first() # type: ignore
            if doc:
                doc.title = generate_section_title(section)
                doc.save()
                progress.update(task, advance=1)


if __name__ == "__main__":
    generate_section_titles()
    console.print(
        Panel(
            Text("Generated Section's Values", style="value"),
            title=Text("Generated Section's Values", style="title"),
            title_align="left",
            border_style="key",
        )
    )
