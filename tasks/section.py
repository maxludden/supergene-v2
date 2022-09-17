# tasks/section.py
from pathlib import Path

from rich import inspect, print
from rich.panel import Panel
from rich.progress import Progress
from rich.text import Text
from rich.markdown import Markdown
from src.atlas import sg
from src.chapter import Chapter
from src.log import BASE, console, log, logpanel
from src.section import Section, generate_section_start, generate_section_end, generate_section_title, generate_section_filename, generate_section_md_path, generate_section_html_path, generate_section_chapters, generate_section_part, generate_section_part_word, generate_section_md, generate_section_html

def generate_section_values() -> None:
    """
    Generate the values for the section.
    """
    with Progress(console=console) as progress:
        generate_section_starts = progress.add_task(
            "[bold green]Generating Section's Start...", total=17
        )
        generate_section_ends = progress.add_task(
            "[bold green]Generating Section's End...", total=17
        )
        generate_section_titles = progress.add_task(
            "[bold green]Generating Section's Title...", total=17
        )
        generate_section_filenames = progress.add_task(
            "[bold green]Generating Section's Filename...", total=17
        )
        generate_md_paths = progress.add_task(
            "[bold green]Generating Section's Markdown Path...", total=17
        )
        generate_html_paths = progress.add_task(
            "[bold green]Generating Section's HTML Path...", total=17
        )
        generate_section_chapters = progress.add_task(
            "[bold green]Generating Section's Chapters...", total=17
        )
        generate_section_parts = progress.add_task(
            "[bold green]Generating Section's Parts...", total=17
        )
        generate_section_part_words = progress.add_task(
            "[bold green]Generating Section's Part Words...", total=17
        )
        generate_mds = progress.add_task(
            "[bold green]Generating Section's Markdown...", total=17
        )
        generate_section_htmls = progress.add_task(
            "[bold green]Generating Section's HTML...", total=17
        )
        regenerate_sections = progress.add_task(
            "[bold green]Regenerating Sections...", total=17
        )

        for section in range(1, 18):
            sg()
            doc = Section.objects(section=section).first()  # type: ignore
            doc.start = generate_section_start(section) # type: ignore
            progress.advance(generate_section_starts)
            doc.end = generate_section_end(section) # type: ignore
            progress.advance(generate_section_ends)
            doc.title = generate_section_title(section) # type: ignore
            progress.advance(generate_section_titles)
            doc.filename = generate_section_filename(section) # type: ignore
            progress.advance(generate_section_filenames)
            doc.md_path = generate_section_md_path(section) # type: ignore
            progress.advance(generate_md_paths)
            doc.html_path = generate_section_html_path(section) # type: ignore
            progress.advance(generate_html_paths)
            doc.chapters = generate_section_chapters(section) # type: ignore
            progress.advance(generate_section_chapters)
            doc.parts = generate_section_part(section) # type: ignore
            progress.advance(generate_section_parts)
            doc.part_words = generate_section_part_word(section) # type: ignore
            progress.advance(generate_section_part_words)
            doc.md = generate_section_md(section) # type: ignore
            progress.advance(generate_mds)
            doc.html = generate_section_html(section) # type: ignore
            progress.advance(generate_section_htmls)
            doc.save()
            progress.advance(regenerate_sections)

if __name__ == "__main__":
    generate_section_values()
    console.print(
        Panel(
            Text(
                "Generated Section's Values",
                style="value"
            ),
            title="['title']Generated Section's Values[/]",
            title_align='left',
            border_style='key',
        )
    )
