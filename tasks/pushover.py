import os
from json import load
from datetime import datetime
from os import system
from time import sleep

from requests import post
from rich import print
from rich.theme import Theme
from rich.console import Console
from rich.panel import Panel
from rich.style import Style
from rich.text import Text
from rich.color import Color

from dotenv import load_dotenv

notify_console = Console()
load_dotenv()

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
    system(
        'for i in {1..10}\ndo\n  open raycast://confetti && echo "Celebrate  🎉"\ndone'
    )


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
def notify(title: str, msg: str,
color: Color = Color.parse('cornflower_blue')) -> None:
    url = "https://api.pushover.net/1/messages.json"
    payload = {
        "token": API_TOKEN,
        "user": USER_KEY,
        "title": title,
        "message": msg,
        "sound": "mario",
    }
    response = post(url, data=payload)
    if response.status_code == 200:

        success_panel = Panel(
            Text("Notification Sent!", style="bold white"),
            title=Text("Pushover",
                style="bold white"
            ),
            title_align='left',
            style=Style(
                color = color,
                bold = True)
        ),
        yay()
        notify_console.print(success_panel)
    else:

        error_panel = Panel(
            Text("Notification Failed!",
                style=Style(
                    color = 'bright_red',
                    bold = True,
                    reverse = True
                ),
            ),
            title=Text(
                "Pushover",
                style=Style(
                    color="red",
                    bold=True,
                    bgcolor="default")
            ),
            title_align='left',
            style=Style(
                color='bright_red',
                bold=True,
                reverse=True
            ),
        )
        notify_console.print(error_panel)
