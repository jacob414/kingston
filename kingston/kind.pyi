from typing import TypeVar, Generic, Any, Iterable, List

T = TypeVar("T")

from dataclasses import dataclass

@dataclass
class Box(Generic[T]):
    inner: T

    @property
    def unboxed(self) -> T: ...

def fromiter(objs: Iterable[Any]) -> List[type]: ...

def nick(x: Any) -> str: ...
