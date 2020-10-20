# yapf

import pytest

from kingston import lang
from kingston import match
from kingston.testing import fixture

from typing import Any
import operator as ops
from altered import E


@pytest.fixture
def rgen() -> None:
    "A fixture with a recursive generator expression"
    return (e for e in (1,
                        2,
                        (e for e in range(31, 34)),
                        4,
                        (e for e in range(51, 54))))  # yapf: disable


def test_unfold_gen(rgen) -> None:
    "Should unfold a recursive generator correctly."
    assert lang.unfold_gen(rgen) == (1, 2, 31, 32, 33, 4, 51, 52, 53)


class Dispatching(object):
    @lang.methdispatch
    def reflect(self, arg):
        raise NotImplementedError("Not implemented for {}".format(type(arg)))

    @reflect.register(list)
    def _(self, alist):
        return (list, alist)

    @reflect.register(int)
    def _(self, anint):
        return (int, anint)


@pytest.fixture
def Dispatcher():
    yield Dispatching


def test_methdispatch(Dispatcher: Dispatching) -> None:
    "Should dispatch per type"
    assert Dispatcher().reflect([1, 2]) == (list, [1, 2])


@pytest.fixture
def Alt():
    "Does Alt"
    yield lang.mkclass('Alt')


def test_mkclass_classmethod(Alt: Any) -> None:
    "Should be able to declare dynamic class methods"

    @Alt.classmethod
    def cmeth(cls, x, y) -> int:
        "Does cmeth"
        return x + y

    sum = Alt.cmeth(1, 1)
    assert sum == 2, \
        "Expected 2, got {}".format(sum)


def test_mkclass_staticmethod(Alt: Any) -> None:
    "Should be able to declare dynamic class methods"

    @Alt.staticmethod
    def smeth(x, y):
        "Does cmeth"
        return x + y

    sum = Alt.smeth(1, 1)
    assert sum == 2, \
        "Expected 2, got {}".format(sum)


def test_method_on_type_0param(Alt: Alt) -> None:
    "Should handle methods without parameters correctly"

    @Alt.method
    def paramless_method(self: Alt):
        "An example parameterless method"
        self.foo = id(self)

    alt0 = Alt()
    alt0.paramless_method()
    assert type(alt0.foo) is int


def test_method_on_type_nary(Alt: Alt) -> None:
    "Should"

    @Alt.method
    def meth_on_type(self: Alt, foo: str):
        "Does meth_on_type"
        self.foo = foo

    alt0 = Alt()
    alt0.meth_on_type('bar')
    assert alt0.foo == 'bar'


@fixture.params(
    "func, expected",
    ((lambda: 0), 0),
    ((lambda x: x), 1),
    ((lambda x, y: (x, y)), 2),
    ((lambda x, y, z: x), 3),
)
def test_arity(func, expected) -> None:
    "Should arity"
    assert lang.arity(func) == expected


def test_mkclass_bound_method(Alt: Alt) -> None:
    "Should be able to add methods to individual objects."
    alt1, alt2 = Alt(), Alt()

    @alt1.method
    def amethod(self: Alt, foo: int):
        "Does _"
        self.bar = foo + 1

    alt1.amethod(1)
    assert alt1.bar == 2
    assert not hasattr(alt2, 'amethod')


@fixture.params(
    "type_, expected",
    (int, True),
    (bool, True),
    (float, True),
    (str, True),
    (set, True),
    (list, True),
    (dict, True),
    (object, False),
    ('', False),
    (1, False),
)
def test_isprim_type(type_: type, expected: Any) -> None:
    "Should work"
    assert lang.isprim_type(type_) == expected


# int_or_same = lang.coerce_or_same(int)


@fixture.params("value, expected", (1, 1), ('1', 1), ('x', 'x'))
def test_coerce_or_same(value: Any, expected: Any) -> None:
    "Should convert strings with digits to `int`."
    assert lang.num_or_else(value) == expected


@pytest.mark.wbox
def test_pubvars_dict() -> None:
    assert set(lang.pubvars({'x': 'x', 'y': 'y'})) == {'x', 'y'}


@pytest.mark.wbox
def test_pubvars_list() -> None:
    assert set(lang.pubvars([1, 2, 3])) == {1, 2, 3}


@pytest.mark.wbox
def test_pubvars_obj() -> None:
    "Should pubvars"

    class Cls(object):
        def __init__(self, x, y):
            self.x = x
            self.y = y

    assert set(lang.pubvars(Cls('x', 'y'))) == {'x', 'y'}


@pytest.mark.wbox
@fixture.params(
    "obj, name",
    ('Hello', 'str'),
    (None, 'None'),
    (E(a=1), 'Expando'),
)
def test_typename(obj, name) -> None:
    "Should typename"
    assert lang.typename(obj) == name


def test_primbases() -> None:
    """Should return the primitive baseclasses from an object
    deriving from a primitive type.

    """
    class FromPrim(int):
        pass

    assert lang.primbases(FromPrim) == [int]
