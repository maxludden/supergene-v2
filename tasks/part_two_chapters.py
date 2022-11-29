from rich import print
from rich.prompt import IntPrompt, PromptError
from maxconsole import get_theme, get_console
from maxprogress import get_progress
from maxcolor import gradient_panel, gradient
from rich.columns import Columns
from src.chapter import Chapter, chapter_gen, get_filename
from src.section import Section
from src.atlas import sg
from maxsetup import new_run

console = get_console(get_theme())
progress = get_progress(console)
run = new_run(console)


def print_section_chapters(section: int):
    sg()
    """Print the chapters in the current section."""
    section = Section.objects(section=section).first()
    chapters = section.chapters
    book = section.book
    chapter_list = ""
    resource_path = ""
    for chapter in chapters:
        chapter_list = f"{chapter_list}  - chapter-{str(chapter).zfill(4)}.html\n"
        resource_path = (
            f"{resource_path}  - ${{.}}/html/chapter-{str(chapter).zfill(4)}.html\n"
        )
    console.print(
        gradient(
            f"Book {book} - Chapters in Section {section.section}\n\n{chapter_list}\n\n\n{resource_path}",
        ),
        justify="left",
    )


# beginning = 1822
# end = 1960
# total = end - beginning + 1

# chapters = []
# for x in range(total):
#     chapter = beginning + x
#     chapter_string = str(chapter).zfill(4)

#     chapters.append(chapter_string)

# for chapter in chapters:
#     console.print(gradient(f"  - chapter-{chapter}.html"))


print_section_chapters(section=17)
