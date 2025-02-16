import sys
from typing import NoReturn

from termcolor import colored


def echo_warn(message: str):
    message = colored(message, "yellow")
    print(f"⚠️ {message}", file=sys.stdout)


def fatal_error(message: str, code: int = 1) -> NoReturn:
    message = colored(message, "black", "on_red")
    print(f"💀 {message}", file=sys.stderr)
    exit(code)
