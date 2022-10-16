# src/edit.py
import re
from concurrent.futures import (ProcessPoolExecutor, ThreadPoolExecutor,
                                as_completed)
from multiprocessing import cpu_count, freeze_support
from pathlib import Path

import ujson as json
from rich import print
from rich.color import Color
from rich.live import Live
from rich.live_render import LiveRender
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress
from rich.prompt import Prompt
from rich.style import Style
from rich.table import Table
from rich.text import Text
from rich.theme import Theme
from sh import Command, ErrorReturnCode, RunningCommand

import myaml as yaml
from atlas import sg, max_title
from chapter import Chapter, chapter_gen, get_text_path
from log import BASE, console, log


class TextFileNotFound(Exception):
    pass

class TextPathNotFound(Exception):
    pass

class ChapterNotFound(Exception):
    pass

class MarkdownGenerationError(Exception):
    pass


# def tp_edit():
#     chapters = chapter_gen()
#     with Progress(console=console) as progress:
#         task = progress.add_task("Reading Text...", total=len(chapters))
#         with ThreadPoolExecutor(max_workers=cpu_count()) as executor:
#             futures = [executor.submit(edit, chapter, progress) for chapter in chapters]
#             for future in as_completed(futures):
#                 progress.advance(task)

# def pp_edit():
#     freeze_support()
#     chapters = chapter_gen()
#     with Progress(console=console) as progress:
#         task = progress.add_task("Reading Text...", total=len(chapters))
#         with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
#             futures = [executor.submit(edit, chapter, progress) for chapter in chapters]
#             for future in as_completed(futures):
#                 progress.advance(task)

# def sequential_edit():
#     chapters = chapter_gen()
#     with Progress(console=console) as progress:
#         task = progress.add_task("Reading Text...", total=len(chapters))
#         for chapter in chapters:
#             edit(chapter, progress)
#             progress.advance(task)

REPLACEMENTS = {
        "shit1": {"regex": r"sh\*t", "replacement": "shit"},
        "shit2": {"regex": r"s\*#t", "replacement": "shit"},
        "shit3": {"regex": r"Sh\*t", "replacement": "Shit"},
        "shit4": {"regex": r"S\*#t", "replacement": "Shit"},
        "fuck1": {"regex": r"f\*#k", "replacement": "fuck"},
        "fuck2": {"regex": r"f\*ck", "replacement": "fuck"},
        "fuck3": {"regex": r"F\*#k", "replacement": "Fuck"},
        "fuck4": {"regex": r"F\*ck", "replacement": "Fuck"},
        "bitch1": {"regex": r"b\*tch", "replacement": "bitch"},
        "bitch2": {"regex": r"B\*tch", "replacement": "Bitch"},
        "ass1": {"regex": r" \*ss ", "replacement": " ass "},
        "ass2": {"regex": r"\n\*ss ", "replacement": r"\nAss "},
        "ass3": {"regex": r"\. \*ss ", "replacement": ". Ass "},
        "asshole1": {"regex": r" \*sshole ", "replacement": r" asshole "},
        "asshole2": {"regex": r"\"\*sshole ", "replacement": r"\"Asshole "},
        "asshole3": {"regex": r"\. \*sshole ", "replacement": r"\. Asshole"},
        "hell1": {"regex": r" h\*ll ", "replacement": r" hell "},
        "hell2": {"regex": r"\"H\*ll ", "replacement": r"\"Hell "},
        "hell3": {"regex": r"\. H*ll ", "replacement": r"\. Hell"},
        "iceskin": {"regex": r"Ice Skin", "replacement": "Jadeskin"},
        "ice-skin": {"regex": r"Ice-Skin", "replacement": "Jadeskin"}
    }

ICESKIN = {
    "iceskin": {"regex": r"Ice Skin", "replacement": "Jadeskin"},
    "ice-skin": {"regex": r"Ice-Skin", "replacement": "Jadeskin"}
}

keys = REPLACEMENTS.keys()

def edit_chapter(chapter: int) -> None:
    # _. Edit the text for the given chapter.
    # . Connect to MongoDB
    sg()
    doc = Chapter.objects(chapter=chapter).first() # type: ignore
    if doc:
        if doc.text_path:
            text_path = Path(doc.text_path)
            if text_path.exists():
                # , Read the text for the given chapter from disk
                with open(text_path, "r") as infile:
                    text = infile.read()

                # , Edit the text for the given chapter
                changed = False
                for key in keys:
                    bad_word = REPLACEMENTS[key]
                    regex = bad_word["regex"]
                    replacement = bad_word["replacement"]
                    result = re.search(regex, text)
                    if result:
                        changed = True
                        text = re.sub(regex, replacement, text)
                        log.debug(f"Replaced {regex} with {replacement} in Chapter {chapter}.")
            else:
                raise TextFileNotFound(f"Text file for Chapter {chapter} not found.")
        else:
            raise TextPathNotFound(f"Text path for Chapter {chapter} not found.")
    else:
        raise ChapterNotFound(f"Chapter {chapter} not found.")

    if changed:
        # , Write the edited text for the give chapter to disk if changed
        with open (text_path, 'w') as outfile:
            outfile.write(text)
            log.debug(f"Wrote text for Chapter {chapter} to {text_path}.")

    # . Update MongoDB with the edited text for the given chapter
    doc.text = text

    # . Fix Title
    title = doc.title
    if 'Ice Skin' in title:
        title = title.replace('Ice Skin', 'Jadeskin')
        doc.title = title
        log.debug(f"Updated title for Chapter {chapter} to {title}.")
    if 'Ice-Skin' in title:
        title = title.replace('Ice-Skin', 'Jadeskin')
        doc.title = title
        log.debug(f"Updated title for Chapter {chapter} to {title}.")

    # . Save the document
    doc.save()

def update_md(chapter: int) -> None:
    # _. Update the markdown for the given chapter.
    # . Connect to MongoDB
    sg()
    doc = Chapter.objects(chapter=chapter).first() # type: ignore
    if doc:
        title = max_title(doc.title)
        section = f"{doc.section}"
        book = f"{doc.book}"

        metadata = f"---\n"
        metadata = f"{metadata}title: {title}\n"
        metadata = f"{metadata}chapter: {chapter}\n"
        metadata = f"{metadata}section: {section}\n"
        metadata = f"{metadata}book: {book}\n"
        metadata = f"{metadata}CSS: style.css\n"
        metadata = f"{metadata}viewport: width=device-width\n"
        metadata = f"{metadata}---\n\n"

        atx = f"## {title}\n\n"
        atx = f"{atx}### Chapter {chapter}\n\n"

        img = '<figure>\n\t<img src="../Images/gem.gif" alt="" id="gem" width="120" height="60" />\n</figure>\n\n'

        text = str(doc.text)
        text = text.strip()

        md = f"{metadata}{atx}{img}{text}"

        md_path = Path(doc.md_path)
        with open (md_path, 'w') as outfile:
            outfile.write(md)

        doc.md = md
        doc.save()
    else:
        raise ChapterNotFound(f"Chapter {chapter} not found.")




def main():
    '''
    Main function.
    '''
    with Progress(console=console) as progress:
        chapter = 0
        task = progress.add_task(description=f"Editing Supergene Chapters... Chapter {chapter}/3462", total = 3460) # type: ignore
        chapters = chapter_gen()

        for chapter in chapters:
            update_md(chapter)
            progress.advance(task)


if __name__ == "__main__":
    main()