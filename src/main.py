from inspect import currentframe, getframeinfo
import re
from os import environ
from pathlib import Path

import ujson as json
from maxcolor import gradient, gradient_panel
from mongoengine import ValidationError
from maxconsole import get_theme, get_console
from maxprogress import get_progress

import src.myaml as yaml
from src.chapter import Chapter, chapter_gen
from atlas import sg
from rich.panel import Panel
from rich.columns import Columns
from rich.pretty import pprint
from rich.table import Table, Column
from loguru import logger as log

console = get_console(get_theme())
progress = get_progress(console)


@log.catch
def edit(pattern: str) -> None:
    """
    Edits the given pattern.

    Args:
        `pattern` (str):
            The given pattern.
    """
    regex = re.compile(pattern, re.I)
    sg()
    results = []

    with progress:
        task = progress.add_task("Searching...", total=3460)

        for doc in Chapter.objects().all(): # type: ignore
            if doc:
                result = re.search(regex, doc.text)
                if result:
                    index = len(results)
                    match = result.match # type: ignore
                    match_group = match.group()

                    table = Table(
                        title=f'Chapter {doc.chapter}',
                        show_header=True,
                        header_style='bold magenta',
                        style='rainbow',
                        row_styles=['dim', 'bright'],
                    )

                    table.add_column('key', justify='left', style='key', no_wrap=True)
                    table.add_column('value', justify='left', style='value', no_wrap=True)
                    table.add_row('match', str(match))
                    table.add_row('match_group', str(match_group))

                    title = gradient(f"Index {index}", 5)

                    panel = Panel(
                        table,
                        title=title,
                        title_align='left',
                        border_style='white',
                    )

                    results.append(panel)

                    progress.advance(task)