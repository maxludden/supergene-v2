from pathlib import Path

from rich import print
from rich.panel import Panel
from rich.progress import Progress
from rich.text import Text
from sh import Command
from src.atlas import sg
from src.chapter import Chapter, chapter_gen, get_book
from src.log import BASE, console, log

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from functools import partial
from itertools import chain
from multiprocessing import Pool, Process, Queue, cpu_count

import src.chapter as chapter
from time import perf_counter


class HTMLGenerationError(Exception):
    pass


class ChapterNotFound(Exception):
    pass


class HtmlProgress(Progress):
    def get_renderables(self):
        yield Panel(self.make_tasks_table(self.tasks))


chapters = chapter_gen()


def generate_filename(chapter: int) -> str:
    return f"chapter-{str(chapter).zfill(4)}"


def generate_md_path(chapter: int) -> Path:
    BASE = Path.cwd()
    book = get_book(chapter)
    book_zfill = str(book).zfill(2)
    book_dir = f"book{book_zfill}"
    filename = generate_filename(chapter)
    return BASE / "books" / book_dir / "md" / f"{filename}.md"


def generate_html_path(chapter: int) -> Path:
    BASE = Path.cwd()
    book = get_book(chapter)
    book_zfill = str(book).zfill(2)
    book_dir = f"book{book_zfill}"
    filename = generate_filename(chapter)
    return BASE / "books" / book_dir / "html" / f"{filename}.html"


def generate_html(chapter: int, save: bool = True):
    start = perf_counter()
    sg()
    doc = Chapter.objects(chapter=chapter).first()  # type: ignore
    if doc:
        html_path = generate_html_path(doc.chapter)
        md_path = generate_md_path(doc.chapter)
        log.debug(f"Generating HTML for Chapter {doc.chapter}.")

        if md_path.exists():
            multimarkdown = Command("multimarkdown")
            mmd = multimarkdown.bake(
                "-f",
                "--nolabels",
                "-o",
            )
            result = mmd(html_path, md_path)
            if result.exit_code == 0:  # type: ignore
                log.debug(f"Successfully generated HTML for doc {doc.chapter}.")
                if save:
                    sg()
                    doc = Chapter.objects(chapter=chapter).first()  # type: ignore
                    with open(html_path, "r") as infile:
                        doc.html = infile.read()
                        log.debug(f"Saved Chapter {doc.chapter}'s HTML to MongoDB.")
            else:
                log.error(f"Error generating HTML for doc {doc.chapter}.")
                raise HTMLGenerationError(
                    f"Error generating HTML for doc {doc.chapter}."
                )
        else:
            log.error(f"Markdown file not found for doc {doc.chapter}.")
            raise ChapterNotFound(f"Markdown file not found for doc {doc.chapter}.")
    else:
        log.error(f"Chapter {doc.chapter} not found.")
        raise ChapterNotFound(f"Chapter {doc.chapter} not found.")
    end = perf_counter()
    duration = end - start
    log.debug(
        f"Generated HTML for Chapter {doc.chapter} in {end - start:0.4f} seconds."
    )
    return duration


if __name__ == "__main__":
    start = perf_counter()
    durations = []
    with Progress(console=console) as progress:
        task = progress.add_task("Generating HTML...", total=3462)
        with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
            futures = [executor.submit(generate_html, chapter) for chapter in chapters]
            for future in as_completed(futures):
                progress.advance(task)
    end = perf_counter()
    total_duration = end - start
    sum = sum(durations)
    avg = sum / 3462
    msg = f"Generated HTML for all chapters in {end - start:0.4f} seconds. Average time per chapter: {avg:0.6f} seconds."
    console.log(
        Panel(
            Text(msg, justify="left", style="white"),
            title=Text(f"Generated Chapter HTML", style="bold green"),
            title_align="left",
            expand=False,
            border_style="#00ff00",
        )
    )
    log.debug(msg)
