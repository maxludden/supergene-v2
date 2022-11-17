# tasks/read_text.py
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
from pathlib import Path

from maxcolor import gradient_panel
from maxconsole import get_theme, get_console
from maxprogress import get_progress
from rich import print, inspect
from rich.pretty import pprint
from rich.panel import Panel
from src.atlas import sg
from src.chapter import Chapter, chapter_gen


def read_text(chapter: int) -> str:
    """
    Reads the given chapter's text from disk and saves it to MongoDB.

    Args:
        `chapter` (int):
            The given chapter.
    """
    sg()
    doc = Chapter.objects(chapter=chapter).first()  # type: ignore
    path = Path(doc.text_path)
    if path.exists():
        with open(path, "r") as infile:
            doc.text = infile.read(doc.text)
            doc.save()
    return str(chapter)


def tp_read_chapters():
    theme = get_theme()
    console = get_console(theme)
    progress = get_progress(console)

    chapters = chapter_gen()
    with progress:
        task = progress.add_task("Reading Chapter Text...", total=3460)
        with ProcessPoolExecutor(max_workers=(cpu_count() - 1)) as executor:
            futures = [executor.submit(read_text, chapter) for chapter in chapters]
            for future in as_completed(futures):
                progress.advance(task)
                pprint(future.result())


if __name__ == "__main__":
    console = get_console(get_theme())
    progress = get_progress()

    with progress:
        read_chapters = progress.add_task("Reading Chapter Text...", total=3460)
        chapters = chapter_gen()
        for chapter in chapters:
            sg()
            doc = Chapter.objects(chapter=chapter).first()  # type ignore
            with open(doc.text_path, "r") as infile:
                doc.text = infile.read()
                doc.save()
                progress.advance(read_chapters)
