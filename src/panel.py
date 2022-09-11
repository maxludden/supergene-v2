from pydantic import BaseModel, Field, ValidationError, validator
from pydantic.types import FilePath
from pydantic.networks import HttpUrl
from pydantic.color import Color
from rich.console import Console, JustifyMethod
from rich.panel import Panel
from rich.text import Text
from rich.style import Style
from rich.color import Color as RichColor
from beanie import Document, init_beanie, Indexed
import pymongo

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



class MyPanel(Document):
    color: Color = Field(..., description="Color of the panel.")
    title: str = Field(..., description="Title of the panel.")
    text: str = Field(..., description="Text of the panel.")
    expand: bool = Field(True, description="Expand the panel.")
    justify: JustifyMethod = Field('center', description="Justify the panel.")

    def generate(self) -> Panel:
        panel = Panel(
            Text(
                self.text,
                style=Style(
                    color = "white",
                    bold=True)
            ),
            title=Text(self.title),
            style=Style(
                color = self.color, # type: ignore
                bold=True)
            )
        return panel

    class Config:
        orm_mode = True

    class Settings:
        name = "panels"