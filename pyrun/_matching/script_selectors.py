from __future__ import annotations


from typing import TYPE_CHECKING, Iterable, Callable, TypeAlias, Union


if TYPE_CHECKING:
    from pyrun._scripts.runnable import Runnable

    Selector: TypeAlias = Callable[[Runnable], bool]


def trivial_selector(yes_no: bool) -> Callable[[Runnable], bool]:

    def rule(script: Runnable):
        return yes_no

    return rule


def range_selector(start: int | None, end: int | None) -> Callable[[Runnable], bool]:

    def rule(script: Runnable):
        if script.pos is None:
            return False
        if start is not None and script.pos < start:
            return False
        if end is not None and script.pos > end:
            return False
        return True

    return rule


def pos_selector(pos: int) -> Callable[[Runnable], bool]:

    def rule(script: Runnable):
        return script.pos == pos

    return rule


def name_selector(name: str) -> Callable[[Runnable], bool]:

    def rule(script: Runnable):
        return script.name and script.name.lower() == name.lower() or False

    return rule


def any_selector(
    selectors: Iterable[Callable[[Runnable], bool]]
) -> Callable[[Runnable], bool]:

    def rule(script: Runnable):
        return bool([1 for rule in selectors if rule(script)])

    return rule


def parse_selector(selector: str) -> Callable[[Runnable], bool]:
    if selector == "%":
        return trivial_selector(True)
    elif "-" in selector:
        [before, after] = selector.split("-")
        # Either '-1' or '1-2':
        if not before or before.isdigit():
            return range_selector(
                int(before) if before else None, int(after) if after else None
            )
        else:
            # Must be a name with a '-' in it.
            return name_selector(selector)
    elif selector.isdigit():
        return pos_selector(int(selector))
    else:
        return name_selector(selector)


def parse_selector_list(union_selector_str: str) -> Callable[[Runnable], bool]:
    selector_list = union_selector_str.split(",")
    return any_selector([parse_selector(s) for s in selector_list])
