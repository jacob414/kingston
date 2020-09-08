# yapf

from dataclasses import dataclass
from typing import TypeVar, Generic

# See https://github.com/python/mypy/issues/5485

T = TypeVar("T")


@dataclass
class Box(Generic[T]):
    """
    Ugh, wierd import issue https://stackoverflow.com/q/61855034/288672
    unsolved as of 2020-05-27...

    You can run this file, but not import it
    """
    inner: T

    @property
    def unboxed(self) -> T:
        return self.inner


from .xxx_kind import *  # NOQA
