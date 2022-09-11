from tkinter import ROUND
from pydantic import BaseModel, Field, ValidationError, validator
from pydantic.types import FilePath
from pydantic.networks import HttpUrl
from pydantic.color import Color as PyColor
from beanie import Document, init_beanie, Indexed
import pymongo
from rich.abc import RichRenderable
from rich import print, inspect
from rich.console import Group
from rich.color import Color
from rich.panel import Panel
from rich.style import Style
from rich.text import Text
from rich.table import Table
from rich.box import ROUNDED
from rich.markdown import Markdown


class Chapter(Document):
    chapter: int = Field(
        ..., description="The chapter number", title="Chapter", ge=1, le=3462
    )
    section: int = Field(
        ..., ge=1, le=17, description="The section of the book.", title="Section"
    )
    book: int = Field(
        ..., ge=1, le=10, description="Book of the chapter.", title="Book"
    )
    title: str = Field(
        ..., max_length=500, description="Title of the chapter.", title="Chapter Title"
    )
    text: str = Field(..., description="The text of the chapter.", title="Chapter Text")
    filename: str = Field(
        ..., description="Filename of the chapter.", title="Chapter Filename"
    )
    md_path: FilePath = Field(
        ..., description="Path to the markdown file.", title="Chapter Markdown Path"
    )
    html_path: FilePath = Field(
        ..., description="Path to the html file.", title="Chapter HTML Path"
    )
    md: str = Field(
        ..., description="Markdown of the chapter text.", title="Chapter Markdown"
    )
    html: str = Field(
        ..., description="HTML of the chapter text.", title="Chapter HTML"
    )
    url: HttpUrl = Field(
        ..., description="URL of the chapter text.", title="Chapter URL"
    )
    unparsed_text: str = Field(
        ..., description="Unparsed text of the chapter.", title="Chapter Unparsed Text"
    )
    parsed_text: str = Field(
        ..., description="Parsed text of the chapter.", title="Chapter Parsed Text"
    )

    class DocumentMeta:
        collection_name = "chapter"
    class Settings:
        name = "chapter"
        indexes = [
            [
                ("chapter", pymongo.ASCENDING),
                ("section", pymongo.ASCENDING),
                ("book", pymongo.ASCENDING),
                ("title", pymongo.TEXT),
            ]
        ]

Chapter.update_forward_refs()

def __rich_repr__(self) -> Group:
        """Rich representation of the chapter."""
        chapter_table = Table(
            title=f"Chapter {self.chapter}",
            title_style="bold purple",
            show_header=False,
            show_lines=False,
            box=ROUNDED,
            row_styles=["dim", ""],
            expand=True,
        )

        chapter_table.add_column("Keys", style="italic bluepurple", justify="left")
        chapter_table.add_column(
            "Values",
            style="bold bright_white",
        )
        chapter_table.add_row("Chapter", f"{self.chapter}")
        chapter_table.add_row("Section", f"{self.section}")
        chapter_table.add_row("Book", f"{self.book}")
        chapter_table.add_row("Title", f"{self.title}")
        chapter_table.add_row("Filename", f"{self.filename}")
        chapter_table.add_row("Markdown Path", f"{self.md_path}")
        chapter_table.add_row("HTML Path", f"{self.html_path}")
        chapter_table.add_row("URL", f"{self.url}")

        md = Markdown(self.md)
        md_panel = Panel(md, title="Markdown", border_style="bold bluepurple")
        result = Group(chapter_table, md_panel)
        return result
