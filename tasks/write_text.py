from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count

from rich import print
from rich.panel import Panel
from maxcolor import console, log, progress
from src.chapter import Chapter, chapter_gen
from src.atlas import sg


def write_text(chapter: int) -> int:
    """
    Writes the given chapter's text to a file.

    Args:
        `chapter` (int):
            The given chapter.
    """
    sg()
    doc = Chapter.objects(chapter=chapter).first()  # type: ignore
    path = Path(doc.text_path)
    if path.exists():
        with open(path, "w") as outfile:
            outfile.write(doc.text)
    return chapter


if __name__ == "__main__":
    chapters = chapter_gen()
    with progress:
        task = progress.add_task("Writing Chapter Text...", total=3460)
        with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
            futures = [executor.submit(write_text, chapter) for chapter in chapters]
            for future in as_completed(futures):
                progress.advance(task)
                chapter = future.result()
                console.print(
                    Panel(
                        f"[bold bright_white]Chapter [/][bold purple1]{chapter} [/][bold bright_white]written to file.[/]",
                        title="[bold bright_magenta]Write Text[/]",
                        title_align="left",
                        border_style="bright_magenta",
                        expand=True,
                        width=100,
                    ),
                    highlight=True,
                )
