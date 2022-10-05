import atexit
import math
import sys
import time
from signal import SIG_DFL, SIGPIPE, signal
from typing import Any, Optional, TextIO
from io import StringIO

from rich.color import Color, parse_rgb_hex
from rich import print
from rich.panel import Panel
from rich.traceback import install
from pathlib import Path
from src.log import BASE, log, console

import random
import re

ph_path = BASE / "tasks" / "lorem.txt"
with open(ph_path, "r") as infile:
    placeholder = infile.read()


PY3 = sys.version_info >= (3,)

# override default handler so no exceptions on SIGPIPE
signal(SIGPIPE, SIG_DFL)

# Reset terminal colors at exit
def reset():
    sys.stdout.write("\x1b[0m")
    sys.stdout.flush()


atexit.register(reset)


STRIP_ANSI = re.compile(r"\x1b\[(\d+)(;\d+)?(;\d+)?[m|K]")
COLOR_ANSI = (
    (0x00, 0x00, 0x00),
    (0xCD, 0x00, 0x00),
    (0x00, 0xCD, 0x00),
    (0xCD, 0xCD, 0x00),
    (0x00, 0x00, 0xEE),
    (0xCD, 0x00, 0xCD),
    (0x00, 0xCD, 0xCD),
    (0xE5, 0xE5, 0xE5),
    (0x7F, 0x7F, 0x7F),
    (0xFF, 0x00, 0x00),
    (0x00, 0xFF, 0x00),
    (0xFF, 0xFF, 0x00),
    (0x5C, 0x5C, 0xFF),
    (0xFF, 0x00, 0xFF),
    (0x00, 0xFF, 0xFF),
    (0xFF, 0xFF, 0xFF),
)

install()

ANSI_SEQ = "\x1b[{}m"
FG_RGB = "38;2;{};{};{}"
BG_RGB = "48;2;{};{};{}"
RESET = "0"
FRAMED = "51"

ATTRS = {
    key: code
    for key, code in [
        line.strip().split()
        for line in """\
    bold 1
    faint 2
    italic 3
    underline 4
    blink 5
    fast_blink 6
    reverse 7
    conceal 8
    crossed 9
    fraktur 20
    double_underline 21
    framed 51
    encircled 52
    overlined 54\
""".split(
            "\n"
        )
    ]
}


def printc(*args, **kw):
    """Extends print function to add color printing parameters in compatible terminals.

    Use the optional bg= or fg= parameters to pass colors for foreground or background
    respectively. Parameters should be a 3-sequence with RGB numbers from 0 to 255
    as string or decimal.
    Use the optional end_fg and end_bg parameters to create color gradients
    from the starting color to the ending ones.

    Other attributes can be accepted as "True" according  the keys in ATTRS

    """
    extra_options = {}
    for argname, value in list(kw.items()):
        if argname in ATTRS:
            extra_options[argname] = kw.pop(argname)

    fg_param = kw.pop("start_fg", kw.pop("fg", None))
    bg_param = kw.pop("start_bg", kw.pop("bg", None))

    start_fg = fg = tuple(int(comp) for comp in (fg_param if fg_param else (0, 0, 0)))
    start_bg = bg = tuple(int(comp) for comp in (bg_param if bg_param else (0, 0, 0)))

    end_fg = tuple(int(comp) for comp in kw.pop("end_fg", fg))
    end_bg = tuple(int(comp) for comp in kw.pop("end_bg", bg))

    original_file = kw.pop("file", sys.stdout)
    original_flush = kw.pop("flush", False)
    original_end = kw.pop("end", None)
    text_io = StringIO()
    print(*args, **kw, file=text_io, end="")
    text = text_io.getvalue()

    if not fg_param and not bg_param or not len(text):
        return print(*args, **kw)

    fg_gradient = start_fg != end_fg
    bg_gradient = start_bg != end_bg

    text_io = StringIO()

    extra_attrs = ";".join(ATTRS[key] for key in extra_options)
    if extra_attrs:
        text_io.write(ANSI_SEQ.format(extra_attrs))
    for i, character in enumerate(text):
        ansi_str = ""
        if start_fg and (i == 0 or fg_gradient):
            ansi_str = FG_RGB.format(*fg)

        if start_bg and (i == 0 or bg_gradient):
            ansi_str += (";" if ansi_str else "") + BG_RGB.format(*bg)

        if ansi_str:
            text_io.write(ANSI_SEQ.format(ansi_str))

        text_io.write(character)

        fg = tuple(
            int(comp + i * (end_comp - comp) / len(text))
            for comp, end_comp in zip(fg, end_fg)
        )
        bg = tuple(
            int(comp + i * (end_comp - comp) / len(text))
            for comp, end_comp in zip(bg, end_bg)
        )

    text_io.write(ANSI_SEQ.format(RESET))

    return print(
        text_io.getvalue(),
        end=str(original_end),
        flush=original_flush,
        file=original_file,
    )


