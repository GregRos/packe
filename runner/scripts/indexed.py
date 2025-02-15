from pathlib import Path


def try_parse_indexed(stem: str):
    all = stem.split(".", maxsplit=1)
    match all:
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
