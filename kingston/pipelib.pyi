from typing import Any, Optional

class BasePiping: ...

class BasePiping:
    def __add__(self, other: Any) -> BasePiping: ...
    def __sub__(self, other: Any) -> BasePiping: ...
    def __mul__(self, other: Any) -> BasePiping: ...
    def __matmul__(self, other: Any) -> BasePiping: ...
    def __truediv__(self, other: Any) -> BasePiping: ...
    def __floordiv__(self, other: Any) -> BasePiping: ...
    def __mod__(self, other: Any) -> BasePiping: ...
    def __divmod__(self, other: Any) -> BasePiping: ...
    def __pow__(self, other: Any, modulo: Optional[Any]=...) -> None: ...
    def __lshift__(self, other: Any) -> BasePiping: ...
    def __rshift__(self, other: Any) -> BasePiping: ...
    def __and__(self, other: Any) -> BasePiping: ...
    def __xor__(self, other: Any) -> BasePiping: ...
    def __or__(self, other: Any) -> BasePiping: ...
    def __radd__(self, other: Any) -> BasePiping: ...
    def __rsub__(self, other: Any) -> BasePiping: ...
    def __rmul__(self, other: Any) -> BasePiping: ...
    def __rmatmul__(self, other: Any) -> BasePiping: ...
    def __rtruediv__(self, other: Any) -> BasePiping: ...
    def __rfloordiv__(self, other: Any) -> BasePiping: ...
    def __rmod__(self, other: Any) -> BasePiping: ...
    def __rdivmod__(self, other: Any) -> BasePiping: ...
    def __rpow__(self, other: Any) -> BasePiping: ...
    def __rlshift__(self, other: Any) -> BasePiping: ...
    def __rrshift__(self, other: Any) -> BasePiping: ...
    def __rand__(self, other: Any) -> BasePiping: ...
    def __rxor__(self, other: Any) -> BasePiping: ...
    def __ror__(self, other: Any) -> BasePiping: ...
    def __iadd__(self, other: Any) -> BasePiping: ...
    def __isub__(self, other: Any) -> BasePiping: ...
    def __imul__(self, other: Any) -> BasePiping: ...
    def __imatmul__(self, other: Any) -> BasePiping: ...
    def __itruediv__(self, other: Any) -> BasePiping: ...
    def __ifloordiv__(self, other: Any) -> BasePiping: ...
    def __imod__(self, other: Any) -> BasePiping: ...
    def __ipow__(self, other: Any, modulo: Optional[Any]=...) -> None: ...
    def __ilshift__(self, other: Any) -> BasePiping: ...
    def __irshift__(self, other: Any) -> BasePiping: ...
    def __iand__(self, other: Any) -> BasePiping: ...
    def __ixor__(self, other: Any) -> BasePiping: ...
    def __ior__(self, other: Any) -> BasePiping: ...
    def __neg__(self) -> BasePiping: ...
    def __pos__(self) -> BasePiping: ...
    def __abs__(self) -> BasePiping: ...
    def __invert__(self) -> BasePiping: ...
    def __int__(self) -> BasePiping: ...
    def __float__(self) -> BasePiping: ...
