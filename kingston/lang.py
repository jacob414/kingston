# yapf

from funcy import flow  # type: ignore
import funcy as fy  # type: ignore

import types
import numbers
import copy
from functools import singledispatch
from typing import (Any, Mapping, List, Tuple, Iterable, Sequence, Generator,
                    Callable, Union, TYPE_CHECKING)

from . import decl

import itertools

from functools import wraps, update_wrapper

import operator as ops

from .decl import (PRIMTYPES, textual, numeric, isdict, isgen)


class Undefined:
    "Marker class for undefined values."


def itempadded(index: int, pad:Any) -> Any:
    """Sets up a function that will index a sequence but return a marker
    object if the index is out of bounds.

    """
    def element_or_default(seq: Sequence) -> Any:
        try:
            return seq[index]
        except IndexError:
            return pad

    return element_or_default


def unfold_gen(x: Generator[Any, None, None],
               cast: type = tuple) -> Iterable[Any]:
    """Quick recursive unroll of possibly nested (uses funcy library under
    the hood)

    """
    res = tuple(fy.flatten(x, isgen))
    if TYPE_CHECKING:
        res = cast(Iterable, res)  # pragma: nocov
    return res


def typename(x: Any) -> str:
    """Safely get a type name from parameter `x`. If `x == None` returns
    `'None'`

    """
    return x is None and 'None' or x.__class__.__name__


def pubvars(obj: Any) -> Iterable:
    "Returns all public variables except methods"
    if isdict(obj):
        return tuple(obj)
    if fy.is_seqcoll(obj) or isinstance(obj, set):
        return copy.copy(obj)
    else:
        return [
            attr for attr in dir(obj)
            if not attr.startswith('__') and not callable(getattr(obj, attr))
        ]


def isprimitive(obj):
    "Determines if a value belongs to a primitive type (= {numbers, strings})"

    if numeric(obj):
        return True
    elif textual(obj):
        return True

    return False


def isprim_type(type_):
    "Does primtype"
    return True if type_ in PRIMTYPES else False


def num_or_else(cand: Any) -> numbers.Number:
    asint = flow.silent(int)(cand)
    if decl.numeric(asint):
        return asint
    asfloat = flow.silent(float)(cand)
    if decl.numeric(asfloat):
        return asfloat
    return cand


def replace(reps: dict, seq: Sequence) -> Sequence:
    """Simple replacement of values in a sequence. Returns a copy of
    ``seq`` where all values in ``seq`` that are equal to keys in
    ``reps`` are replaced by the values in ``reps`` corresponding to
    that same key.

    >>> replace({1:10, 3:30}, (1, 2, 3, 4, 5))
    (10, 2, 30, 4, 5)

    The return type is the same as of the parameter ``seq``::

    >>> replace({1:10, 5:50}, [1, 2, 3, 4, 5])
    [10, 2, 3, 4, 50]
    """
    return fy.empty(seq).__class__(
        map(lambda x: x in reps and reps[x] or x, seq))


def detect_numbers(seq: Iterable) -> Iterable:
    return [num_or_else(el) for el in seq]


def methdispatch(func):
    """Thanks Zero Piraeus!

    https://stackoverflow.com/a/24602374/288672
    """
    dispatcher = singledispatch(func)

    def wrapper(*args, **kw):
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)

    wrapper.register = dispatcher.register
    update_wrapper(wrapper, func)
    return wrapper


def primbases(cls):
    "Does primbase"
    return [T for T in cls.__bases__ if isprim_type(T)]


def bind_methods(Base, instance):
    "Does bind_methods"
    for name, fn in instance.__bind__:
        setattr(Base, name, types.MethodType(fn, instance))
    return instance


class Base(object):
    __bind__: List[Tuple[Callable, Any]] = []

    def __init__(self, *params, **opts):
        bind_methods(self.__class__, self)

        def bind_method_on_self(self: Any, fn: Callable):
            "Does bound_on_instance"

            name = fn.__name__

            @wraps(fn)
            def callit(*params: Any, **opts: Any) -> None:
                "Does callit"
                return fn(self, *params, **opts)

            setattr(self, name, callit)
            return callit

        self.method = types.MethodType(bind_method_on_self, self)

    @staticmethod
    def __wrapper(fn: Callable, Cls: Any = None, name: str = None):
        "Does __wrapper"
        if name is None:
            name = fn.__name__

        @wraps(fn)
        def do_call(*params, **opts):
            if Cls is None:
                return fn(*params, **opts)
            else:
                return fn(*((Cls, ) + params), **opts)

        if Cls is None:
            setattr(Base, name, do_call)
        else:
            setattr(Cls, name, do_call)

        return do_call

    __classmethod__ = classmethod

    @classmethod
    def classmethod(cls, fn):
        return Base.__wrapper(fn, Cls=cls)

    @staticmethod
    def staticmethod(fn: Callable) -> Callable:
        return Base.__wrapper(fn)

    @__classmethod__
    def method(Subclass: Any, fn: Callable) -> Callable:
        "Creates a method from the decorated function `fn`"
        setattr(Subclass, fn.__name__, types.MethodType(fn, Subclass))
        return fn


def mkclass(name: str, bases: Tuple = (), **clsattrs: Any) -> Any:
    "Does mkclass"

    Gen = type(name, (Base, ) + bases, clsattrs)
    return Gen


def arity(fn: Callable) -> int:
    "Returns the number of arguments required by `fn`."
    return len(decl.params(fn))


def callinfo(fn: Callable, env: Mapping[str, Any]) -> dict:
    return {
        'args': [env[name] for name in decl.params(fn)],
    }
