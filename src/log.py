# src/log.py

from platform import platform
from os import environ
from time import perf_counter

from loguru import logger as log
from rich import print, inspect
from rich.pretty import pprint
from rich.highlighter import ReprHighlighter
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.style import Style
from functools import wraps
from ujson import load, loads, dump, dumps

console = Console(width=110)

# > BASE
def generate_base():
    """Generate base directory for the project."""
    if platform() == "Linux":
        ROOT = "home"
    else:
        ROOT = "Users"  # < Mac
    BASE = f"/{ROOT}/maxludden/dev/py/supergene"
    return BASE


BASE = generate_base()

# > Current Run
def get_last_run() -> int:
    """
    Get the last run of the script.
    """
    with open(f"{BASE}/run.txt", "r") as infile:
        last_run = int(infile.read())
    return last_run


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
    with open(f"{BASE}/run.txt", "w") as outfile:
        outfile.write(str(run))


def new_run() -> int:
    """
    Create a new run of the script.
    """
    last_run = get_last_run()
    run = increment_run(last_run)
    record_run(run)
    console.clear()
    console.rule(title=f"\n\n\nRun {run}\n\n\n")
    return run


current_run = new_run()
# End of run

# > Handlers
sinks = log.configure(
    handlers=[
        dict(
            sink=f"{BASE}/logs/debug.log",
            level="DEBUG",
            format="Run {extra[run]} | {time:hh:mm:ss:SSS A} | {file.name: ^13} |  Line {line: ^5} | {level: <8}ﰲ  {message}",
            rotation="10 MB",
        ),
        dict(
            sink=f"{BASE}/logs/info.log",
            level="INFO",
            format="Run {extra[run]} | {time:hh:mm:ss:SSS A} | {file.name: ^13} |  Line {line: ^5} | {level: <8}ﰲ  {message}",
            rotation="10 MB",
        ),
        dict(
            sink=(
                lambda msg: console.log(
                    msg, markup=True, highlight=True, log_locals=True
                )
            ),
            level="INFO",
            format="Run {extra[run]} | {time:hh:mm:ss:SSS A} | {file.name: ^13} |  Line {line: ^5} | {level: ^8} ﰲ  {message}",
        ),
        dict(
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
    extra={"run": current_run},
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

'''
def inspect_func(*, level="DEBUG", entry: bool=True, exit: bool=True):
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
        function_dict = {
            "name": name,
        }

        @wraps(func)
        def wrapped(*args, **kwargs):
            inspect_log = log.opt(depth=1)
            if entry:
                function_dict["args"] = args
                function_dict["kwargs"] = kwargs
                inspect_log.log(
                    level,
                    f"Entering '{name}'\n<code>\nargs:\n{args}'\nkwargs={kwargs}</code>",
                )
            result = func(*args, **kwargs)
            if exit:
                inspect_log.log(
                    level, f"Exiting '{name}'<code>\nresult:\n<{result}</code>"
                )
                function_dict["result"] = str(result)

            panel_title_str = f"Called {name}(args, kwargs)"
            panel_title = Text(
                panel_title_str,
                justify="center",
                style = Style(
                    color = "purple",
                    bgcolor = "white",
                    bold = True,
                )
            )
            result_str = f"Result: {result}"
            result = Text(
                result_str,
                justify="left"
                style=Style(
                    color="purple",
                    bgcolor="white",
                )
            )

                ))
            inspect_panel = Panel(
                Text(f" Called {function_dict["result"]}",
                    style=Style(
                        color="white",
                        bgcolor="purple"
                        bold = True
                    ),
                    title
                    )),
            return result
            )
            return wrapped

    return wrapper
    '''