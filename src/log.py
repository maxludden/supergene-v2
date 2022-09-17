# src/log.py

from functools import wraps
from os import environ
from pathlib import Path
from platform import platform
from time import perf_counter

from loguru import logger as log
from rich import inspect, print
from rich.console import Console
from rich.panel import Panel
from rich.pretty import pprint
from rich.style import Style
from rich.text import Text
from rich.theme import Theme
from ujson import dump, load

mconsole = Console()


# > BASE
def generate_base():
    """Generate base directory for the project."""
    BASE = Path.cwd()
    return BASE
BASE = generate_base()


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

# > Current Run
def get_last_run() -> int:
    """
    Get the last run of the script.
    """
    with open("json/run.json", "r") as infile:
        last_run_dict = dict(load(infile))
    return int(last_run_dict["run"])


def increment_run(last_run: int) -> int:
    """
    Increment the last run of the script.
    """
    run = last_run + 1
    return run


def record_run(run: int) -> None:
    """
    Record the last run of the script.
    """
    run = {"run": run}  # type: ignore
    with open("json/run.json", "w") as outfile:
        dump(run, outfile, indent=4)


def new_run() -> int:
    """
    Create a new run of the script.
    """
    # > RUN
    last_run = get_last_run()
    run = increment_run(last_run)
    record_run(run)

    # > Clear and initialize console
    mconsole.clear()
    return run

current_run = new_run()
console.rule(title=f"\n\n\nRun {current_run}\n\n\n")


# > Configure Loguru Logger Sinks
sinks = log.configure(
    handlers=[
        dict(  # . debug.log
            sink=f"{BASE}/logs/debug.log",
            level="DEBUG",
            format="Run {extra[run]} | {time:hh:mm:ss:SSS A} | {file.name: ^13} |  Line {line: ^5} | {level: <8}ﰲ  {message}",
            rotation="10 MB",
        ),
        dict(  # . info.log
            sink=f"{BASE}/logs/info.log",
            level="INFO",
            format="Run {extra[run]} | {time:hh:mm:ss:SSS A} | {file.name: ^13} |  Line {line: ^5} | {level: <8}ﰲ  {message}",
            rotation="10 MB",
        ),
        dict(  # . Rich Console Log > INFO
            sink=(
                lambda msg: console.log(
                    msg, markup=True, highlight=True, log_locals=False
                )
            ),
            level="INFO",
            format="Run {extra[run]} | {time:hh:mm:ss:SSS A} | {file.name: ^13} |  Line {line: ^5} | {level: ^8} ﰲ  {message}",
        ),
        dict(  # . Rich Console Log > ERROR
            sink=(
                lambda msg: console.log(
                    msg, markup=True, highlight=True, log_locals=True
                )
            ),
            level="ERROR",
            format="Run {extra[run]} | {time:hh:mm:ss:SSS A} | {file.name: ^13} |  Line {line: ^5} | {level: ^8} ﰲ  {message}",
            diagnose=True,
            catch=True,
            backtrace=True,
        ),
    ],
    extra={"run": current_run},  # > Current Run
)

log.debug("Initialized Logger")
# End of handlers

# > Decorators
@log.catch
def check(
    *,
    entry=True,
    exit=True,
    level="DEBUG",
):
    """Create a decorator that can be used to record the entry, *args, **kwargs,as well ass the exit and results of a decorated function.

    Args:
        entry (bool, optional):
            Should the entry , *args, and **kwargs of given decorated function be logged? Defaults to True.

        exit (bool, optional):
            Should the exit and the result of given decorated function be logged? Defaults to True.

        level (str, optional):
            The level at which to log to be recorded.. Defaults to "DEBUG".
    """

    def wrapper(func):
        name = func.__name__
        log.debug(f"Checking function {name}.")

        @wraps(func)
        def wrapped(*args, **kwargs):
            check_log = log.opt(depth=1)
            if entry:
                check_log.log(
                    level,
                    f"Entering '{name}'\n<code>\nargs:\n{args}'\nkwargs={kwargs}</code>",
                )
            result = func(*args, **kwargs)
            if exit:
                check_log.log(
                    level, f"Exiting '{name}'<code>\nresult:\n<{result}</code>"
                )
            return result

        return wrapped

    return wrapper


def time(*, level="DEBUG"):
    """Create a decorator that can be used to record the entry and exit of a decorated function.
    Args:
        level (str, optional):
            The level at which to log to be recorded.. Defaults to "DEBUG".
    """

    def wrapper(func):
        name = func.__name__
        log.debug(f"Timing function {name}.")

        @wraps(func)
        def wrapped(*args, **kwargs):
            time_log = log.opt(depth=1)
            start = perf_counter()
            result = func(*args, **kwargs)
            end = perf_counter()
            time_log.log(level, f"{name} took {end - start} seconds.")
            return result

        return wrapped

    return wrapper


def logpanel(msg: str, level: str = "INFO") -> None:
    """Log a message to loguru sinks and print to a panel.
    Args:
        msg (str):
            The message to be logged.
    """
    match level:
        case "DEBUG" | 'debug' | 'd':
            panel = Panel(
                Text(
                    msg,
                    style="bold bright_white"
                ),
                title=Text(
                    "DEBUG",
                    style="debug",
                ),
                title_align="left",
                border_style="debug",
                padding=(1, 1),
                expand=False,
            )
            console.log(panel, markup=True, highlight=True, log_locals=False)
            log.debug(msg)
        case "INFO" | 'info' | 'i':
            panel = Panel(
                Text(
                    msg,
                    style="bold bright_white"
                ),
                title=Text(
                    "INFO",
                    style="info",
                ),
                title_align="left",
                border_style="info",
                padding=(1, 1),
                expand=False,
            )
            console.log(panel, markup=True, highlight=True, log_locals=False)
            log.info(msg)
        case "WARNING" | 'warning' | 'w':
            panel = Panel(
                Text(
                    msg,
                    style="bold bright_white"
                ),
                title=Text(
                    "WARNING",
                    style="warning",
                ),
                title_align="left",
                border_style="warning",
                padding=(1, 1),
                expand=False
            )
            console.log(panel, markup=True, highlight=True, log_locals=False)
            log.warning(msg)
        case "ERROR" | 'error' | 'e':
            panel = Panel(
                Text(
                    msg,
                    style="bold bright_white"
                ),
                title=Text(
                    "ERROR",
                    style="error",
                ),
                title_align="left",
                border_style="error",
                padding=(1, 1),
                expand=False
            )
            console.log(panel, markup=True, highlight=True, log_locals=True)
            log.error(msg)
        case "CRITICAL" | 'critical' | 'c':
            panel = Panel(
                Text(
                    msg,
                    style="bold bright_white"
                ),
                title=Text(
                    "CRITICAL",
                    style="critical",
                ),
                title_align="left",
                border_style="critical",
                padding=(1, 1),
                expand=False
            )
            console.log(panel, markup=True, highlight=True, log_locals=True)
            log.critical(msg)
        case _:
            console.log(msg, markup=True, highlight=True, log_locals=False)
            log.info(msg)
