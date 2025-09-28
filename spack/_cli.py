import argparse
from logging import fatal
from os import environ
from sys import stderr
from typing import Iterable, Sequence, Union
from ._print import fatal_error

from spack._command import Command
from spack._matching.script_selectors import parse_selector_list


def _add_selector(p: argparse.ArgumentParser):
    p.add_argument(
        "selector",
        nargs="+",
        help="a multipart selector for the installation scripts to run.",
    )


class _Cli:
    def __init__(self):
        root_parser = argparse.ArgumentParser(description="Perdido setup script runner")

        root_parser.add_argument(
            "-C", "--config", help="path to a config file", required=False, type=str
        )
        subparsers = root_parser.add_subparsers(
            title="command", required=True, dest="command"
        )

        version = subparsers.add_parser("version", help="print the version and exit")

        run = subparsers.add_parser(
            "run",
            help="run one or more installation scripts",
        )

        run.add_argument(
            "-D",
            "--dry",
            dest="dry",
            action="store_true",
            help="don't actually run the scripts",
            required=False,
        )
        _add_selector(run)
        list = subparsers.add_parser("list", help="list installation scripts")
        _add_selector(list)
        printing = subparsers.add_parser("print", help="print installation scripts")
        _add_selector(printing)

        self._parser = root_parser

    def parse(self, args: Union[Sequence[str], None] = None) -> Command:
        args_result = self._parser.parse_args(args)
        if args_result.command == "version":
            return args_result  # type: ignore
        if hasattr(args_result, "rule"):
            args_result.rule = parse_selector_list(args_result.rule)
        if not hasattr(args_result, "config"):
            args_result.config = environ.get("PYRUN_CONFIG", None)
            if not args_result.config:
                fatal_error("No config file specified and PYRUN_CONFIG not set", 2)

        return args_result  # type: ignore
