from rich import print
from maxconsole import get_theme, get_console
from maxcolor import gradient_panel, gradient
from rich.columns import Columns


console = get_console(get_theme())

beginning = 1822
end = 1960
total = end - beginning + 1

chapters = []
for x in range(total):
    chapter = beginning + x
    chapter_string = str(chapter).zfill(4)

    chapters.append(chapter_string)

for chapter in chapters:
    console.print(gradient(f"  - chapter-{chapter}.html"))
