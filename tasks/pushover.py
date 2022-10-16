import os
from json import load
from datetime import datetime
from os import system
from time import sleep
from pathlib import Path

from requests import post
from rich import print
from rich.theme import Theme
from rich.console import Console
from rich.panel import Panel
from rich.style import Style
from rich.text import Text
from rich.color import Color
from sh import Command, RunningCommand
import sh
# from colr import Colr as C
from cfonts import render, say

from dotenv import load_dotenv

console = Console()
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
    open_cmd = Command("open")
    celebrate = open_cmd.bake("raycast://confetti")

    # > Mario Sound
    CWD = Path.cwd()
    mario = CWD / "styles" / "mario_notification.mp3"

    # > Celebrate
    for i in range(1, 11):
        if i == 1:
            os.system("afplay " + str(mario))
            celebrate()

    # Gradient Text
    # gradient = C("Celebrate", fore=(255, 0, 0), back=(0, 255, 0))     
    # yay_title = C("Yay!").gradient_rgb(start=(0, 255, 68), stop=(255, 0, 212))

    # # Rainbow gradient
    # ryay = C("Celebrate 🎉").rainbow(rgb_mode=True)
    # ryay_title = C("Yay!").rainbow(fore="white", rgb_mode=True)

    # console.print(
    #     Panel(
    #         yay,  # type: ignore
    #         title=yay_title,  # type: ignore
    #         title_align="left",
    #         expand=True,
    #         width=80,
    #     )
    # )


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
    if response.status_code == 200:

        success_panel = (
            Panel(
                Text("Notification Sent!", style="bold white"),
                title=Text("Pushover", style="bold white"),
                title_align="left",
                style=Style(color=color, bold=True),
            ),
        )
        yay()
        console.print(success_panel)
    else:

        error_panel = Panel(
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
        console.print(error_panel)

yay()