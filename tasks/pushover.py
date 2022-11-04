import os
from datetime import datetime
import ujson as json
from os import system
from pathlib import Path
from time import sleep


# from colr import Colr as C
from dotenv import load_dotenv
from requests import post
from rich import print
from rich.color import Color
from rich.panel import Panel
from rich.style import Style
from rich.text import Text
from sh import Command
from maxconsole import get_theme, get_console
from maxprogress import get_progress
from maxcolor import console, rainbow, gradient_panel

load_dotenv()
console = get_console(get_theme())
progress = get_progress()

USER_KEY = os.environ.get("USER_KEY")
API_TOKEN = os.environ.get("API_TOKEN")

# > YAY ----------------------------------
def yay(clear: bool = False) -> None:
    """
    Celebrates Anything!

    Args:
        `clear` (bool, optional): Whether to clear the console prior to celebrating. Defaults to True.
    """
    if clear == True:
        system("clear")
    sleep(0.75)
    # 'for i in {1..10}\ndo\n  open raycast://confetti && echo "Celebrate  🎉"\ndone'

    open_cmd = Command("open")
    celebrate = open_cmd.bake("raycast://confetti")

    # > Mario Sound
    CWD = Path.cwd()
    mario = CWD / "styles" / "mario_notification.mp3"

    # > Celebrate
    os.system("afplay " + str(mario))
    system("for i in {1..10};\ndo\n  open raycast://confetti\ndone")


# > SUPER YAY ------------------------------
def superyay(clear: bool = False) -> None:
    """
    Excessively Celebrates Anything!

    Args:
        `clear` (bool, optional): Whether to clear the console prior to celebrating. Defaults to False.
    """
    if clear == True:
        system("clear")
    sleep(0.75)
    for i in range(0, 4):
        system(
            'for i in {1..20}\ndo\n  open raycast://confetti && echo "Celebrate  🎉"\ndone'
        )
        sleep(1)


# > Pushover --------------------------------------
def notify(title: str, msg: str, color: Color = Color.parse("cornflower_blue")) -> None:
    url = "https://api.pushover.net/1/messages.json"
    payload = {
        "token": API_TOKEN,
        "user": USER_KEY,
        "title": title,
        "message": msg,
        "sound": "mario",
    }
    response = post(url, data=payload)

    # . Print Pushover Status
    if response.status_code == 200:
        console.print(
            gradient_panel(
                "Push notification sent via Pushover",
                "Success - 200"
            )
        )
    else:
        # . If Pushover Fails, print error to panel
        console.print(
            Panel(
                Text(
                    "Notification Failed!",
                    style=Style(color="bright_red", bold=True, reverse=True),
                ),
                title=Text(
                    "Pushover", style=Style(color="red", bold=True, bgcolor="default")
                ),
                title_align="left",
                style=Style(color="bright_red", bold=True, reverse=True),
            )
        )
