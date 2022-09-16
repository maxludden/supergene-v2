#!//Users/maxludden/dev/venvs/supergene/bin/python

# supergene/taks/backup.py
from operator import truediv
import os
from datetime import datetime
from pathlib import Path

import sh
from dotenv import load_dotenv
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.style import Style
from rich.text import Text
from rich.color import Color
from sh import mongodump, rm  # type: ignore


try:
    from pushover import notify, notify_console
except ModuleNotFoundError:
    from .pushover import notify, notify_console
except ImportError:
    from tasks.pushover import notify, notify_console

# Setup Script
SUDO = os.environ.get("SUDO")
notify_console = Console()
notify_console.clear()  # Clears Console

date = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
dump_dir = Path("/Users/maxludden/dev/py/supergene/backups/")
outfile = f"{date}_SUPERFORGE"
filepath = dump_dir / outfile
if not filepath.exists():
    filepath.mkdir(parents=True, exist_ok=True)

# > Bake SH Commands
URL = "mongodb://localhost:27017"
mongodump = mongodump.bake("--port", "27017", "-o", filepath, "-d", "SUPERGENE")
rm = rm.bake("-rf")

# > Count number of backups
backups = []
with sh.contrib.sudo(password=SUDO, _with=True):
    for child in dump_dir.iterdir():
        if child.is_dir():
            backups.append(child.name)

# > Remove oldest backup if there are more than 6
if len(backups) > 6:
    panel = Panel(
        Text("Deleting oldest backup", style="bold white"),
        title=Text("MongoDump", style="bold white"),
        title_align="left",
        style=Style(color="purple", bold=True),
    )
    notify_console.print(panel)
    oldest_backup = backups[0]
    oldest_backup = dump_dir / oldest_backup
    with sh.contrib.sudo(password=SUDO, _with=True):
        rm(oldest_backup)  # removes oldest backup

# > Update user on status and backup the database
mongodump_panel = Panel(
    Text("Creating new backup...", style="bold white"),
    title=Text("MongoDump", style="bold white"),
    title_align="left",
    style=Style(color="green", bold=True),
)
notify_console.print(mongodump_panel)
with sh.contrib.sudo(password=SUDO, _with=True):
    mongodump(URL)


panel = Panel(
    Text("Backup Complete!", style="bold white"),
    title=Text("MongoDump", style="bold white"),
    title_align="left",
    style=Style(color="bright_green"),
)
notify_console.print(panel)
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
msg = f"Backup completed at {now}"
notify(title="MongoDump", msg=msg, color=Color.parse("cornflower_blue"))
