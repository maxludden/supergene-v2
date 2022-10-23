from enum import IntEnum
from pathlib import Path
import time

from rich import print
from rich.panel import Panel
from rich.progress import Progress
from rich.text import Text
from src.atlas import sg
from src.cover import (
    Coverpage,
    generate_html,
    generate_html_path,
    get_html,
    get_html_path,
)
from maxcolor import console, log

choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


class InvalidBook(ValueError):
    pass


def generate_specific_cover():
    book = int(input("Which book? (1-10)"))
    if book not in choices:
        raise InvalidBook(f"Book {book} does not exist.")
    generate_html(book)


def generate_covers():
    with Progress(
        console=console,
    ) as progress:
        covers = progress.add_task("[white]Creating Covers...", total=10)

        for book in range(1, 11):
            generate_html(book)
            progress.update(covers, advance=1)


if __name__ == "__main__":
    time.sleep(5)
    book = input("Generate all volumes? (y/n)")
    match book:
        case "y" | "Y" | "yes" | "Yes":
            generate_covers()
        case "n" | "N" | "no" | "No":
            generate_specific_cover()
        case _:
            print("Invalid choice.")
