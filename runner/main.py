from pathlib import Path

from termcolor import colored

from runner._cli import _Cli
from runner._from_config import pack_from_config


def start():
    cli = _Cli()

    command = cli.parse()

    pack = pack_from_config(Path(command.config))
    matched = list(pack.find_all(command.selector))
    cmd = command.command
    if hasattr(command, "dry") and command.dry:
        cmd = "list"
    if not matched:
        splat = " ".join(command.selector)
        print(f"No scripts found for {splat}")
        exit(1)
    match cmd:
        case "run":
            for script in matched:
                script.run()
            print(
                colored(
                    f"      ↑ DONE ↑      ", color="white", on_color="on_light_green"
                ),
                "\n",
            )
        case "list":
            for script in matched:
                print(f"{script:address}")
        case "print":
            for script in matched:
                print(f"{script:full}")
        case _:
            raise Exception(f"Unknown command {command.command}")
