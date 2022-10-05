#!//Users/maxludden/dev/venvs/supergene/bin/python
# supergene/tasks/backup.py
# Imports
from datetime import datetime
from os import environ
from pathlib import Path
from typing import List, Any

import sh
from dotenv import load_dotenv
from rich import print
from rich.color import Color
from rich.console import Console
from rich.panel import Panel
from rich.style import Style
from rich.text import Text
from src.log import theme, console
from sh import mongodump, rm  # type: ignore

from tasks.pushover import notify

load_dotenv()

SUDO = environ.get("SUDO")

console = Console(theme=theme)


# > MongoDump - global
URL = "mongodb://localhost:27017"  # LOCALDB
backup_dir = Path("/Users/maxludden/dev/py/supergene/backups")  # Backup directory
mongodump = mongodump.bake("--port", "27017", "-o", backup_dir, "-d", "SUPERGENE")  # type: ignore
rm = rm.bake("-rf")

# . Helper Functions
def get_backups(print: bool = False) -> List[Any]:
    """Count Number of Backups"""
    backups = []

    with sh.contrib.sudo(password=SUDO, _with=True):  # type: ignore
        for child in backup_dir.iterdir():  # type: ignore
            if child.is_dir():
                dir_name = child.name
                backups.append(dir_name)

    backups.sort(reverse=True)
    backup_list = "\n".join(backups)  # type: ignore
    backup_count = len(backups)  # type: ignore
    if print:
        console.print(
            Panel(
                backup_list,
                title="[title_style]MongoDump[/]",
                title_align="left",
                border_style="blue",
                expand=False,
                subtitle=f"[bright_blue]Number of Backups:[/][#54c6ff]{backup_count}[/]",
                subtitle_align="right",
            )
        )
    return backups  # type: ignore


def create_backup() -> None:
    """Ensure that there are only backups for the last 7 days"""
    backups = get_backups()  # . Gets backups

    # > Remove oldest backup if there are more than 6
    if len(backups) > 6:
        console.print(
            Panel(
                f"[key_style]Current Number of Backups:[/][value_style] {len(backups)}\t\t\t\t[/]",
                title="[title_style]MongoDump[/]",
                title_align="left",
                border_style="blue",
                expand=False,
                subtitle=f"[bright_blue]{__file__}[/][#FFFFFF]|[/][#54c6ff]line 85[/]",
                subtitle_align="right",
            )
        )
        for backup in backups[6:]:
            console.print(
                Panel(
                    f"[key_style]Removing Backup:[/][value_style] {backup}[/]",
                    title="[title_style]MongoDump[/]",
                    title_align="left",
                    border_style="blue",
                    expand=False,
                    subtitle=f"[bright_blue]{__file__}[/][#FFFFFF]|[/][#54c6ff]line 97[/]",
                    subtitle_align="right",
                )
            )
            with sh.contrib.sudo(password=SUDO, _with=True):
                rm(backup_dir / backup)

    # > Update user on status and backup the database
    mongodump_panel = Panel(
        f"[key_style]Creating new backup...[/]",
        title="[title_style]MongoDump[/]",
        title_align="left",
        border_style=Style(color="magenta", bold=True),
        expand=False,
    )
    console.print(mongodump_panel)
    with sh.contrib.sudo(password=SUDO, _with=True):  # type: ignore
        mongodump(URL)

    panel = Panel(
        f"[value_style]Backup Complete![/]",
        title="[title_style]MongoDump[/]",
        title_align="left",
        style=Style(color="bright_green"),
        expand=False,
    )
    console.print(panel)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"Backup completed at {now}"
    notify(title="MongoDump", msg=msg, color=Color.parse("cornflower_blue"))


get_backups()
create_backup()
