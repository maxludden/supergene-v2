from inspect import currentframe, getframeinfo
import re
from os import environ
from pathlib import Path

import ujson as json
from maxcolor import console, gradient_panel, log, progress, rainbow
from mongoengine import ValidationError

import src.myaml as yaml
from src.chapter import Chapter, chapter_gen
from atlas import sg
from rich.panel import Panel
from rich.column import columns
from rich.pretty import pprint
from rich.table import Table, Column

@log.catch()
def main():
    pattern = re.compile(r'Sky B\*stard\?', re.I)

    sg()
    results = []

    with progress:
        task = progress.add_task("Searching...", total=3460)

        for doc in Chapter.objects().all(): # type: ignore
            if doc:
                result = pattern.search(doc.text)
                if result:
                    index = len(results)
                    match = result.match
                    match_group = match.group()

                    table = Table(
                        title=f'Chapter {doc.chapter}',
                        title_align='center',
                        show_header=True,
                        header_style='bold magenta',
                        style='rainbow',
                        row_styles=['dim', 'bright'],
                    )

                    table.add_column('key', justify='left', style='key', no_wrap=True)
                    table.add_column('value', justify='left', style='value', no_wrap=True)
                    table.add_row('match', str(match))
                    table.add_row('match_group', str(match_group))

                    title = rainbow(f"Index {index}")

                    panel = Panel(
                        table,
                        title=title,
                        title_align='left',
                        border_style='white',
                    )

if __name__ == '__main__':
    main()