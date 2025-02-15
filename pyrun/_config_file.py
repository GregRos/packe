from pathlib import Path
from typing import TypedDict
from yaml import safe_load


class ConfigEntry(TypedDict):
    path: str


class ConfigFile:
    data: dict[str, ConfigEntry]

    def __init__(self, path: Path):
        self.path = path
        self.data = safe_load(path.read_text())

    def to_root_pack(self):
        from pyrun._scripts import Pack

        root = Pack.root()
        for name, obj in self.data.items():
            path = Path(obj["path"])
            root.add(Pack.from_indexed_dir(root, path, name))
        return root
