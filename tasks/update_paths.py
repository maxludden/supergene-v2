from pathlib import Path

from rich import inspect, print
from rich.panel import Panel
from rich.progress import Progress
from rich.text import Text
from src.atlas import sg
from src.chapter import Chapter
from src.chapter import generate_html_path as generate_chapter_html_path
from src.chapter import generate_md_path as generate_chapter_md_path
from src.chapter import generate_text_path as generate_chapter_text_path
from src.cover import Coverpage
from src.cover import generate_html_path as generate_cover_html_path
from src.endofbook import EndOfBook
from src.endofbook import generate_html_path as generate_endofbook_html_path
from src.epubmetadata import Epubmeta, generate_epubmeta_filepath, generate_yaml_dir
from maxcolor import console, log, logpanel
