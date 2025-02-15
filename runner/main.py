from pathlib import Path

from termcolor import colored

from runner.cli import Cli
from runner.all_scripts import root


def start():
    cli = Cli()

    command = cli.parse()

    matched = list(root.find_all(command.selector))
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
