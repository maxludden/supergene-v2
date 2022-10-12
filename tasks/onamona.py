import re
import sys
from pathlib import Path
from alive_progress import alive_bar
from rich import print
from rich.text import Text
from rich.panel import Panel
from rich.progress import Progress

from src.chapter import Chapter, generate_text_path
from src.log import console, log, BASE
from src.atlas import sg

words = [
    "Bam!",
    "Beep!",
    "Bang!",
    "Boom!",
    "Blast!",
    "Crash!",
    "Clash!",
    "Clunk!",
    "Crunch!",
    "Crack!",
    "Clap!",
    "Clang!",
    "Clank!",
    "Clatter!",
    "Clink!",
    "Clump!",
    "Clunk!",
    "Ding!",
    "Dink!",
    "Hiss!",
    "Hss!",
    "Hsss!",
    "Hssss!",
    "Pow!",
    "Pop!",
    "Poof!",
    'Roar!',
    "Smack!",
    "Slam!",
    "Smash!",
    "Slap!",
    "Snap!",
    "Splat!",
    "Splash!",
    "Screech!",
    "Thud!",
    "Thump!",
    "Tick!",
    "Tock!",
    "Tsk!",
    "Tzt!",
    "Tzzt!",
    "Tzzzt!" "Whack!",
    "Wham!",
    "Whoosh!",
    "Whoosh! Whoosh! Whoosh!",
    "Zap!",
    "Zing!",
]
sg()
with Progress(console=console) as progress:
    onamona = progress.add_task("[white]Processing", total=3460)

    regex1 = re.compile(r"^((?P<html1><i>)(?P<ona>.*?)(?P<html2></i>))$", re.MULTILINE)
    subst = "*\\g<ona>*"
    regex2 = re.compile(r"^(?P<ona>\w*!)$", re.MULTILINE)
    count = 0
    for doc in Chapter.objects():  # type: ignore
        if doc:
            edited = False
            result = re.sub(regex1, subst, doc.text, 0)
            if result:
                doc.text = result
                edited = True
            for word in words:
                if word in doc.text:
                    if not f"**{word}**" in doc.text:
                        edited = True
                        doc.text = doc.text.replace(word, f"*{word}*")
                if f"**{word}**" in doc.text:
                    edited = True
                    doc.text = doc.text.replace(f"**{word}**", f"*{word}*")
            if not edited:
                result = re.sub(regex2, subst, doc.text, 0)
                if result:
                    doc.text = result
                    edited = True

            if edited:
                count += 1
                doc.save()
                text_path = doc.text_path
                with open(text_path, "w") as f:
                    f.write(doc.text)
                console.log(
                    Panel(
                        Text(
                            f"Italicized onomonapia in Chapter {doc.chapter}. Updated MongoDB and text file.",
                            justify="left",
                            style="white",
                        ),
                        title=Text(f"Italicized Onomonapia", style="bold green"),
                        title_align="left",
                        expand=False,
                        border_style="green",
                    )
                )
        progress.advance(onamona)

    panel = Panel(
        Text(f"Updated {count} chapters", style="bold white"),
        title=Text("Onomonapia", style="bold green"),
        title_align="left",
        expand=False,
        border_style="green",
    )
    console.print(panel)
