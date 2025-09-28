from typing import Iterable

from termcolor import colored
from spack._scripts.runnable import Runnable
from pygments import highlight
from pygments.formatters.terminal import TerminalFormatter
from pygments.lexers.shell import BashLexer

term = TerminalFormatter()
lexer = BashLexer()


def pretty_print_lines(title: str, contents: str):
    # NNN | Line
    title = colored(title, attrs=["underline"])
    contents = contents.strip()
    contents = highlight(contents, lexer, term)
    lines = contents.split("\n")
    lines = [f"{(i + 1):>3} | {line}" for i, line in enumerate(lines)]
    return "\n".join([title, *lines])


def pretty_print_kids(title: str, kids: Iterable["Runnable"]):
    results = [f"∙ {x.name}" for x in kids]
    title = colored(title, attrs=["underline"])
    return "\n".join([title, *results])
