from pathlib import Path

from rich import print
from rich.panel import Panel
from rich.progress import Progress
from rich.text import Text

from src.chapter import Chapter, generate_text_path
from src.log import console, log, BASE
from src.atlas import sg

sg()
with Progress(console=console, expand=True) as progress:
    line_rule = progress.add_task("[white]Processing", total=3460)

    for doc in Chapter.objects():  # type: ignore
        text_path = Path(doc.text_path)
        with open(text_path, "r") as infile:
            text = infile.read()
        if "\n...\n" in text:
            text = text.replace("\n...\n", "\n<br>\n\n*****\n\n<br>\n")
            doc.text = text
            doc.save()
            with open(text_path, "w") as outfile:
                outfile.write(text)
            console.log(
                Panel(
                    Text(
                        f"Added rule to Chapter {doc.chapter}. Updated MongoDB and text file.",
                        justify="left",
                        style="white",
                    ),
                    title=Text(f"Added Horizontal Rule", style="bold green"),
                    title_align="left",
                    expand=False,
                    border_style="green",
                )
            )
        if "\n…\n" in text:
            text = text.replace("\n…\n", "\n<br>\n\n*****\n\n<br>\n")
            doc.text = text
            doc.save()
            with open(text_path, "w") as outfile:
                outfile.write(text)
            console.log(
                Panel(
                    Text(
                        f"Added rule to Chapter {doc.chapter}. Updated MongoDB and text file.",
                        justify="left",
                        style="white",
                    ),
                    title=Text(f"Added Horizontal Rule", style="bold green"),
                    title_align="left",
                    expand=False,
                    border_style="green",
                )
            )
        progress.advance(line_rule)
