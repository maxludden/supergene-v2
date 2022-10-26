# superforge/core/max_yaml.py

from pathlib import Path
import yaml
from typing import Any
from pathlib import Path
from rich import print, inspect


BASE = Path.cwd()


# Import UnsafeLoader
try:
    from yaml import CUnsafeLoader as Loader
except ImportError:
    from yaml import UnsafeLoader as Loader


# Import SafeLoader
try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader


# Import Dumper
try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper

# Import SafeDumper
try:
    from yaml import CSafeDumper as SafeDumper
except ImportError:
    from yaml import SafeDumper



def load(filepath: str | Path) -> Any:
    """
    Load a yaml file.

    Args:
        filepath (str | Path): The path to the yaml file.

    Returns:
        Any: The loaded yaml file.
    """

    with open(filepath, "r") as infile:
        result = yaml.load(infile, Loader=Loader)
    return result


def loads(data: str) -> Any:
    """
    Load a yaml file.

    Args:
        data (str): The yaml data to load.

    Returns:
        Any: The loaded yaml file.
    """
    result = yaml.load(data, Loader=Loader)
    return result


def _safe_load(yaml_to_load: str, filepath: str | Path) -> None:
    with open(filepath, "r") as infile:
        result = yaml.safe_load(infile)
    result = yaml.load(yaml_to_load, Loader=SafeLoader)
    return result


def _unsafe_load(yaml_to_load: str):
    result = yaml.load(yaml_to_load, Loader=yaml.UnsafeLoader)
    return result


def _safe_dump(data: str, filepath: str | Path):
    with open(filepath, "w") as outfile:
        yaml.dump(
            data,
            stream=outfile,
            Dumper=SafeDumper,
            mode="wt",
            encoding="utf-8",
            indent=2,
        )  # type: ignore


def dump(data: Any, filepath: str | Path) -> None:
    """
    Serialize a yaml file using the normal pyaml library.

    Args:
        data (Any): The data to serialize.
        filepath (str | Path): The path to the yaml file.
    """
    data = yaml.dump(
        data, Dumper=Dumper, mode="wt", encoding="utf-8", indent=2
    )  # type: ignore
    inspect(data)
    with open(filepath, "w") as outfile:
        outfile.write(data)


def dumps(data: Any) -> str:
    """
    Serialize a yaml string form a python object.add()

    Args:
        data (Any): The data to serialize.

    Returns:
        str: The serialized yaml string.
    """
    data = yaml.dump(
        data, Dumper=Dumper, mode="wt", encoding="utf-8", indent=2
    )  # type: ignore
    inspect(data)
    return data
