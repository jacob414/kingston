# yapf
# strict types

from typing import (Any, Mapping, List, Tuple, Iterable, Generator, Callable,
                    Union, Set, cast)
import numbers
import collections
import funcy as fy
import types

from functools import wraps

PRIMTYPES = {int, bool, float, str, set, list, tuple, dict, bytes}
LISTLIKE = {set, list, tuple}
TEXTLIKE = {str, bytes}
MUTABLE = {list, set, dict}

Primitive = Union[int, bool, float, str, set, list, tuple, dict, bytes]
Listlike = Union[set, list, tuple]
Singular = Union[Primitive, Callable]

textual = fy.isa(*TEXTLIKE)
numeric = fy.isa(numbers.Number)
isint = fy.isa(int)
isdict = fy.isa(dict)
isgen = fy.isa(types.GeneratorType)


def unbox(x: Any) -> Singular:
    """
    >>> unbox(1)
    1
    >>> unbox((1,))
    1
    >>> unbox((1,2))
    (1, 2)
    >>> unbox((1,2,(3,4)))
    (1, 2, (3, 4))
    """
    do: Callable[[Any], Any] = lambda x: x[0] if fy.is_seqcoll(x) and len(
        x) == 1 else x

    if callable(x):

        @wraps(x)
        def decorate(*params: Any, **opts: Any) -> Any:
            return do(x(*params, **opts))

        return decorate
    return do(x)


def box(x: Any) -> Any:
    return x if type(x) in LISTLIKE else (x, )

def setof(x:Any) -> Set:
    return cast(Set, set(x) if type(x) in LISTLIKE else {x})

