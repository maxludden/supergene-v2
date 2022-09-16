from pathlib import Path
from rich import print
from rich.text import Text
from rich.panel import Panel
from rich.progress import Progress
from src.log import BASE, console, log
from src.cover import Coverpage, generate_html_path
from src.atlas import sg

def main():
    for book in range(1,11):
        sg()
