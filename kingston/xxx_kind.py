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


def fromiter(objs: Iterable[Any]) -> List[type]:
    return [type(ob) for ob in objs]


def nick(x: Any) -> str:
    """Safely get a short 'nickname' from parameter `x`. If `x == None` returns
    `'None'`

    >>> nick(1)
    'int'
    >>> nick([1,2])
    'list'
    >>> nick(None)
    'None'
    """
    kind = getattr(x, '__name__', getattr(type(x), '__name__', '?'))
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
    elif fy.is_seqcoll(arg):
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
