# task/pandoc.py
from inspect import currentframe, getframeinfo
from pathlib import Path
from concurrent.futures import (ProcessPoolExecutor, ThreadPoolExecutor,
                                as_completed)
from multiprocessing import cpu_count

from rich import print
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.table import Table, Column
from rich.style import Style
from sh import Command, ErrorReturnCode, RunningCommand
from src.log import log, console

BASE = Path.cwd()
pandoc = Command("pandoc")
pandoc = pandoc.bake("--css", "style.css")
cd = Command("cd")
cp = Command("cp")

books = {
    1: "1 - First God's Sanctuary.epub",
    2: "2 - Second God's Sanctuary.epub",
    3: "3 - Third God's Sanctuary.epub",
    4: "4 - Fourth and Fifth God's Sanctuary.epub",
    5: "5 - Planet Kate and Narrow Moon.epub",
    6: "6 - Sky Palace, Blade, and Eclipse.epub",
    7: "7 - The Ice Blue Knights and The Extreme Kings.epub",
    8: "8 - The Systems of Chaos and The Very High.epub",
    9: "9 - Meeting God and Fighting Sacred.epub",
    10: "10 - The Universe of Kingdoms and Quin Kiu.epub",
}

book_numbers = list(books.keys())

text_column = TextColumn("[progress.description]{task.description}")
spinner_column = SpinnerColumn()
bar_column = BarColumn(
    bar_width=None, finished_style="green", table_column=Column(ratio=3)
)
mofn_column = MofNCompleteColumn()
time_elapsed_column = TimeElapsedColumn()
time_remaining_column = TimeRemainingColumn()

progress = Progress(
    text_column,
    spinner_column,
    bar_column,
    mofn_column,
    time_elapsed_column,
    time_remaining_column,
    console=console,
    transient=True,
    refresh_per_second=10,
    auto_refresh=True,
)

def create_books(book: int) -> Panel:
    book_zfill = str(book).zfill(2)
    cd(BASE / "books" / f"book{book_zfill}" / "html")
    pandoc("-d", f"sg{book}")

    file = books[book]
    destination = BASE / "books" / file
    cp(file, destination)


    panel = Panel(
            f"[bold bright_white]Created {file}[/bold bright_white]",
            title=f"[bold purple1]Book {book}[/bold purple1]",
            title_align="left",
            border_style=Style(color="#e8affb", bold=True),
            expand=True,
            width=80,
        )
    return panel


if __name__ == "__main__":
    with progress:
        task = progress.add_task("Creating Books...", total=10)

        for book in book_numbers:
            with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
                futures = [executor.submit(create_books, book) for book in book_numbers]

                for future in as_completed(futures):
                    console.print(f"Updated Chapter {future.result()}.")
                    progress.advance(task)
