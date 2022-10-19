# src/edit.py
import re
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from multiprocessing import cpu_count
from pathlib import Path
from time import perf_counter

import ujson as json
from rich import print
from rich.color import Color
from rich.live import Live
from rich.live_render import LiveRender
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, MofNCompleteColumn
from rich.prompt import Prompt
from rich.style import Style
from rich.table import Table, Column
from rich.text import Text
from rich.theme import Theme
from sh import Command, ErrorReturnCode, RunningCommand

import myaml as yaml
from atlas import sg, max_title
from chapter import Chapter, get_text_path
from log import BASE, console, log, progress


class TextFileNotFound(Exception):
    pass


class TextPathNotFound(Exception):
    pass


class ChapterNotFound(Exception):
    pass


class MarkdownGenerationError(Exception):
    pass


class HTMLGenerationError(Exception):
    pass


words = [
    "Alu Alu Alu!",
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
    "Pang!",
    "Pang! Pang! Pang!",
    "Pop!",
    "Poof!",
    "Roar!",
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


class chapter_gen:
    """
    Generator for chapter numbers.
    """

    def __init__(self, start: int = 1, end: int = 3462):
        self.start = start
        self.end = end
        self.chapter_number = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.chapter_number >= 3462:
            raise StopIteration
        elif self.chapter_number == 3094:
            # Skipping chapter 3095
            # 3094 + 1 + 1 = 3096
            self.chapter_number += 2
            return self.chapter_number
        elif self.chapter_number == 3116:
            # Skipping chapter 3117
            # 3116 + 1 + 1 = 3118
            self.chapter_number += 2
            return self.chapter_number
        else:
            self.chapter_number += 1
            return self.chapter_number

    def __len__(self):
        return self.end - self.start + 1


REPLACEMENTS = {
    "shit1": {"regex": r"sh\*t", "replacement": "shit"},
    "shit2": {"regex": r"s\*#t", "replacement": "shit"},
    "shit3": {"regex": r"Sh\*t", "replacement": "Shit"},
    "shit4": {"regex": r"S\*#t", "replacement": "Shit"},
    "fuck1": {"regex": r"f\*#k", "replacement": "fuck"},
    "fuck2": {"regex": r"f\*ck", "replacement": "fuck"},
    "fuck3": {"regex": r"F\*#k", "replacement": "Fuck"},
    "fuck4": {"regex": r"F\*ck", "replacement": "Fuck"},
    "goddamn1": {"regex": r"godd\*mn", "replacement": "goddamn"},
    "goddamn2": {"regex": r"Godd\*mn", "replacement": "Goddamn"},
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
    "ice-skin": {"regex": r"Ice-Skin", "replacement": "Jadeskin"},
}

ICESKIN = {
    "iceskin": {"regex": r"Ice Skin", "replacement": "Jadeskin"},
    "ice-skin": {"regex": r"Ice-Skin", "replacement": "Jadeskin"},
}

keys = REPLACEMENTS.keys()


def edit_chapter(chapter: int) -> None:
    """Edit the text for the given chapter."""
    # . Connect to MongoDB
    sg()
    doc = Chapter.objects(chapter=chapter).first()  # type: ignore
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
                        log.debug(
                            f"Replaced {regex} with {replacement} in Chapter {chapter}."
                        )
            else:
                raise TextFileNotFound(f"Text file for Chapter {chapter} not found.")
        else:
            raise TextPathNotFound(f"Text path for Chapter {chapter} not found.")
    else:
        raise ChapterNotFound(f"Chapter {chapter} not found.")

    if changed:
        # , Write the edited text for the give chapter to disk if changed
        with open(text_path, "w") as outfile:
            outfile.write(text)
            log.debug(f"Wrote text for Chapter {chapter} to {text_path}.")

    # . Update MongoDB with the edited text for the given chapter
    doc.text = text

    # . Fix Title
    title = doc.title
    if "Ice Skin" in title:
        title = title.replace("Ice Skin", "Jadeskin")
        doc.title = title
        log.debug(f"Updated title for Chapter {chapter} to {title}.")
    if "Ice-Skin" in title:
        title = title.replace("Ice-Skin", "Jadeskin")
        doc.title = title
        log.debug(f"Updated title for Chapter {chapter} to {title}.")

    # . Save the document
    doc.save()


def update_md(chapter: int) -> None:
    """Update the markdown file for the given chapter."""
    # . Connect to MongoDB
    sg()
    doc = Chapter.objects(chapter=chapter).first()  # type: ignore
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
        with open(md_path, "w") as outfile:
            outfile.write(md)

        doc.md = md
        doc.save()
    else:
        raise ChapterNotFound(f"Chapter {chapter} not found.")


def generate_html(chapter: int, save: bool = True):
    start = perf_counter()
    sg()
    doc = Chapter.objects(chapter=chapter).first()  # type: ignore
    if doc:
        html_path = Path(doc.html_path)
        md_path = Path(doc.md_path)

        if md_path.exists():
            multimarkdown = Command("multimarkdown")
            mmd = multimarkdown.bake(
                "-f",
                "--nolabels",
                "-o",
            )
            result = mmd(html_path, md_path)
            if result.exit_code == 0:  # type: ignore

                if save:
                    sg()
                    doc = Chapter.objects(chapter=chapter).first()  # type: ignore
                    with open(html_path, "r") as infile:
                        doc.html = infile.read()

            else:
                raise HTMLGenerationError(
                    f"Error generating HTML for doc {doc.chapter}."
                )

        else:
            raise ChapterNotFound(f"Markdown file not found for doc {doc.chapter}.")
    else:

        raise ChapterNotFound(f"Chapter {doc.chapter} not found.")
    end = perf_counter()
    duration = end - start

    return duration


def update_chapter(chapter: int) -> int:
    """Update the text, markdown, and html for the given chapter."""
    sg()
    doc = Chapter.objects(chapter=chapter).first()  # type: ignore
    if doc:

        # . Edit the text for the given chapter
        text_path = Path(doc.text_path)

        # Read the text for the given chapter from disk
        with open(text_path, "r") as infile:
            text = infile.read()

        # Edit the text for the given chapter
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

        # Update MongoDB with the edited text for the given chapter
        doc.text = text

        # Fix Title
        title = doc.title
        if "Ice Skin" in title:
            title = title.replace("Ice Skin", "Jadeskin")
            doc.title = title
            log.debug(f"Updated title for Chapter {chapter} to {title}.")
        if "Ice-Skin" in title:
            title = title.replace("Ice-Skin", "Jadeskin")
            doc.title = title
            log.debug(f"Updated title for Chapter {chapter} to {title}.")

        if changed:
            #  Write the edited text for the give chapter to disk if changed
            with open(text_path, "w") as outfile:
                outfile.write(text)
                log.debug(f"Wrote text for Chapter {chapter} to {text_path}.")

        # . Markdown
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
        with open(md_path, "w") as outfile:
            outfile.write(md)

        doc.md = md

        # . HTML
        html_path = Path(doc.html_path)
        md_path = Path(doc.md_path)

        multimarkdown = Command("multimarkdown")
        mmd = multimarkdown.bake(
            "-f",
            "--nolabels",
            "-o",
        )
        result = mmd(html_path, md_path)
        if result.exit_code == 0:  # type: ignore
            sg()
            doc = Chapter.objects(chapter=chapter).first()  # type: ignore
            with open(html_path, "r") as infile:
                doc.html = infile.read()
        else:
            raise HTMLGenerationError(f"Error generating HTML for doc {doc.chapter}.")
        doc.save()
        return chapter
    else:
        raise ChapterNotFound(f"Chapter {chapter} not found.")


if __name__ == "__main__":
    with progress:
        task = progress.add_task("Generating HTML...", total=3460)

        chapters = chapter_gen()

        with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
            futures = [executor.submit(update_chapter, chapter) for chapter in chapters]

            for future in as_completed(futures):
                print(f"Updated Chapter {future.result()}.")
                progress.advance(task)
