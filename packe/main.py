import importlib.metadata
import os
import sys
from pathlib import Path
from sys import platform

from termcolor import colored

from packe._cli import Cli
from packe._config_wrapper import ConfigFileWrapper
from packe._exec.bash_exec_prefix import BashPrefixExecutor
from packe._print import fatal_error


def start():
    if platform == "win32" or platform == "darwin":
        fatal_error("packe only supports Linux!", 3)

    cli = Cli()
    command = cli.parse()
    if command.command == "version":
        v = importlib.metadata.version("packe")
        print(colored(f"packe {v} / python {sys.version}", "green"))
        exit(0)
    cfg = ConfigFileWrapper(Path(command.config.strip()))
    if os.geteuid() != 0 and cfg.root_only:
        fatal_error("Config file requires running as root!", 4)

    pack = cfg.root_pack
    if len(pack) == 0:
        fatal_error("No scripts found in config", 1)

    matched = pack.find_all(command.selector)
    executor = BashPrefixExecutor(cfg.before)
    cmd = command.command
    if hasattr(command, "dry") and command.dry:
        cmd = "list"
    if not matched:
        splat = " ".join(command.selector)
        fatal_error(f"No scripts found for {splat}", 10)
    print(f"Matched {len(matched)} scripts")
    match cmd:
        case "run":
            matched.run(executor)
        case "list":
            print(f"{matched:summary}")
        case "print":
            print(f"{matched:full}")
        case _:
            fatal_error(f"Unknown command: {cmd}", 2)
    exit(0)
