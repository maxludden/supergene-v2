#max_logger/color.py
import re
from random import choice
from typing import Tuple

from rich.color import Color
from rich.color_triplet import ColorTriplet
from rich.console import Console
from rich.panel import Panel
from rich.progress import (BarColumn, MofNCompleteColumn, Progress,
                           SpinnerColumn, TextColumn, TimeElapsedColumn,
                           TimeRemainingColumn)
from rich.table import Column
from rich.text import Text
from rich.theme import Theme
from rich.traceback import install

theme = Theme(
    {
        "debug": "bold bright_cyan",
        "cyan": "#00ffff",
        "info": "bold cornflower_blue",
        "cornflower_blue": "#249df1",
        "blue": "bold #0000FF",
        "success": "bold bright_green",
        "green": "#00ff00",
        "warning": "bold bright_yellow",
        "yellow": "#ffff00",
        "error": "bold orange1",
        "orange": "#ff8800",
        "critical": "bold reverse #F00000",
        "red": "#ff0000",
        "key": "italic blue_violet",
        "blue_violet": "#5f00ff",
        "value": "bold bright_white",
        "white": "#ffffff",
        "title": "bold purple",
        "purple": "#af00ff",
    }
)

# . Console
console = Console(theme=theme)

# , Traceback
install(console=console)

# . Progress
text_column = TextColumn("[progress.description]{task.description}")
spinner_column = SpinnerColumn()
bar_column = BarColumn(
    bar_width=None, finished_style="green", table_column=Column(ratio=3)
)
mofn_column = MofNCompleteColumn()
time_elapsed_column = TimeElapsedColumn()
time_remaining_column = TimeRemainingColumn()
progress = Progress(
    text_column,
    spinner_column,
    bar_column,
    mofn_column,
    time_elapsed_column,
    time_remaining_column,
    console=console,
    transient=True,
    refresh_per_second=10,
    auto_refresh=True,
)

def parse_rgb_hex(hex_color: str) -> ColorTriplet:
    """Parse a hex color string into a ColorTriplet.
    Args:
        hex_color (str):
            The hex color string to be parsed.
    Returns:
        ColorTriplet:
            The parsed ColorTriplet.
    """
    assert len(hex_color) == 6, "must be 6 characters"
    color = ColorTriplet(
        int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    )
    return color


class InvalidHexColor(Exception):
    """Raised when a hex color string is invalid."""
    pass

def gradient(message: str, color1: str, color2: str) -> Text:
    """Print text with a gradient."""
    text = Text(message)

    # . Add `#` to the HEX color if it is missing.
    if '#' not in color1:
        color1 = f"#{color1}"
    if '#' not in color2:
        color2 = f"#{color2}"

    # , Validate Hex Color
    hex_regex = re.compile(r"^#(?:[0-9a-fA-F]{3}){1,2}$")
    if hex_regex.match(color1) and hex_regex.match(color2):
        color1 = Color.parse(color1).triplet # type: ignore
        color2 = Color.parse(color2).triplet # type: ignore

        # . Color1's RGB values
        r1 = int(color1[0])
        g1 = int(color1[1])
        b1 = int(color1[2])

        # , Color2's RGB values
        r2 = int(color2[0])
        g2 = int(color2[1])
        b2 = int(color2[2])

        # . Calculate the difference between the two colors.
        dr = r2 - r1
        dg = g2 - g1
        db = b2 - b1

        size = len(text)
        for index in range(size):
            blend = index / size
            color = f"#{int(r1 + dr * blend):02X}{int(g1 + dg * blend):02X}{int(b1 + db * blend):02X}"
            text.stylize(color, index, index + 1)
        return text

    else:
        if not hex_regex.match(color1) and not hex_regex.match(color2):
           raise InvalidHexColor(f"Invalid hex colors: {color1} and {color2}")
        elif not hex_regex.match(color1):
            raise InvalidHexColor(f"Invalid hex color: {color2}")
        else:
            raise InvalidHexColor(f"Invalid hex color: {color1}")

