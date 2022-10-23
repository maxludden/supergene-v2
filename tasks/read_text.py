# tasks/read_text.py
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
from pathlib import Path

from maxcolor import console, gradient_panel, progress, rainbow
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


if __name__ == "__main__":
    chapters = chapter_gen()
    with progress:
        task = progress.add_task("Reading Chapter Text...", total=3460)
        with ProcessPoolExecutor(max_workers=(cpu_count()-1)) as executor:
            futures = [executor.submit(read_text, chapter) for chapter in chapters]
            for future in as_completed(futures):
                progress.advance(task)
                pprint(future.result())
