import collections.abc
from typing import Any, Collection, Iterable, List, Tuple, Union

Mutable = Union[list, set, dict]
Immutable = Union[tuple, str, bytes, list, int, bool, float]

class FrozenDict(collections.abc.Mapping):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def __iter__(self) -> Any: ...
    def __len__(self) -> None: ...
    def __getitem__(self, key: Any) -> Any: ...
    def __hash__(self) -> Any: ...

def fromiter(objs: Iterable[Any]) -> List[type]: ...
def nick(x: Any) -> str: ...
def xrtype(arg: Any) -> Union[type, Tuple[type]]: ...
def uniform(template: Collection, sibling: Collection) -> Collection: ...
def describe(obj: Any) -> Any: ...
def cast_to_hashable(obj: Any) -> Any: ...
def forcehash(x: Any) -> int: ...
def anyhash(x: Any) -> int: ...
def mute(mut: Mutable) -> Immutable: ...
