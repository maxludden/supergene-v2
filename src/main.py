from lib2to3.pytree import Base
from os import environ

from beanie import init_beanie
from dotenv import load_dotenv
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings
from rich import inspect, print
from rich.console import Console
from rich.style import Style
from rich.theme import Theme

from chapter import Chapter
from log import log
from myaml import dump, load, safe_dump, safe_load
from routes import chapter_router

app = FastAPI()

max_theme = Theme(
    {
        "debug": "bold bright_cyan",  #             #00ffff
        "info": "bold cornflower_blue",  #          #249df1
        "success": "bold bright_green",  #          #00ff00
        "warning": "bold bright_yellow",  #         #ffff00
        "error": "bold orange1",  #                 #ff8800
        "critical": "bold reverse bright_red",  #   #ff0000
        "key": "italic blue_violet",  #             #5f00ff
        "value": "bold bright_white",  #            #ffffff
        "title": "bold purple",  #                  #af00ff
    }
)

console = Console(theme=max_theme)

class Settings(BaseSettings):
    mongodb_url = 'mongodb://localhost:27017/SUPERGENE'


@app.on_event("startup")
async def app_int():
    client = AsyncIOMotorClient(Settings().mongodb_url)
    await init_beanie(client.get_default_database(), document_models=[Chapter])
    app.include_router(chapter_router, prefix='/v1')
