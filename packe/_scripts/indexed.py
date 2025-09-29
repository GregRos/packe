from pathlib import Path
import re


def try_parse_indexed(stem: str):
    # split on first dot or hyphen, so "01.name" and "01-name" both work
    parts = re.split(r"[.-]", stem, maxsplit=1)
    match parts:
        case [name]:
            return None
        case ["", name]:
            return None
        case ["_", name]:
            return (None, name)
        case [pos, name] if pos.isdigit():
            return (int(pos), name)
        case _:
            return None


def is_valid_script(path: Path):
    return path.suffix == ".sh" or path.suffix == ".bash"


def must_parse_indexed(stem: str):
    r = try_parse_indexed(stem)
    if r is None:
        raise Exception(f"Invalid indexed name: {stem}")
    return r
