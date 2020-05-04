# yapf

from dataclasses import dataclass
from typing import TypeVar, Generic, Any, Iterable, List

T = TypeVar("T")

# See https://github.com/python/mypy/issues/5485


@dataclass
class Box(Generic[T]):
    inner: T

    @property
    def unboxed(self) -> T:
        return self.inner


def fromiter(objs: Iterable[Any]) -> List[type]:
    return [type(ob) for ob in objs]


def nick(x: Any) -> str:
    """Safely get a short 'nickname' from parameter `x`. If `x == None` returns
    `'None'`

    >>> nick(1)
    int
    >>> nick([1,2])
    list
    >>> nick(None)
    None
    """
    kind = type(x).__name__
    return x is None and 'None' or kind
