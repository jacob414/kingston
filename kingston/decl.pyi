from typing import Any, Callable, Set, Union

PRIMTYPES: Any
LISTLIKE: Any
TEXTLIKE: Any
MUTABLE: Any
Primitive = Union[int, bool, float, str, set, list, tuple, dict, bytes]
Listlike = Union[set, list, tuple]
Singular = Union[Primitive, Callable]
textual: Any
numeric: Any
isint: Any
isdict: Any
isgen: Any

def unbox(x: Any) -> Singular: ...
def box(x: Any) -> Any: ...
def setof(x: Any) -> Set: ...
