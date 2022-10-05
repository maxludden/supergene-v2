from pathlib import Path
import os
import io
from sh import Command, ErrorReturnCode, RunningCommand
from src.log import BASE, console, log, current_run, theme
from src.atlas import sg, max_title
from dotenv import load_dotenv

from rich import print
from rich.panel import Panel
from rich.text import Text
from rich.style import Style
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.console import Console

from typing import Any, Dict, List, Optional, Tuple, Union

load_dotenv()

# > Console
console = Console(theme=theme, color_system="truecolor", width=100, align="center")
console.clear()
console.rule(
    title=f"\n\n[value]Gradient.py[/][bold bright_white] | [/][key]Run {current_run}[/]",
    style="bold bright_white",
    characters='━',
    align='center')


# > Commands and Paths
SUDO = os.environ.get("SUDO")
TEMP = BASE/'temp'
TEST_TEXT = TEMP / 'test_text.txt'
USER_TEXT = TEMP/ 'text.txt'
buf = io.StringIO()
lolcat = Command("lolcat")
gradient = lolcat.bake("-p", "10", "-F", "0.5")

# > Rich
rich = Command('rich')
panel = rich.bake('--panel','rounded','--panel-style','')

def main(user_text: Optional[str] = None, test: bool = False):
    if test:
        title = max_title("Gradient Test Mode")



        with open (TEMP, 'w') as outfile:
            outfile.write(text)
        gradient(text)
        gradient_output = buf.getvalue()
        print(gradient_output)

        console.print(
            Panel(
                gradient_output,
                title=f"[green]{title}[/]",
                title_align="left",
                border_style="#0c620c",
                padding=(1, 2),
                expand=True,
                width=100
            )
        )
    user_input = IntPrompt.ask(
        "1. Read text from file\n2. Enter text manually", choices=["1", "2"]
    )
    match int(user_input):
        case 1:
            file_path = Prompt.ask("Enter relative file path: (Supergene is CWD)")
            with open(file_path, "r") as infile:
                text = infile.read()
                gradient(text)
        case 2:
            text = Prompt.ask(
                "Enter a string that you would like to apply a gradient to:",
                default="Hello World!",
            )
            gradient(text)

    console.print(
        Panel(
            buf.getvalue(),
            title="[bright_magenta]Gradient[/]",
            title_align="left",
            border_style="bright_cyan",
            expand=True,
            width=80,
        )
    )

if __name__ == "__main__":
    main("", test=True)