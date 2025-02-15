from pathlib import Path

from termcolor import colored

from runner._cli import _Cli
from runner._config_file import ConfigFile


def start():
    cli = _Cli()

    command = cli.parse()
    config_file = ConfigFile(Path(command.config))
    pack = config_file.to_root_pack()
    matched = pack.find_all(command.selector)
    cmd = command.command
    if hasattr(command, "dry") and command.dry:
        cmd = "list"
    if not matched:
        splat = " ".join(command.selector)
        print(f"No scripts found for {splat}")
        exit(1)

    match cmd:
        case "run":
            matched.run()
        case "list":
            print(f"{matched:summary}")
        case "print":
            print(f"{matched:full}")
        case _:
            raise Exception(f"Unknown command {command.command}")
