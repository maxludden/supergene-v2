# tasks/section.py
from pathlib import Path
from functools import wraps

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
    generate_section_chapters,  # type: ignore
    generate_section_part,
    generate_section_part_word,
    generate_section_md,
    generate_section_html,
)

key = Style(color="#5f00ff", italic=True)
value = Style(color="#eed4fc", bold=True)
title = Style(color="#8e47ff", bold=True)


def finished(task: str) -> Panel:
    return Panel(
        "[#00ff00]Finished[/#00ff00]",
        title=Text(f"Section {task}", style=Style(color="bright_green")),
        title_align="left",
        border_style="green",
        expand=False,
    )


def generate_section_starts():
    """Generate section Starts."""
    with Progress(console=console) as progress:
        task = progress.add_task("[bold green]Generating Section Starts...", total=17)

        for section in range(1, 18):
            sg()
            doc = Section.objects(section=section).first()  # type: ignore
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

        for section in range(1, 18):
            sg()
            doc = Section.objects(section=section).first()  # type: ignore
            if doc:
                doc.end = generate_section_end(section)
                doc.save()
                progress.update(task, advance=1)


def generate_section_titles():
    """Generate section Titles."""
    with Progress(console=console) as progress:
        task = progress.add_task("[bold green]Generating Section Titles...", total=17)

        for section in range(1, 18):
            sg()
            doc = Section.objects(section=section).first()  # type: ignore
            if doc:
                doc.title = generate_section_title(section)
                doc.save()
                progress.update(task, advance=1)


def generate_section_filenames():
    """Generate section Filenames."""
    with Progress(console=console) as progress:
        task = progress.add_task(
            "[bold green]Generating Section Filenames...", total=17
        )

        for section in range(1, 18):
            sg()
            doc = Section.objects(section=section).first()  # type: ignore
            if doc:
                doc.filename = generate_section_filename(section)
                doc.save()
                progress.update(task, advance=1)
        console.print(finished("Filenames"))


# generate_section_filenames()


def generate_section_md_paths():
    """Generate section Markdown Paths."""
    with Progress(console=console) as progress:
        task = progress.add_task(
            "[bold green]Generating Section Markdown Paths...", total=17
        )

        for section in range(1, 18):
            sg()
            doc = Section.objects(section=section).first()  # type: ignore
            if doc:
                doc.md_path = str(generate_section_md_path(section))
                doc.save()
                progress.update(task, advance=1)
        console.print(finished("Markdown Paths"))


# generate_section_md_paths()


def generate_section_html_paths():
    """Generate section HTML Paths."""
    with Progress(console=console) as progress:
        task = progress.add_task(
            "[bold green]Generating Section HTML Paths...", total=17
        )

        for section in range(1, 18):
            sg()
            doc = Section.objects(section=section).first()  # type: ignore
            if doc:
                doc.html_path = str(generate_section_html_path(section))
                doc.save()
                progress.update(task, advance=1)
        console.print(finished("HTML Paths"))


# generate_section_html_paths()


def generate_sections_chapters():
    """Generate section Chapters."""
    with Progress(console=console) as progress:
        task = progress.add_task("[bold green]Generating Section Chapters...", total=17)

        for section in range(1, 18):
            sg()
            doc = Section.objects(section=section).first()  # type: ignore
            if doc:
                doc.chapters = generate_section_chapters(section)
                doc.save()
                progress.update(task, advance=1)
        console.print(finished("Chapters"))


# generate_sections_chapters()


def generate_section_parts():
    """Generate section Parts."""
    with Progress(console=console) as progress:
        task = progress.add_task("[bold green]Generating Section Parts...", total=17)

        for section in range(1, 18):
            sg()
            doc = Section.objects(section=section).first()  # type: ignore
            if doc:
                doc.part = generate_section_part(section)
                doc.save()
                progress.update(task, advance=1)
        console.print(finished("Parts"))


# generate_section_parts()


def generate_section_part_words():
    """Generate section Part Words."""
    with Progress(console=console) as progress:
        task = progress.add_task(
            "[bold green]Generating Section Part Words...", total=17
        )

        for section in range(1, 18):
            sg()
            doc = Section.objects(section=section).first()  # type: ignore
            if doc:
                doc.part_word = generate_section_part_word(section)
                doc.save()
                progress.update(task, advance=1)
        console.print(finished("Part Words"))


# generate_section_part_words()


def generate_section_markdown():
    """Generate section Markdown."""
    with Progress(console=console) as progress:
        task = progress.add_task("[bold green]Generating Section Markdown...", total=17)

        for section in range(1, 18):
            sg()
            doc = Section.objects(section=section).first()  # type: ignore
            if doc:
                doc.markdown = generate_section_md(section)
                doc.save()
                progress.update(task, advance=1)
        console.print(finished("Markdown"))


generate_section_markdown()


def generate_section_htmls():
    """Generate section HTML."""
    with Progress(console=console) as progress:
        task = progress.add_task("[bold green]Generating Section HTML...", total=17)

        for section in range(1, 18):
            sg()
            doc = Section.objects(section=section).first()  # type: ignore
            if doc:
                doc.html = generate_section_html(section)
                footer = """ 	<div class="footer">
		<h3>Written by Twelve Winged Dark Seraphim</h3>

		<h3>Formatted and Edited by Max Ludden</h3>
	</div>"""
                doc.html = str(doc.html).replace("<p>FOOTER</p>", footer)
                doc.save()
                with open(doc.html_path, "w") as f:
                    f.write(doc.html)
                progress.update(task, advance=1)
        console.print(finished("HTML"))


generate_section_htmls()
