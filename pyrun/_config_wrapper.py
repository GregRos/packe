import functools
import os
from pathlib import Path
from typing import NotRequired, TypedDict
from yaml import safe_load

from pyrun._config import ConfigFile


class ConfigFileWrapper:
    _data: ConfigFile

    def __init__(self, path: Path):
        self.path = path
        self._data = safe_load(path.read_text())
        before_str = self._data.get("before", None)
        self.before = path.absolute().parent / Path(before_str) if before_str else None

    @functools.cached_property
    def root_pack(self):
        from pyrun._scripts import Pack

        root = Pack.root()
        for name, obj in self._data["entrypoints"].items():
            path = self.path.absolute().parent / obj["path"]
            expanded = os.path.expandvars(path)
            root.add(Pack.from_indexed_dir(root, Path(expanded), name))
        return root
