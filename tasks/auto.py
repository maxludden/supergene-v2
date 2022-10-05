#!/Users/maxludden/dev/venvs/supergene/bin/python
# supergene/tasks/auto.py
# Imports
from datetime import datetime
from os import environ
from pathlib import Path
from typing import Any, List
from io import StringIO

import sh
from dotenv import load_dotenv
from rich import print
# from rich.color import Color
from rich.console import Console
# from rich.text import Text
from rich.panel import Panel
# from rich.style import Style
from rich.theme import Theme
from sh import Command, RunningCommand, ErrorReturnCode

from tasks.pushover import notify, notify_console

load_dotenv()

# . Helper Functions
SUDO = environ.get("SUDO") # sudo password

# > rm -rf
rm = Command('rm')
rm = rm.bake('-rf')

# > MongoDump
brew = Command('brew')
services = brew.bake('services')
restart = brew.bake('services', 'restart', '--all')

#. Rich
theme = Theme(
    {
        'key': '#5fffff italic',
        'value': '#ffffff bold',
        'title': 'cornflower_blue bold',
        'running': '#54c6ff',
        'running_title': '#54c6ff reverse',
        'error': 'bold #ff0084',
        'error_title': 'bold #ff0084 reverse',
        'success': '#00ff00',
        'success_title': '#00ff00 reverse'
    }
)
console = Console(theme=theme)

def service_error(print: bool = False) -> bool:
    '''Check if MongoDB is running'''
    try:
        buf = StringIO()
        services(_out=buf)

        # . Output
        services_output = buf.getvalue()
        output_split = services_output.splitlines()
        formatted_output = []
        for line in output_split:
            if len(str(line)) < 79:
                extra = 79 - len(str(line))
                line = f"{line}{' ' * extra}"
            formatted_output.append(line)

        output = "\n".join(formatted_output)

        if 'error' in output:
            console.print(Panel(services_output, title='[title]Brew Services Output[/title]', style='value', expand=False, border_style='running'))
            return True
        else:
            return True
    except ErrorReturnCode:
        console.print(Panel("[error]Unknown Error occured while checking if [/error][bold bright_white]MongoDB[/][error] was running.[/]", title="Checking Services", title_align="left", expand=True, width=80,border_style="#ffffff"))
        return False


if __name__ == "__main__":
    if service_error():
        console.print(Panel("[success_title]Running[/]", style='success_title'))

    else:
        console.print(Panel("[error_title]Not Running[/]", style='error_title'))


│                                                                                                                 │