def fg_rainbow(
    text: str | list[str], fg_start: str = "#ffd900", fg_end: str = "#ec00f0"
) -> None:
    """
    Returns the text with a rainbow gradient from
    fg_start (defaults to `bright_red` #F00F00) to
    fg_end (defaults to `magenta` #F00F00)
    """
    # Guarantees any lists are converted into a string with newlines.
    if isinstance(text, list):
        text = "\n".join(text)

    # Converts the hex colors into RGB tuples.
    start_hex = fg_start.replace("#", "")
    start_rgb = parse_rgb_hex(start_hex)

    end_hex = fg_end.replace("#", "")
    end_rgb = parse_rgb_hex(end_hex)

    text_io = StringIO()
    printc(text, start_fg=start_rgb, end_fg=end_rgb, file=text_io)
    print(text_io.getvalue())


# # fg_rainbow("HLorem sit veniam qui proident enim laborum mollit duis amet eiusmod nulla culpa tempor ea. Officia dolore aliquip velit sint anim. Dolor fugiat non in sint anim commodo occaecat culpa labore commodo nisi reprehenderit. Exercitation reprehenderit non Lorem mollit proident in ea dolore duis deserunt aute enim. Culpa officia pariatur quis duis tempor officia dolor. Magna aliqua nostrud eu reprehenderit nisi. Deserunt consectetur in aliqua eiusmod et sit nostrud mollit mollit velit cupidatat Lorem duis. Adipisicing ut sint reprehenderit adipisicing nostrud esse ad laborum nisi nulla elit minim tempor ullamco in. Amet do eu proident eiusmod. Nulla mollit in enim ut exercitation.")
# printc(
#     "Lorem sit veniam qui proident enim laborum mollit duis amet eiusmod nulla culpa tempor ea. Officia dolore aliquip velit sint anim. Dolor fugiat non in sint anim commodo occaecat culpa labore commodo nisi reprehenderit. Exercitation reprehenderit non Lorem mollit proident in ea dolore duis deserunt aute enim. Culpa officia pariatur quis duis tempor officia dolor. Magna aliqua nostrud eu reprehenderit nisi. Deserunt consectetur in aliqua eiusmod et sit nostrud mollit mollit velit cupidatat Lorem duis. Adipisicing ut sint reprehenderit adipisicing nostrud esse ad laborum nisi nulla elit minim tempor ullamco in. Amet do eu proident eiusmod. Nulla mollit in enim ut exercitation.",
#     start_fg=(255, 0, 0),
#     end_fg=(0, 0, 255),
# )


def hex_rgb(hex_color: str) -> Color:
    hex_color = str(hex_color)
    if "#" in hex_color:
        hex_color = hex_color.replace("#", "")
    color_triplet = parse_rgb_hex(hex_color)
    rgb = Color.from_triplet(color_triplet)
    return rgb


# > Gradient Options Global Dict
os = random.randint(0, 256)
fresh_options = {"seed": 0, "freq": 0.1, "spread": 3.0, "force": False, "os": os}m


