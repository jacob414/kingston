import inspect
from inspect import Parameter

from typing import Any, Collection, Union, Tuple, Callable, Mapping, Type

from kingston.decl import params  # type: ignore  ## XXX but why ???
from kingston.decl import LISTLIKE, box, unbox, Singular

# XXX sigh, I just can't get this to work. Yes, I have generated
# stubs and tried what I can find in the mypy docs.
import funcy as fy  # type: ignore

from operator import attrgetter

Mutable = Union[list, set, dict]
Immutable = Union[tuple, str, bytes, list, int, bool, float]

POSITIONAL = (Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD)
KEYWORD = (Parameter.KEYWORD_ONLY, )


def uniform(template: Collection, sibling: Collection) -> Collection:
    try:
        return type(sibling)(template)  # type: ignore  ## ugh..
    except ValueError:
        raise TypeError(
            f"kingston.kind.uniform(): ran out of options for {sibling!r}")


def safetype(x: Any) -> Type:
    """Safer than `type(x)` due to a special rule: instances of `x` that
    are taken from the `typing` module is returned as-is.

    """
    return x if str(x).startswith('typing.') else type(x)  # XXX ugly check


def xrtype(x: Any) -> Union[type, Collection[type]]:
    """
    Non-recursive type descriptions with extra smarts.
    >>> xrtype(1)
    <class 'int'>
    >>> xrtype('x')
    <class 'str'>
    >>> xrtype(())
    <class 'tuple'>
    >>> xrtype((1,2))
    (<class 'int'>, <class 'int'>)
    >>> xrtype([1,2,3])
    [<class 'int'>, <class 'int'>, <class 'int'>]
    >>> xrtype(Mapping)
    typing.Mapping
    """
    name = x.__name__ if hasattr(x, '__name__') else None
    type_ = name if name else safetype(x)
    arity = len(x) if type_ in LISTLIKE else 0

    if arity == 0:
        return type_
    else:
        return safetype(x)(xrtype(el) for el in x)


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
    T = xrtype(x)
    return 'None' if x is None else getattr(T, '__name__', type(x).__name__)


def ispos(p):
    return p if p.kind in POSITIONAL else False


def iskw(p):
    return p if p.kind in KEYWORD else False


def primparams(fn: Callable) -> Union[Singular, Tuple[Any]]:
    "Aproximate type signature of function `fn´ in Python primitive types"
    fullparams = params(fn)  # type: ignore

    def getparams():
        return filter(lambda p: p.default is inspect.Signature.empty,
                      fullparams.values())

    positional = map(attrgetter('annotation'), filter(ispos, getparams()))
    keyword = map(attrgetter('annotation'), filter(iskw, getparams()))

    kind = attrgetter('kind')

    variadic = tuple(... for x in fullparams.values()
                     if kind(x) == Parameter.VAR_POSITIONAL) + tuple(
                         Mapping for x in fullparams.values()
                         if kind(x) == Parameter.VAR_KEYWORD)

    return unbox(tuple(fy.chain(positional, keyword, variadic)))


def deepxrtype(obj):
    """
    Recursive variant of `xrtype()`.

    >>> deepxrtype(1)
    (<class 'int'>,)
    >>> deepxrtype('x')
    (<class 'str'>,)
    >>> deepxrtype((1, 'x'))
    (<class 'int'>, <class 'str'>)
    >>> deepxrtype((1, 'x', ('y', 'z')))
    (<class 'int'>, <class 'str'>, (<class 'str'>, <class 'str'>))
    """

    return fy.walk(xrtype, box(obj))


def cast_to_hashable(obj):
    try:
        hash(obj)
        return obj
    except TypeError:
        return tuple(x for x in obj)


def anyhash(x: Any) -> int:
    try:
        return hash(x)
    except TypeError:
        return hash(tuple(x))