def rgb_gradient(
    message: str, color1: Tuple[int, int, int], color2: Tuple[int, int, int]
) -> Text:
    """Blend text from one color to another."""
    text = Text(message)
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    dr = r2 - r1
    dg = g2 - g1
    db = b2 - b1
    size = len(text)
    for index in range(size):
        blend = index / size
        color = f"#{int(r1 + dr * blend):02X}{int(g1 + dg * blend):02X}{int(b1 + db * blend):02X}"
        text.stylize(color, index, index + 1)
    return text



def rainbow(message: str, num_of_gradients: int = 7) -> Text:
    """Rainbow text."""
    red = "#ff0000"
    orange = "#ff7f00"
    yellow = "#ffff00"
    green = "#00ff00"
    blue = "#61bdff"
    violet = "#7f00ff"
    magenta = "#ff00ff"
    colors1 = [red, orange, yellow, green, blue, violet, magenta]
    colors2 = [orange, yellow, green, blue, violet, magenta, red]
    colors3 = [yellow, green, blue, violet, magenta, red, orange]
    colors4 = [green, blue, violet, magenta, red, orange, yellow]
    colors5 = [blue, violet, magenta, red, orange, yellow, green]
    colors6 = [violet, magenta, red, orange, yellow, green, blue]
    colors7 = [magenta, red, orange, yellow, green, blue, violet]
    colors = [colors1, colors2, colors3, colors4, colors5, colors6, colors7]

    rainbow = choice(colors)
    text = Text(message)
    size = len(text)

    if num_of_gradients > 7:
        num_of_gradients = 7
    gradient_size = size // (num_of_gradients - 1)
    gradient_text = Text()

    for index in range(0, num_of_gradients):
        begin = index * gradient_size
        end = (index + 1) * gradient_size
        sub_text = text[begin:end]

        if index < 6:
            color1 = Color.parse(rainbow[index])
            color1_triplet = color1.triplet
            r1 = color1_triplet[0]  # type: ignore
            g1 = color1_triplet[1]  # type: ignore
            b1 = color1_triplet[2]  # type: ignore
            color2 = Color.parse(rainbow[index + 1])
            color2_triplet = color2.triplet
            r2 = color2_triplet[0]  # type: ignore
            g2 = color2_triplet[1]  # type: ignore
            b2 = color2_triplet[2]  # type: ignore
            dr = r2 - r1
            dg = g2 - g1
            db = b2 - b1

        for index in range(gradient_size):
            blend = index / gradient_size
            color = f"#{int(r1 + dr * blend):02X}{int(g1 + dg * blend):02X}{int(b1 + db * blend):02X}"  # type: ignore
            sub_text.stylize(color, index, index + 1)
        gradient_text = Text.assemble(gradient_text, sub_text)

    return gradient_text


def magenta_orange(text: str) -> Text:
    """Magenta to orange gradient."""
    length = len(text)
    mid = length // 2
    text1 = text[:mid]
    text2 = text[mid:]

    # Magenta to Red
    text1 = rgb_gradient(text1, (255, 0, 255), (255, 0, 0))
    # Red to Orange
    text2 = rgb_gradient(text2, (255, 0, 0), (255, 127, 0))
    return Text.assemble(text1, text2)


def gradient_panel(text: str, title: str | None = None, colors: int = 4) -> Panel:
    """Gradient panel."""
    if colors <=7:
        gradient_text = rainbow(text, colors)

    else:
        raise ValueError(f"Invalid number: {colors}. Colors must be an integer between 1 and 7.")

    if title:
        return Panel(
            gradient_text,
            title = f"[bold bright_white]{title}[/bold bright_white]",
            title_align = "left",
            border_style = "bright_white",
            expand = False,
            style = "bold"
        )
    else:
        return Panel(
            gradient_text,
            border_style = "bright_white",
            expand = False,
            style = "bold"
        )
