from os import path
from pathlib import Path
from yaml import safe_load

from runner._scripts import Pack


def pack_from_config(config_path: Path):
    with open(config_path, "r") as f:
        config = safe_load(f)
    root = Pack.root()
    for name, obj in config.items():
        path = Path(obj["path"])
        root.add(Pack.from_indexed_dir(root, path, name))
    return root
