from os import environ
from pathlib import Path

import ujson as json
from mongoengine import ValidationError


import src.myaml as yaml
from atlas import sg

from log import BASE, console, log
from rich import inspect as rinspect
from inspect import stack



