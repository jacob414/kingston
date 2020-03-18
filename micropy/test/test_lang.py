# yapf

import pytest

from micropy import lang
from micropy.testing import fixture

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


int_or_same = lang.coerce_or_same(int)


@fixture.params("value, expected", (1, 1), ('1', 1), ('x', 'x'))
def test_coerce_or_same(value: Any, expected: Any) -> None:
    "Should convert strings with digits to `int`."
    assert int_or_same(value) == expected


@pytest.fixture
def xe() -> lang.XE:
    yield lang.XE(foo='foo', bar='bar')


def test_xe_as_obj(xe: lang.XE) -> None:
    "Should "
    assert xe.foo == 'foo'


def test_xe_as_dict(xe: lang.XE) -> None:
    "Should be able to index XE object as dictionaries"
    assert xe['foo'] == 'foo'


@pytest.fixture
def simplest_pipe() -> lang.Piping:
    "A fixture with a Piping object that only supports add."

    class SimplestPipe(lang.Piping):
        def __add__(self, value) -> None:
            "Does __add__"
            self.queue(ops.add, value)
            return self

    return SimplestPipe(10)


def test_piping_simplest(simplest_pipe) -> None:
    "Should piping_simplest"
    res = simplest_pipe + 10 + 20
    assert res() == 40


@pytest.mark.xfail(raises=NotImplementedError)
def test_piping_simplest_restrictive(simplest_pipe) -> None:
    "Should piping_simplest_restrictive1"
    simplest_pipe + 10 - 20


class FilterPipeExample(lang.Piping):
    def __add__(self, value) -> lang.Piping:
        "Add operation"
        self.queue(ops.add, value)
        return self


filter_from_8 = lambda: (FilterPipeExample(
    8, kind=filter, format=(lambda x: x > 10)) + 1 + 1)


@fixture.params("fpipe, param, want",
   (filter_from_8(),
   (8, 9, 10, 11, 12),
   (11,12)
))  # yapf: disable
def test_piping_as_filter_simple(fpipe: FilterPipeExample, param: tuple,
                                 want: tuple) -> None:
    """Piping object should be able to work as filters provided a
    formattting function is specified.

    """
    was = tuple(filter(fpipe, param))
    assert was == want


def test_more_filter() -> None:
    "Should more_filter"
    pass


def test_piping_as_mapping() -> None:
    """Piping objects derived from `ComposePiping` should always support
    the bitwise pipe (`'|'`) operatror as a simple function
    composition.

    """
    incr = lambda x: x + 1
    showr = "It is {}!".format
    assert (lang.ComposePiping(5) >> incr >> incr >> showr)() == "It is 7!"


got_a, got_b, none = E(a=1), E(b=1), E(c=1)
got_ab, got_bc = E(a=1, b=1), E(b=1, c=1)

has = lambda name: lambda obj: hasattr(obj, name)

only_a = lambda: lang.LogicPiping() // has('a')
a_and_b = lambda: lang.LogicPiping() // has('a') & has('b')
either = lambda: lang.LogicPiping() // has('a') | has('b')
a_or_b = lambda: lang.LogicPiping() // has('a') | has('b')


class LogicAndCount(lang.CountPiping, lang.LogicPiping):
    pass


@fixture.params(
    "lpipe, param, want",
    (only_a(), got_a, got_a),
    (only_a(), got_bc, False),
    (a_or_b(), got_a, got_a),
    (either(), got_b, got_b),
    (a_or_b(), got_bc, got_bc),
    (a_and_b(), got_bc, False),
    (lang.LogicPiping() // has('a') & lang.PNot(has('b')), got_ab, False),
    (LogicAndCount(format=bool) + 1 >= 2, 1, True),
    (LogicAndCount(format=bool) + 1 >= 3, 1, False),
    (LogicAndCount(format=bool) + 1 > 1, 1, True),
    (LogicAndCount(format=bool) + 1 > 1, 1, True),
    (LogicAndCount(format=bool) + 1 == 2, 1, True),
    (LogicAndCount(format=bool) + 1 == 3, 1, False),
    (LogicAndCount(format=bool) + 1 != 2, 1, False),
    (LogicAndCount(format=bool) + 1 != 3, 1, True),
    (LogicAndCount(format=bool) + 1 & lang.PNot(2), 1, False),
)
def test_logic_piping(lpipe, param, want) -> None:
    "Should logic_piping"
    assert lpipe(param) == want


def dispr() -> lang.Match:
    "Does dispr"

    disp = lang.Match({int: lambda x: x + 1})

    @disp.case
    def add_two_int(self, a: int, b: int) -> int:
        "Fixture function: called with 2 integers, should add the integers."
        return a + b

    return disp


@pytest.mark.wbox
@fixture.params("disp, params, expected",
  (dispr(), (1, ), 2),
  (dispr(), (1, 2), 3),
)  # yapf: disable
def test_callbytype_variants(disp, params, expected) -> None:
    "Should dispatch calls to correct function based on instance types."
    assert disp(*params) == expected
