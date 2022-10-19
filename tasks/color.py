import random
from io import StringIO
from pathlib import Path
from signal import SIG_DFL, SIGPIPE, signal
from typing import Any, Optional, TextIO, Tuple

import rich
from rich import print
from rich.color import Color, blend_rgb, parse_rgb_hex
from rich.panel import Panel
from rich.pretty import pprint
from rich.text import Text
from rich.traceback import install
from src.log import BASE, console, log, progress
from sh import Command

lorem = """Sint adipisicing consequat cillum dolor commodo quis pariatur ea aute consequat.\nUt id occaecat culpa aute consectetur culpa consequat commodo commodo non ad est. \nOfficia ut est aute enim. Proident sunt anim ut. Irure nostrud id est elit quis velit \naute Lorem."""


def gradient(
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

def rainbow(message: str) -> Text:
    """Rainbow text."""
    red =       "#ff0000"
    orange =    "#ff7f00"
    yellow =    "#ffff00"
    green =     "#00ff00"
    blue =      "#61bdff"
    violet =    "#7f00ff"
    magenta =   "#ff00ff"
    colors1 = [red, orange, yellow, green, blue, violet, magenta]
    colors2 = [orange, yellow, green, blue, violet, magenta, red]
    colors3 = [yellow, green, blue, violet, magenta, red, orange]
    colors4 = [green, blue, violet, magenta, red, orange, yellow]
    colors5 = [blue, violet, magenta, red, orange, yellow, green]
    colors6 = [violet, magenta, red, orange, yellow, green, blue]
    colors7 = [magenta, red, orange, yellow, green, blue, violet]
    colors = [colors1, colors2, colors3, colors4, colors5, colors6, colors7]

    rainbow = random.choice(colors)
    text = Text(message)
    size = len(text)
    gradient_size = size // 6
    gradient_text = Text()

    for index in [0,1,2,3,4,5,6]:
        begin = index * gradient_size
        end = (index + 1) * gradient_size
        sub_text = text[begin:end]

        if index < 6:
            color1 = Color.parse(rainbow[index])
            color1_triplet = color1.triplet
            r1 = color1_triplet[0] # type: ignore
            g1 = color1_triplet[1] # type: ignore
            b1 = color1_triplet[2] # type: ignore
            color2 = Color.parse(rainbow[index+1])
            color2_triplet = color2.triplet
            r2 = color2_triplet[0] # type: ignore
            g2 = color2_triplet[1] # type: ignore
            b2 = color2_triplet[2] # type: ignore
            dr = r2 - r1
            dg = g2 - g1
            db = b2 - b1

        for index in range(gradient_size):
            blend = index / gradient_size
            color = f"#{int(r1 + dr * blend):02X}{int(g1 + dg * blend):02X}{int(b1 + db * blend):02X}" # type: ignore
            sub_text.stylize(color, index, index + 1)
        gradient_text = Text.assemble(gradient_text, sub_text)

    return gradient_text

def magenta_orange(text: str) -> Text:
    """Magenta to orange gradient."""
    length = len (text)
    mid = length // 2
    text1 = text[:mid]
    text2 = text[mid:]

    # Magenta to Red
    text1 = gradient(text1, (255, 0, 255), (255, 0, 0))
    # Red to Orange
    text2 = gradient(text2, (255, 0, 0), (255, 127, 0))
    return Text.assemble(text1, text2)

# console.print(
#     magenta_orange(
#         f"♥  Max Ludden is cool ♥\n\n{lorem}",
#         # Color.parse("#ff0000").triplet, # type: ignore
#         # Color.parse("#c300ff").triplet, # type: ignore
#     ),
#     justify="center",
#     style="bold"
# )

