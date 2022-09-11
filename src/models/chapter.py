from pydantic import BaseModel, Field, ValidationError, validator
from pydantic.types import FilePath
from pydantic.networks import HttpUrl
from pydantic.color import Color as PyColor
from beanie import Document, init_beanie, Indexed
import pymongo

class Chapter(Document):
    chapter: Indexed(
        typ=int,
        index_type=pymongo.ASCENDING) = Field(  # type: ignore
            ...,
            description="The chapter number",
            title="Chapter",
            ge=1,
            le=3462
        )
    ) # type: ignore
    section: int = Field(...,
        ge=1,
        le=17,
        description="The section of the book.",
        title="Section")
    book: int = Field(...,
        ge=1,
        le=10,
        description="Book of the chapter.",
        title="Book")
    title: str = Field(...,
        max_length=500,
        description="Title of the chapter.",
        title="Chapter Title")
    text: str = Field(...,
        description="The text of the chapter.",
        title="Chapter Text")
    filename: str = Field(...,
        description="Filename of the chapter.",
        title="Chapter Filename")
    md_path: FilePath = Field(...,
        description="Path to the markdown file.",
        title="Chapter Markdown Path")
    html_path: FilePath = Field(...,
        description="Path to the html file.",
        title="Chapter HTML Path")
    md: str = Field(...,
        description="Markdown of the chapter text.",
        title = "Chapter Markdown")
    html: str = Field(...,
        description="HTML of the chapter text.",
        title="Chapter HTML")
    url: HttpUrl = Field(...,
        description="URL of the chapter text.",
        title="Chapter URL")
    unparsed_text: str = Field(...,
        description="Unparsed text of the chapter.",
        title="Chapter Unparsed Text")
    parsed_text: str = Field(...,
        description="Parsed text of the chapter.",
        title="Chapter Parsed Text")