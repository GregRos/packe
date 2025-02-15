from dataclasses import field, dataclass
from os import name
from pathlib import Path
from typing import Callable, Iterable
from runner._matching.script_selectors import parse_selector_list
from runner._scripts.pretty_print import pretty_print_kids
from runner._scripts.script import Script
from runner._scripts.indexed import must_parse_indexed, try_parse_indexed
from runner._scripts.runnable import Runnable
from runner._scripts.types import RunnableFormat


@dataclass
class Pack(Runnable):
    _kids: list[Runnable] = field(init=False, default_factory=list)

    @property
    def kids(self):
        return [x for x in sorted(self._kids, key=lambda x: x.pos or 0)]

    @classmethod
    def is_valid_indexed(cls, path: Path):
        return path.is_dir() and try_parse_indexed(path.name) is not None

    @classmethod
    def root(cls):
        pk = Pack(None, "@", None)
        return pk

    def add(self, *kids: Runnable):
        self._kids = [*self._kids, *kids]
        return self

    @classmethod
    def from_indexed_dir(
        cls, parent: Runnable | None, index_root: Path, name: str | None = None
    ):
        if not index_root.is_dir():
            raise Exception(
                f"Expected a directory, got {index_root}, ${index_root.stat()}"
            )
        if name is not None:
            pos = None
        elif cls.is_valid_indexed(index_root):
            pos, name = must_parse_indexed(index_root.name)
        else:
            name = index_root.name
            pos = None
        p = Pack(pos, name, parent)

        def make_kid(path: Path):
            if path.is_dir():
                return Pack.from_indexed_dir(p, path)
            assert parent is not None
            return Script.from_indexed_path(p, path)

        indexed_kids = [
            make_kid(x)
            for x in index_root.glob("*")
            if try_parse_indexed(x.name) is not None
        ]
        p.add(*indexed_kids)
        return p

    def find_all(self, multipart_selectors: list[str]):
        all_results = []
        for multipart_selector in multipart_selectors:
            selector_list = [
                parse_selector_list(s) for s in multipart_selector.split("/")
            ]

            results = [self]
            for selector in selector_list:
                next_results = []
                for x in results:
                    assert isinstance(
                        x, Pack
                    ), f"Selector tried to look inside script {x}"
                    for kid in x.kids:
                        if selector(kid):
                            next_results.append(kid)
                results = next_results
            all_results.extend(results)

    def __len__(self):
        return len(self.kids)

    @property
    def caption(self):
        return f"{super().caption}"

    def __format__(self, format_spec: RunnableFormat) -> str:

        match format_spec:
            case "full":
                return pretty_print_kids(self.address, self.kids)
            case "line":
                return ": ".join(
                    [self.name, ", ".join(f"{x:child}" for x in self.kids)]
                )
            case "child":
                return f"{self.name}[{len(self)}]/"
            case "address":
                return f"{self.address}/"
            case "short":
                return self.caption + "/"
            case _:
                raise ValueError(f"Unknown format spec: {format_spec}")

    def __repr__(self) -> str:
        return self.__format__("line")

    def __str__(self) -> str:
        return self.__format__("short")

    def run(self):
        for x in self.kids:
            x.run()
