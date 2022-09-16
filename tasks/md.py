from pathlib import Path
from rich import print
from rich.panel import Panel
from rich.progress import Progress
from rich.text import Text
from sh import Command
from src.atlas import sg
from src.chapter import Chapter, get_md_path, generate_md
from src.log import BASE, console, log
import src.chapter as chapter

class MarkdownGenerationError(Exception):
    pass
class ChapterNotFound(Exception):
    pass

with Progress(console=console) as progress:
    markdown = progress.add_task("Generating markdown...", total=3460)

    chapters = chapter.chapter_gen()
    for ch in chapters:
        sg()
        doc = Chapter.objects(chapter=ch).first() # type: ignore
        if doc:
            md_path = Path(str(get_md_path(int(doc))))
            try:
                md = str(generate_md(doc.chapter, save=True, write=True))
                doc.md = md
                doc.save()

                with open(md_path, "w") as outfile:
                    outfile.write(md)

                console.log(
                    Panel(
                        Text(
                            f"Generated markdown for doc {doc.chapter}. Updated MongoDB.",
                            justify="left",
                            style="white",
                        ),
                        title=Text(
                            f"Generate Markdown",
                            style="bold green"
                        ),
                        title_align="left",
                        expand=False,
                        border_style="#00ff00",
                    )
                )
                log.debug(f"Read markdown for Chapter {doc.chapter}. Updated MongoDB.")
            except:
                raise MarkdownGenerationError(f"Unable to create markdown for  {doc.chapter}.")
        else:
            raise ChapterNotFound(f"Chapter {doc.chapter} not found.")
        progress.advance(markdown)