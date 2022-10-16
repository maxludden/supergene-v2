# src/edit.py
import re
from concurrent.futures import (ProcessPoolExecutor, ThreadPoolExecutor,
                                as_completed)
from multiprocessing import cpu_count
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
from atlas import sg
from chapter import Chapter, chapter_gen, get_text_path
from log import BASE, console, log


class TextFileNotFound(Exception):
    pass

class ChapterNotFound(Exception):
    pass

class MarkdownGenerationError(Exception):
    pass

def read_text(chapter: int, save: bool = True) -> str:
    '''
    Read the text for the given chapter from the text file.

    Args:
        `chapter` (int):
            The given chapter.
        `save` (bool):
            Whether or not to save the text to MongoDB.

    Returns:
        `text` (str):
            The text for the given chapter.
    '''
    text_path = Path(str(get_text_path(chapter)))
    if text_path.exists():
        with open(text_path, "r") as infile:
            text = str(infile.read())
            if save:
                sg()
                doc = Chapter.objects(chapter=chapter).first() # type: ignore
                doc.text = text
                doc.save()
                log.debug(f"Read text for Chapter {doc.chapter}. Updated MongoDB.")
            return text
    else:
        raise TextFileNotFound(f"Text file not found for doc {chapter}.")

def edit_text(chapter_text: str, progress: Progress) -> str:
    '''
    Edit the text for the given chapter.

    Args:
        `chapter_text` (str):
            The text for the given chapter.

    Returns:
        `edited_text` (str):
            The edited text for the given chapter.
    '''

    bad_words_task = progress.add_task("Editing Bad Words...", total=13)
    bad_words = {
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
        "ass2": {"regex": r"\n\*ss ", "replacement": "\nAss "},
        "ass3": {"regex": r"\. \*ss ", "replacement": ". Ass "},
    }
    bad_word_keys = bad_words.keys()
    for key in bad_word_keys:
        bad_word = bad_words[key]
        regex = bad_word["regex"]
        replacement = bad_word["replacement"]
        result = re.search(pattern=regex, string=chapter_text)

        if result != None:
            chapter_text = re.sub(regex, replacement, chapter_text, re.M)
            console.print(
                Panel(
                    f"[bold bright_white]Corrected {replacement.capitalize()}.[/]",
                    title = "[bright_magenta]Bad Words[/]",
                    border_style=Style(
                        color="bright_purple",
                        bold=True
                    )
                )
            )
        progress.advance(bad_words_task)

    iceskin_task = progress.add_task("Editing Ice Skin...", total=2)
    if 'Ice Skin' in chapter_text:
        chapter_text = re.sub(r'Ice Skin', 'Jadeskin', chapter_text, re.I)
    progress.advance(iceskin_task)
    if 'Ice-Skin' in chapter_text:
        chapter_text = re.sub(r'Ice-Skin', 'Jadeskin', chapter_text, re.I)
    progress.advance(iceskin_task)

    return chapter_text

def write_text(chapter: int, text: str) -> None:
    '''
    Write the edited text for the given chapter to the text file.

    Args:
        `chapter` (int):
            The given chapter.
        `text` (str):
            The edited text for the given chapter.
    '''
    text_path = Path(str(get_text_path(chapter)))
    with open(text_path, "w") as outfile:
        outfile.write(text)
        log.debug(f"Wrote text for Chapter {chapter} to {text_path}.")
    sg()
    doc = Chapter.objects(chapter=chapter).first() # type: ignore
    doc.text = text
    doc.save()
    log.debug(f"Updated MongoDB with edited text for Chapter {doc.chapter}.")
    return None

def edit(chapter: int, progress: Progress) -> None:
    '''
    Edit the text for the given chapter.

    Args:
        `chapter` (int):
            The given chapter.
    '''
    text = read_text(chapter)
    edited_text = edit_text(text, progress)
    write_text(chapter, edited_text)
    return None

def tp_edit():
    chapters = chapter_gen()
    with Progress(console=console) as progress:
        task = progress.add_task("Reading Text...", total=len(chapters))
        with ThreadPoolExecutor(max_workers=cpu_count()) as executor:
            futures = [executor.submit(edit, chapter, progress) for chapter in chapters]
            for future in as_completed(futures):
                progress.advance(task)

chapters = chapter_gen()
with Progress(console=console) as progress:
    task = progress.add_task("Reading Text...", total=len(chapters))
    for chapter in chapters:
        edit(chapter, progress)
        progress.advance(task)