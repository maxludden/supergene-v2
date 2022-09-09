# superforge/core/max_yaml.py

from pathlib import Path
import yaml
from typing import Any, Union
from pathlib import Path


from rich import print, inspect


# BASE = Path(__file__).parent.parent
BASE = Path.cwd()
print(BASE)
#. >> /Users/maxludden/dev/py/supergene


# > Import UnsafeLoader
try:
    from yaml import CUnsafeLoader as Loader
except ImportError:
    from yaml import UnsafeLoader as Loader
    yaml_classes = False

# > Import SafeLoader
try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader


# > Import Dumper
try:
    from yaml import CDumper as Dumper\
except ImportError:
    from yaml import Dumper

# > Import SafeDumper
try:
    from yaml import CSafeDumper as SafeDumper
except ImportError:
    from yaml import SafeDumper


#.End of Imports ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯ Custom Functions:

def load(filepath: str | Path) -> Any:
    with open(filepath, "r") as infile:
        result = yaml.safe_load(infile)
    return result


color_themes = load("json/color_themes.json")
inspect(color_themes)


def safe_load(yaml_to_load: str, filepath: str | Path) -> None:
    with open(filepath, "r") as infile:
        result = yaml.safe_load(infile)
    result = yaml.load(yaml_to_load, Loader=SafeLoader)
    return result


def unsafe_load(yaml_to_load: str):
    result = yaml.load(yaml_to_load, Loader=yaml.UnsafeLoader)
    return result


@log.catch
def safe_dump(data: str, filepath: str | Path):
    with open(filepath, "w") as outfile:
        yaml.dump(
            data,
            stream=outfile,
            Dumper=SafeDumper,
            mode="wt",
            encoding="utf-8",
            indent=2,
        )  # type: ignore


@log.catch
def dump(data: str, filepath: str | Path):
    with open(filepath, "w") as outfile:
        yaml.dump(
            data, stream=outfile, Dumper=Dumper, mode="wt", encoding="utf-8", indent=2
        )  # type: ignore
