# yapf


class BasePiping(object):  # type: ignore
    ...


class BasePiping(object):
    def __add__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement +')

    def __sub__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement -')

    def __mul__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement *')

    def __matmul__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement @')

    def __truediv__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement /')

    def __floordiv__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement //')

    def __mod__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement %')

    def __divmod__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement divmod')

    def __pow__(self, other, modulo=None):
        raise NotImplementedError('Does not implement pow')

    def __lshift__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement <<')

    def __rshift__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement >>')

    def __and__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement &')

    def __xor__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement ^')

    def __or__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement |')

    def __radd__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement righthand +')

    def __rsub__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement righthand -')

    def __rmul__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement righthand *')

    def __rmatmul__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement righthand @')

    def __rtruediv__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement righthand /')

    def __rfloordiv__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement rightand %')

    def __rmod__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement righthand %')

    def __rdivmod__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement righthand divmod')

    def __rpow__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement righthand pow')

    def __rlshift__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement righthand +')

    def __rrshift__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement righthand +')

    def __rand__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement righthand +')

    def __rxor__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement righthand +')

    def __ror__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement righthand +')

    def __iadd__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement +=')

    def __isub__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement -=')

    def __imul__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement *=')

    def __imatmul__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement +')

    def __itruediv__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement +')

    def __ifloordiv__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement +')

    def __imod__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement %=')

    def __ipow__(self, other, modulo=None):
        raise NotImplementedError('Does not implement **=')

    def __ilshift__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement <<=')

    def __irshift__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement >>=')

    def __iand__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement +')

    def __ixor__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement +')

    def __ior__(self, other) -> BasePiping:
        raise NotImplementedError('Does not implement +')

    def __neg__(self) -> BasePiping:
        raise NotImplementedError('Does not implement +')

    def __pos__(self) -> BasePiping:
        raise NotImplementedError('Does not implement +')

    def __abs__(self) -> BasePiping:
        raise NotImplementedError('Does not implement +')

    def __invert__(self) -> BasePiping:
        raise NotImplementedError('Does not implement +')

    def __int__(self) -> BasePiping:
        return int(self.result)

    def __float__(self) -> BasePiping:
        raise float(self.result)
