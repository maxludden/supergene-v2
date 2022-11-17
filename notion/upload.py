from datetime import datetime
from os import environ
from pathlib import Path

from dotenv import load_dotenv
from maxcolor import gradient, gradient_panel
from maxconsole import get_console, get_theme
from maxprogress import get_progress
from requests import request
from rich.markdown import Markdown
from rich.panel import Panel
from rich.pretty import pprint
from rich.text import Text
from ujson import dump, dumps, load, loads

from notion.client import NotionClient
from src.atlas import sg
from src.chapter import Chapter, chapter_gen

console = get_console(get_theme())

CWD = Path.cwd()
CHAPTERS_DIR = CWD / "notion" / "chapters"
PAGE = CWD / "notion" / "page_props.py"

database_id = "dbc4f31d755a4c36824630532a831a74"
token = "secret_FzXQ3Xd1wB5Tg1Qr0gsLAW8OsfiU2LKlBFwE2ClhSIL"
headers = {
    "Authorization": f"Bearer {token}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}


def read_chapter(database_id: str, headers: dict):
    """Reads the chapter from the database."""
    read_url = f"https://api.notion.com/v1/databases/{database_id}/query"
    response = request("POST", read_url, headers=headers)

    with open(CHAPTERS_DIR / "example.json", "w") as outfile:
        dump(response.json(), outfile, indent=4)

    console.print(
        gradient_panel(
            "Chapter read successfully.", title="Notion", padding=(1, 4), expand=False
        )
    )
    return loads(response.text)


def create_chapter(database_id: str, headers: dict, chapter: int):
    """Creates a chapter in the database."""
    sg()
    chapter = Chapter.objects(chapter=chapter).first()  # type: ignore

    create_url = f"https://api.notion.com/v1/pages"
    data = {
        "parent": {"database_id": database_id},
        "properties": {
            "chapter": {"title": [{"text": {"content": chapter.chapter}}]},
            "section": {"Quantity": {"number": chapter.section}},
            "book": {"Quantity": {"number": chapter.section}},
            "filename": {"rich_text": [{"text": {"content": chapter.filename}}]},
            "title": {"rich_text": [{"text": {"content": chapter.title}}]},
            "url": {"Website": {"url": chapter.url}},
            "text_path": {"rich_text": [{"text": {"content": chapter.text_path}}]},
            "md_path": {"rich_text": [{"text": {"content": chapter.md_path}}]},
            "html_path": {"rich_text": [{"text": {"content": chapter.html_path}}]},
            "unparsed_text": {
                "rich_text": [{"text": {"content": chapter.unparsed_text}}]
            },
            "parsed_text": {"rich_text": [{"text": {"content": chapter.parsed_text}}]},
            "text": {"rich_text": [{"text": {"content": chapter.text}}]},
            "md": {"rich_text": [{"text": {"content": chapter.md}}]},
            "html": {"rich_text": [{"text": {"content": chapter.html}}]},
            "tags": {"multi_select": [{"name": tag} for tag in chapter.tags]},
        },
    }
    response = request("POST", create_url, headers=headers, json=data)
    if response.status_code == 200:

        with open(CHAPTERS_DIR / "example.json", "w") as outfile:
            dump(response.json(), outfile, indent=4)

        console.print(
            gradient_panel(
                f"Chapter created successfully.\n\n {response}",
                title="Notion",
                padding=(1, 4),
                expand=False,
            )
        )
    else:
        console.print(
            Panel(
                f"Chapter creation failed.\n\n{response}",
                title=f"[bold bright_white]Error {response.status_code}[/]",
                padding=(1, 4),
                expand=False,
                style="bold bright_red",
            )
        )
        return loads(response.text)
