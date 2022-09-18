# tasks/update_css.py
from pathlib import Path
from typing import List
from rich import inspect, print
from rich.panel import Panel
from rich.progress import Progress
from rich.text import Text
from rich.style import Style
from rich.markdown import Markdown
from src.atlas import sg
from src.chapter import Chapter
from src.log import BASE, console, log, logpanel

def read_css() -> str:
    """Read the CSS file."""
    css_path = BASE / "styles" / "style.css"
    with open(css_path, "r") as infile:
        css = infile.read()
    return css

def generate_paths() -> List[Path]:
    """Generate paths to all style and html directories."""
    paths = []
    for book in range(1,11):
        book_zfill = str(book).zfill(2)
        book_dir = f'book{book_zfill}'
        html_path = BASE / 'books' / book_dir / 'html' / 'style.css'
        style_path = BASE / 'books' / book_dir / 'Styles' / 'style.css'
        paths.append(html_path)
        paths.append(style_path)

    console.print(
        Panel(
            '\n'.join([str(path) for path in paths]),
            title='[#00ff00]Generated Paths[/#00ff00]',
            title_align='left',
            border_style='green',
            expand=False,
            subtitle='[#589a67]tasks[/][#eaffea]/[/][#589a67]update_css[/][#eaffea].[/][#589a67]py[/]',
            subtitle_align='right'
        )
    )
    return paths

def write_css(paths: List[Path], css: str) -> None:
    """Write the CSS to the paths."""
    for path in paths:
        with open(path, 'w') as outfile:
            outfile.write(css)
    console.print(
        Panel(
            '[bright_white]Copied CSS to all style and html directories[/]',
            title='[#00ff00]Copied CSS[/#00ff00]',
            title_align='left',
            border_style='green',
            expand=False,
            subtitle='[#589a67]tasks[/][#eaffea]/[/][#589a67]update_css[/][#eaffea].[/][#589a67]py[/]',
            subtitle_align='right'
        )
    )

if __name__ == "__main__":
    css = read_css()
    paths = generate_paths()
    write_css(paths, css)
    console.print(
        Panel(
            '[bright_white]Finished copying style.css to HTML and Style Directories[/]',
            title='[#00ff00]Finished[/#00ff00]',
            title_align='left',
            border_style='green',
            expand=False,
            subtitle='[#589a67]tasks[/][#eaffea]/[/][#589a67]update_css[/][#eaffea].[/][#589a67]py[/]',
            subtitle_align='right'
        )
    )