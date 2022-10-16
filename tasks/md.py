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

with Progress(console=console, transient=True) as progress:
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
                        f"[bold bright_white]]enerated markdown for[/] [purple1]Chapter {doc.chapter}[/][bold bright_white]. Updated MongoDB.[/]",
                        title = f"[bold bright_magenta]Chapter {doc.chapter}[/]",
                        title_align="left",
                        expand=True,
                        width = 100,
                        border_style="#fa9ff4",
                    )
                )
                log.debug(f"Wrote markdown for Chapter {doc.chapter}. Updated MongoDB.")
            except:
                raise MarkdownGenerationError(f"Unable to create markdown for  {doc.chapter}.")
        else:
            raise ChapterNotFound(f"Chapter {doc.chapter} not found.")
        progress.advance(markdown)