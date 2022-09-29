# inspect

from inspect import FrameInfo, stack
from pathlib import Path
from rich import print, inspect
from rich.panel import Panel
from rich.text import Text
from rich.style import Style
from rich.table import Table
from rich.box import ROUNDED

# >>> print(stack(context=-1)[0])
# . FrameInfo(
# .      frame=<frame at 0x1063ecba0,
# .      file '/Users/maxludden/dev/py/supergene/src/inspect.py',
# .      line 8,
# .      code <module>>,
# .      filename='/Users/maxludden/dev/py/supergene/src/inspect.py',
# .      lineno=8,
# .      function='<module>',
# .      code_context=None,
# .      index=None
# . )

last_frame = stack(context=-1)[0]  # <- this is the last frame in the stack

# filepath = last_frame.filename
# print(filepath)
# >>> /Users/maxludden/dev/py/supergene/src/inspect.py

# filename = Path(filepath).name
# print(filename)
# >>> inspect.py

# line = last_frame.lineno
# print(line)
# >>> 21

# Create a function to generate frame attributes
def get_frame_filepath(frame: FrameInfo = stack(context=-1)[1]) -> str:
    """A function to get the filepath of a frame. Note that the we are request the the second to last frame in the stack. This is because the last frame in the stack is the frame of the function that called this function."""

    filepath = frame.filename
    path_parts = Path(filepath).parts 
    print(f"[italic cyan]Path Lines:[/] [bold bright_white]{filepath}[/]")

    return filepath


print(get_frame_filepath())


def get_frame_filename(frame: FrameInfo = stack(context=-1)[1]) -> str:
    """A function to get the filename of a frame. Note that the we are request the the second to last frame in the stack. This is because the last frame in the stack is the frame of the function that called this function."""

    filepath = frame.filename
    filename = Path(filepath).name
    return filename


def get_frame_lineno(frame: FrameInfo = stack(context=-1)[1]) -> int:
    """A function to get the line number of a frame. Note that the we are request the the second to last frame in the stack. This is because the last frame in the stack is the frame of the function that called this function."""

    lineno = frame.lineno
    return lineno


def get_frame_info(frame: FrameInfo = stack(context=-1)[1]) -> Panel:
    filename = get_frame_filename()
    filepath = get_frame_filepath()
    lineno = get_frame_lineno()

    table = Table(
        show_header=True,
        header_style="bold magenta",
        width=120,
        box=ROUNDED,
        row_styles=["dim", "none"],
        highlight=True,
        style=Style(color="#5f00ff"),
    )

    table.add_column(
        "Attribute",
        justify="left",
        style=Style(color=f"#eed4fc", bold=True),
        no_wrap=True,
    )
    table.add_column("Value", justify="left", style="bold bright_white", no_wrap=True)
    table.add_row("Filename", filename)
    table.add_row("Filepath", filepath)
    table.add_row("Line Number", f"{lineno}")

    panel = Panel(
        table,
        title="Inspect Frame",
        subtitle=f"[purple]src/book.py[/][#FFFFFF]|[/][#54c6ff]line {line}[/]",
        subtitle_align="right",
        border_style=Style(color="#140c6b"),
        expand=False,
    )
    return panel


# print(get_frame_info())