class Gradient(object):
    """
    Returns the text with a rainbow gradient from
    fg_start (defaults to `bright_red` #ff0000) to
    fg_end (defaults to `magenta` #F00000)
    """

    buf: str
    mode: int
    output: TextIO
    seed: int
    freq: float
    spread: float
    force: bool
    os: int
    options: dict[str, Any]

    def __init__(
        self,
        buf: str,
        mode: int = 256,
        output: TextIO = sys.stdout,
        seed: int = 0,
        spread: float = 3.0,
        freq: float = 0.1,
        force: bool = False,
        os: int = 0,
        options: dict = fresh_options,
    ):
        """
        Initialize a new Gradient object.

        Parameters
        ----------
        buf : `str`
            The text to apply the gradient to.
        mode : `int`, optional
            ColorType, by default 256
        output : `TextIO`, optional
            The stream to output the text to, by default sys.stdout
        seed : `int`, optional
            Gradient seed, by default 0
        spread : `float`, optional
            How much spread is in the gradient, by default 3.0
        freq : `float`, optional
            The freqency of the gradient, by default 0.1
        force : `bool`, optional
            Force color even if the ternimal is not TTY, by default False
        os : `int`, optional
            Random Integer, by default [[random.randint(0, 256) if self.seed == 0 else options.seed]]options:dict=fresh_options
        """
        self.buf = buf
        self.mode = mode
        self.output = output
        self.options = options
        if seed != 0:
            self.seed = seed
        if freq != 0.1:
            self.freq = freq
        if spread != 3.0:
            self.spread = spread
        if force:
            self.force = True
        if os != 0:
            self.os = os
        else:
            self.force = False

    def get_options(self) -> dict:
        options = {
            "seed": self.seed,
            "freq": self.freq,
            "spread": self.spread,
            "force": self.force,
            "os": self.os,
        }
        return options

    def set_options(self, options: dict) -> None:
        self_options = self.get_options()
        if options != self_options:
            self.options = options
        if options["seed"] != self.seed:
            self.seed = options["seed"]
        elif options["freq"] != self.freq:
            self.freq = options["freq"]
        elif options["spread"] != self.spread:
            self.spread = options["spread"]
        elif options["force"] != self.force:
            self.force = options["force"]
        elif options["os"] != self.os:
            self.os = options["os"]

    def _distance(self, rgb1, rgb2) -> int:
        return sum(map(lambda c: (c[0] - c[1]) ** 2, zip(rgb1, rgb2)))

    def ansi(self, rgb) -> str:
        r, g, b = rgb

        color = sum(
            [16]
            + [int(6 * float(val) / 256) * mod for val, mod in zip(rgb, [36, 6, 1])]
        )

        return "38;5;%d" % (color,)

    def wrap(self, *codes) -> str:
        return "\x1b[%sm" % ("".join(codes),)

    def rainbow(self, freq, i) -> list[float]:
        r = math.sin(freq * i) * 127 + 128
        g = math.sin(freq * i + 2 * math.pi / 3) * 127 + 128
        b = math.sin(freq * i + 4 * math.pi / 3) * 127 + 128
        return [r, g, b]

    def cat(self, fd, options):
        for line in fd:
            options.os += 1
            self.println(line, options)

    def println(self, s, options):
        s = s.rstrip()
        if self.force or self.output.isatty():
            s = STRIP_ANSI.sub("", s)

        if self.mode == 256:
            self.println_plain(s, options)

        self.output.write("\n")
        self.output.flush()

    # def println_ani(self, s, options):
    #     if not s:
    #         return

    #     for i in range(1, options.duration):
    #         self.output.write("\x1b[%dD" % (len(s),))
    #         self.output.flush()
    #         options.os += self.spread
    #         self.println_plain(s, options)
    #         time.sleep(1.0 / options.speed)

    def println_plain(self, s):
        for i, c in enumerate(s):
            rgb = self.rainbow(self.freq, self.os + i / self.spread)
            self.output.write("".join([str(self.wrap(self.ansi(rgb))), c]))


text = Gradient(placeholder)
text.println(text.buf, text.get_options)
