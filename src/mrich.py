# src/panel_factory.py

from abc import ABC, abstractmethod
from rich import print, inspect
from rich.console import Console, JustifyMethod
from rich.panel import Panel
from rich.style import Style
from rich.theme import Theme
from rich.text import Text
from rich.table import Table
from rich.columns import Columns
from rich.pretty import pprint
from rich.abc import RichRenderable
from rich.color import Color, ColorType
from ujson import dump, dumps, load, loads
from dotenv import load_dotenv
from os import environ

from pydantic import BaseModel, Field, validator, ValidationError
from pydantic.color import Color
from typing import List, Optional, Union, Any, Literal
from enum import Enum, EnumMeta
# Max's Log
try:
    from log import log
except ModuleNotFoundError:
    from .log import log
except ImportError:
    from src.log import log

# Max's YAML
try:
    from myaml import yaml
except ModuleNotFoundError:
    from .myaml import yaml
except ImportError:
    from src.myaml import yaml

# HEX   3HEX        RGB             ANSI           RGBA
#0000ff #00f       bright_blue       21      rgba(0,0,255,1)
#00ffff #0ff       bright_cyan       51      rgba(0,255,255,1)
#00ff00 #0f0       bright_green      46      rgba(0,255,0,1)
#ffff00 #ff0       bright_yellow     226     rgba(255,255,0,1)
#ffaf00 #ffaf00    orange1           208     rgba(255,175,0,1)
#ff0000 #f00       bright_red        196     rgba(255,0,0,1)
#ff00ff #f0f       bright_magenta    201     rgba(255,0,255,1)
#000000 #000       black             16      rgba(0,0,0,1)
#FFFFFF #fff       bright_whit       231     rgba(255,255,255,1)


custom_theme = Theme(
    {
        "pushover": "white on cornflower_blue",  # 249df1
        "debug": "bold cyan1",  # 00ffff
        "info": "bold green",  # 008800
        "success": "bold green1",  # 00ff00
        "warning": "bold yellow1",  # ffff00
        "error": "bold orange1",  # ff8800
        "critical": "bold reverse red1",  # ff0000
    }
)
_blue = dict({
    "blue1": "#0000ff",
    "cyan1": "#00ffff",
    "green1": "#00ff00",
})

# # Panel Styles
# debug = Style(color="blue1"), bgcolor="grey0", bold=True)  # 00ffff
# info = Style(color="grey100", bgcolor="green1", bold=True)  # 008800
# success = Style(color="green1", bgcolor="grey0", bold=True)  # 00ff00
# warning = Style(color="yellow", bgcolor="grey0", bold=True)  # ffff00
# error = Style(color="orange1", bgcolor="grey0", bold=True)  # ff8800
# critical = Style(color="red1", bgcolor="grey0", bold=True)  # ff0000
# pushover = Style(color="grey100", bgcolor="cornflower_blue", bold=True)
# rpushover = Style(color="cornflower_blue", bgcolor="grey100", bold=True)
# mconsole = Console(theme=custom_theme)

class PanelColor(Enum):
    color:Union[Color("cornflower_blue"), Color('lime'), Color('yellow'), Color('orange'), Color('red')] = Color('cornflower_blue')

    @validator('color')
    def color_validator(cls, v):
        match v:
            case 'blue'|'green'|'yellow'|'orange'|'red':
                return v
            case _:
                raise ValueError('Invalid panel color: {color}')

class ColorPanel(Panel):
    content: Union[str, Text]
    title: Union[str, Text, None] = None
    color: Color =  Color('cornflower_blue')),
    justify: Literal["left", "center", "right"] = "left"

    def __init__(self, content: Union[str, Text], title: Union[str, Text, None] = None, color: Color = Color("cornflower_blue"), justify=Literal["left", "center", "right"] = "left", **kwargs):
        self.content = content
        self.title = title
        self.color = color
        self.justify = justify
        super().__init__(content, title, **kwargs)
    match color:
        case "blue":
            border_style = Style(color="blue1", bold=True)
            title_style = Style(color="cyan1", bold=True, reverse=True)
            text_style = Style(color="grey100", bold=True)
        case "green":
            border_style = Style(color="green1", bold=True)
            title_style = Style(color="green1", bold=True, reverse=True)
            text_style = Style(color="grey100", bold=True)
        case "yellow":
            border_style = Style(color="yellow1", bold=True)
            title_style = Style(color="yellow1", bold=True, reverse=True)
            text_style = Style(color="grey100", bold=True)
        case "orange":
            border_style = Style(color="orange1", bold=True)
            title_style = Style(color="orange1", bold=True, reverse=True)
            text_style = Style(color="grey100", bold=True)
        case "red":
            border_style = Style(color="red1", bold=True)
            title_style = Style(color="red1", bold=True, reverse=True)
            text_style = Style(color="grey100", bold=True)
        case _:
            raise ValueError("Invalid color: {color}")
    panel = Panel(
        Text(f"{content}", style=text_style, justify=justify),
        title=Text(title, style=f"reverse {color}"),
        title_align = str(justify),
        border_style=Style(color=color),
        expand=expand",
    )
    return panel
