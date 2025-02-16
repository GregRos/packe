from typing import NotRequired, TypedDict


class ConfigEntry(TypedDict):
    path: str


class ConfigFile(TypedDict):
    entrypoints: dict[str, ConfigEntry]
    prerun: NotRequired[str]
