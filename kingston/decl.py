# yapf
# strict types

from typing import (Any, Mapping, Callable, Union, Set, cast)
import numbers
import funcy as fy  # type: ignore
import types
import operator

import inspect
from inspect import Parameter

PRIMTYPES = {int, bool, float, str, set, list, tuple, dict, bytes}
LISTLIKE = {set, list, tuple}
TEXTLIKE = {str, bytes}
MUTABLE = {list, set, dict}

Primitive = Union[int, bool, float, str, set, list, tuple, dict, bytes]
Listlike = Union[set, list, tuple]
Singular = Union[Primitive, Callable]
Plural = Union[set, list, tuple, dict]
Dualism = Union[Singular, Plural]

PipeCombineFn = Callable[[Any, None, None], Any]

textual = fy.isa(*TEXTLIKE)
numeric = fy.isa(numbers.Number)
isint = fy.isa(int)
isdict = fy.isa(dict)
isgen = fy.isa(types.GeneratorType)
iseq = fy.curry(operator.eq)


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
    return x[0] if fy.is_seqcoll(x) and len(x) == 1 else x


def box(x: Any) -> Any:
    return x if type(x) in LISTLIKE else (x, )


def setof(x: Any) -> Set:
    return cast(Set, set(x) if type(x) in LISTLIKE else {x})


def params(fn: Callable) -> Mapping[str, Parameter]:
    return inspect.signature(fn).parameters
