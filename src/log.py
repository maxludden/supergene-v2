# src/log.py

from functools import wraps
from os import environ
from pathlib import Path
from time import perf_counter
from typing import Tuple

from dotenv import load_dotenv
from loguru import logger as log
from rich.panel import Panel
from rich.table import Column
from rich.text import Text
from rich.prompt import Prompt, Confirm
from ujson import dump, load
from src.color import console, progress, rainbow, gradient, gradient_panel

load_dotenv()


BASE = Path.cwd()
JSON_DIR = BASE / "json"
LOGS_DIR = BASE / "logs"
RUN_DICT = JSON_DIR / "run.json"


def validate_paths() -> None:
    """
    Validate that the necessary directories exist.
    """

    class DirectoryNotFound(Exception):
        pass

    class FileNotFound(Exception):
        pass

    if not JSON_DIR.exists():
        raise DirectoryNotFound(f"JSON Directory: {JSON_DIR} - does not exist.")
    if not LOGS_DIR.exists():
        raise DirectoryNotFound(f"LOG Directory: {LOGS_DIR} - does not exist.")
    if not RUN_DICT.exists():
        raise FileNotFound(f"Run Dictionary: {RUN_DICT} - does not exist.")


# > Current Run
def get_last_run() -> int:
    """
    Get the last run of the script.
    """
    with open(RUN_DICT, "r") as infile:
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
    with open(RUN_DICT, "w") as outfile:
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
    console.clear()
    RUN = rainbow(f"Run {run}", 3)
    console.rule(title=RUN, style="bold bright_white")
    return run


current_run = new_run()

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
            diagnose=True,
            catch=True,
            backtrace=True,
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
