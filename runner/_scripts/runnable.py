from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from runner._scripts.types import RunnableFormat


@dataclass
class Runnable(ABC):
    pos: int | None
    name: str
    parent: "Runnable | None"

    @property
    def address(self):
        all: list[Runnable] = [*self.parents, self]
        prefix = "/".join([x.caption for x in all])
        return prefix

    @property
    def parents(self):
        all_parents: list[Runnable] = []
        last = self
        while last.parent:
            last = last.parent
            all_parents.append(last)
        all_parents.reverse()
        return all_parents

    @property
    def caption(self):
        parts = []
        if self.pos:
            parts.append(str(self.pos).zfill(2))
        parts.append(self.name)
        return ":".join(parts)

    @abstractmethod
    def run(self): ...

    @abstractmethod
    def __format__(self, format_spec: RunnableFormat) -> str: ...
    @abstractmethod
    def __repr__(self) -> str: ...

    @abstractmethod
    def __str__(self) -> str: ...
