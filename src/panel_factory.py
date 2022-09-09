# src/panel_factory.py

from abc import ABC, abstractmethod
from statistics import mode
from turtle import color
from rich import print, inspect
from rich.console import Console
from rich.panel import Panel
from rich.style import Style
from rich.text import Text
from rich.table import Table
from rich.columns import Columns
from rich.pretty import pprint
from rich.abc import RichRenderable
from ujson import dump, dumps, load, loads
from dotenv import load_dotenv
from os import environ

from pydantic import BaseModel, Field, validator, ValidationError
from pydantic.color import Color
from typing import List, Optional, Union, Any, Literal

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

load_dotenv()
console= Console(width=110)
console.clear()

class InvalidColorTheme(ValidationError):
    pass

color_themes = ["white", "off_white", "bg_pushover", "pushover", "bg_blue", "blue", "bg_green", "green", "bg_red", "red", "info", "warning",
    "success", "error"]
with open ('json/color_themes.json', 'r') as infile:
    color_themes_json = load(infile)
color_themes = color_themes_json.keys()

print (color_themes)


class AbstractRich(ABC):
    """
    Abstract class for RichRenderable objects.
    """
    @abstractmethod
    def render(self):
        passWw


class PanelBody(BaseModel):
    content: str = Field(..., description="The content of the panel")
    style: Optional[str] = "white"
    justify: Optional[Literal["left","center","right"]] = "center"

    def __init__(self, content: str, style: Optional[str] = "white", justify: Optional[Literal["left","center","right"]] = "center") -> None:
        self.content = content
        self.style = style
        self.justify = justify

    def get_style(self) -> Style:
        with open ('json/color_themes.json', 'r') as infile:
            color_themes_json = load(infile)
        color_themes = color_themes_json.keys()
        if self.style in color_themes:
            return color_themes_json[self.style]
        else:
            raise ValidationError(f"Invalid color theme: {self.style}", model = PanelBody)

    @validator("content")
    def content_is_str(cls, content: str):
        if not isinstance(content, str):
            raise TypeError(f"Invalid content type: {type(content)}")
        return content

    @validator("style")
    def style_validator(cls, color_theme: str):
        if color_theme not in color_themes:
            color_theme = "blue"
            raise InvalidColorTheme(
                f"Invalid style: {color_theme}",
                model=PanelBody)
        if not color_theme:
            raise InvalidColorTheme(
                "Invalid style: No style provided",
                model=PanelBody
            )
        return color_theme


    @validator("style")
    def style_has_value(cls, color_theme: str):
        if color_theme is None:
            color_theme = "blue"
        return color_theme

    def validate(self):
        try:
            self.content_is_str()
            self.style_validator()
            self.style_has_value()
        except ValidationError as e:
            msg = f"Unable to validate PanelBody: {e}"
            log.error(msg)
            raise e

    def generate(self) -> Text:
        return Text(
            self.content,
            justify = self.justify,
            style = self.get_style()
        )

class PanelTitle(BaseModel):
    content: str
    style: Optional[str] = "white"
    justify: Optional[Literal["left","center","right"]] = "center"

    def __init__(self, content: str, style: Optional[str] = "white", justify: Optional[Literal["left","center","right"]] = "center") -> None:

        self.content = content
        self.style = style
        self.justify = justify


    @validator("content")
    def content_validator(cls, content: Text):
        if not isinstance(content, Text):
            raise TypeError(f"Invalid content type: {type(content)}")
        return content

    @validator("style")
    def style_validator(cls, color_theme: str):
        if color_theme not in color_themes:
            raise InvalidColorTheme(
                f"Invalid style: {color_theme}",
                model=PanelTitle)
        return color_theme

    def generate(self) -> Text:
        return Text(
            self.content,
            justify=self.justify,
            style=self.get_style()
        )

class PanelFactory(BaseModel):
    name: str
    title: str
    body: str
    style: Optional[str] = "white"
    justify: Optional[Literal["left","center","right"]] = "center"
    padding: Optional[int] = 0
    fit: bool = False

    def __init__(self, name: str, title: str, body: str, style: Optional[str] = "white", justify: Optional[Literal["left","center","right"]] = "center", padding: Optional[int] = 0, fit: bool = False) -> None:
        self.name = name
        self.title = title
        self.body = body
        self.style = style
        self.justify = justify
        self.padding = padding
        self.fit = fit


    @validator("name")
    def name_is_string(cls, name: str):
        if not isinstance(name, str):
            raise ValueError("Name must be a string")
        return name

    @validator("title")
    def title_is_str(cls, title: str):
        if not isinstance(title, str):
            raise TypeError(f"Invalid title type: {type(title)}")
        return title

    @validator("body")
    def body_is_str(cls, body: str):
        if not isinstance(body, str):
            raise TypeError(f"Invalid body type: {type(body)}")
        return body

    @validator("style")
    def style_validator(cls, color_theme: str):
        if color_theme not in color_themes:
            raise InvalidColorTheme(
                f"Invalid style: {color_theme}",
                model=PanelBody)
        return color_theme

    def generate(self) -> Panel:
        content = PanelBody(
            name=self.name,
            content=self.body,
            style=self.style,
            justify=self.justify
        )
        title = PanelTitle(
            name=self.name,
            content=self.title,
            style=self.style,
            justify=self.justify
        )
        if self.fit:
            panel = Panel.fit(
                content.generate(),
                title=title.generate(),
                title_align=self.justify,
                padding=self.padding,
                style=self.style,
                expand=True
            )