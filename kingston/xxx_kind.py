import funcy as fy
import inspect
import types
import collections.abc
from typing import (TypeVar, Generic, Any, Iterable, Collection, List, Union,
                    Tuple, Callable, cast)

from kingston.decl import (PRIMTYPES, LISTLIKE, MUTABLE, Primitive, Listlike,
                           box, unbox, textual, numeric, isint, isdict, isgen)

Mutable = Union[list, set, dict]
Immutable = Union[tuple, str, bytes, list, int, bool, float]


class FrozenDict(collections.abc.Mapping):
    # Thank you Mike Graham! (https://stackoverflow.com/a/2704866/288672)
    "Tries to get as possible close to a true frozen dict type"

    def __init__(self, *args, **kwargs):
        "Create from dict and an 'update'"
        self._d = dict(*args, **kwargs)
        self._hash = None

    def __iter__(self):
        return iter(self._d)

    def __len__(self):
        return len(self._d)

    def __getitem__(self, key):
        return self._d[key]

    def __hash__(self):
        # It would have been simpler and maybe more obvious to
        # use hash(tuple(sorted(self._d.iteritems()))) from this discussion
        # so far, but this solution is O(n). I don't know what kind of
        # n we are going to run into, but sometimes it's hard to resist the
        # urge to optimize when it will gain improved algorithmic performance.
        if self._hash is None:
            hash_ = 0
            for pair in self.items():
                hash_ ^= hash(pair)
            self._hash = hash_
        return self._hash


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


def xrtype(arg: Any) -> Union[type, Tuple[type]]:
    """
    Recursive type descriptions with extra smarts.
    >>> xrtype(1)
    int
    >>> xrtype('x')
    str
    >>> xrtype(())
    tuple
    >>> xrtype((1,2))
    (int, int)
    """
    name = arg.__name__ if hasattr(arg, '__name__') else None
    type_ = name if name else type(arg)
    arity = len(arg) if type_ in LISTLIKE else 0

    if arity == 0:
        return type_
    elif arity > 1:
        return cast(Union[type, Tuple[type]], tuple(xrtype(el) for el in arg))
    else:
        raise TypeError(f"kingston.kind.xrtype: doesn't understand {arg!r}")


def uniform(template: Collection, sibling: Collection) -> Collection:
    if sibling is None:
        raise TypeError(f"kingston.kind.uniform(): None can not be uniformed")
    elif template is None:
        raise TypeError(f"kingston.kind.uniform(): Can not uniform to None")
    elif isinstance(sibling, type(template)):
        return sibling
    elif fy.is_seqcoll(sibling):
        coerced = fy.select(fy.identity, sibling)  # e.g. call funcy._factory()
        return cast(Collection, coerced)
    raise TypeError(
        f"kingston.kind.uniform(): ran out of options for {sibling!r}")


def describe(obj):
    """
    >>> describe(1)
    (int,)
    >>> describe((1, 'x'))
    (int,str)
    >>> describe((1, 'x', ('y', 'z'))
    (int, str, (str, str))
    >>> class Cls(object):
    ...    def __init__(self, *args):
    ...        self.args = args
    >>> ob = Cls()
    >>> describe((1, 2, (ob, 'x')))
    (int, int, ('Cls', str))
    """

    return fy.walk(xrtype, box(obj))


def cast_to_hashable(obj):
    try:
        hash(obj)
        return obj
    except TypeError:
        return tuple(x for x in obj)


def forcehash(x: Any) -> int:
    T = type(x)
    if T in MUTABLE:
        return hash(tuple(x))
    if T is dict:
        return hash(repr(x))

    raise TypeError(f"kingston.kind.forcehash(): can't handle {x!r}")


def anyhash(x: Any) -> int:
    try:
        return hash(x)
    except TypeError:
        return forcehash(x)


# from kingston.decl import Immutable  # XXX ??? borde redan vara importerad?


def mute(mut: Mutable) -> Immutable:
    if isdict(mut):
        return cast(Callable, cast(FrozenDict, mut))(mut)
    if fy.is_seqcoll(mut):
        mut = cast(Mutable, mut)
        return tuple(el for el in mut)
    raise NotImplementedError(
        f"kingston.kind.mute(): don't know how to handle {mut!r}")
