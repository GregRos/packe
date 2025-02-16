import sys
from typing import NoReturn

from termcolor import colored


def echo_warn(message: str):
    message = colored(f"⚠️ {message}", "yellow")
    print(message, file=sys.stdout)


def fatal_error(message: str, code: int = 1) -> NoReturn:
    message = colored(f"💀 {message}", "black", "on_red")
    print(message, file=sys.stderr)
    exit(code)
