from operator import ge, le
import re
from abc import ABC, abstractmethod
from enum import Enum, EnumMeta
from os import environ
from typing import Any, List, Literal, Optional, Union

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError, validator
from pydantic.color import Color as PyColor
from rich import inspect, print
from rich.abc import RichRenderable
from rich.align import AlignMethod
from rich.color import Color
from rich.color import parse_rgb_hex
from rich.columns import Columns
from rich.console import Console, JustifyMethod
from rich.panel import Panel
from rich.pretty import pprint
from rich.style import Style
from rich.table import Table
from rich.text import Text
from rich.theme import Theme
from ujson import dump, dumps, load, loads

from beanie import Document, init_beanie
import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient


load_dotenv()
URI = environ.get("LOCALDB")
DB = environ.get("SUPERGENE_DB")

mconsole = Console()


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

class MyColor(Enum):
    """Color enum."""
    BLACK = 0
    WHITE = 1
    RED = 2
    ORANGE =3
    YELLOW = 4
    GREEN = 5
    CYAN = 6
    BLUE = 7
    PURPLE = 8

