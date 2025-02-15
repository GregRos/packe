from typing import Protocol


class Command(Protocol):
    config: str
    command: str
    selector: list[str]
    dry: bool
