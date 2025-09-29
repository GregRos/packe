from typing import NotRequired, TypedDict


class ConfigEntry(TypedDict):
    path: str


class ConfigFile(TypedDict):
    root_only: NotRequired[bool]
    entrypoints: dict[str, ConfigEntry]
    prerun: NotRequired[str]
