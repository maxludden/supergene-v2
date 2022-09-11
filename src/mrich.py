# src/panel_factory.py

from abc import ABC, abstractmethod
from rich import print, inspect
from rich.console import JustifyMethod
from rich.panel import Panel
from rich.style import Style
from rich.theme import Theme
from rich.text import Text
from rich.table import Table
from rich.columns import Columns
from rich.pretty import pprint
from rich.abc import RichRenderable
from rich.highlighter import RegexHighlighter
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

try:
    from main import console
except ModuleNotFoundError:
    from .main import console
except ImportError:
    from src.main import console
# Max's YAML
try:
    from myaml import yaml
except ModuleNotFoundError:
    from .myaml import yaml
except ImportError:
    from src.myaml import yaml

load_dotenv()


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



class SGHighlighter(RegexHighlighter):
    """Highlighter for Super Gene."""
    
