# yapf

import pytest

from altered import E

from micropy import dig
from micropy import testing

from hypothesis import given
from hypothesis import strategies as st

import math
from typing import Any


@given(st.deferred(lambda: st.integers() | st.floats() | st.text()))
def test_xget_prim(param: Any) -> None:
    "Does test_xget_prim"
    result = dig.xget(param, 1)
    assert result == param or all(map(math.isnan, (param, result)))


def test_xget_indexed_iter():
    # type: () -> None
    "Does test_xget_indexed"
    assert dig.xget((1, 2, 3), 1) == 2


def test_xget_indexed_dict():
    # type: () -> None
    "Does test_xget_indexed"
    assert dig.xget({'foo': 'bar'}, 'foo') == 'bar'


def test_xget_object():
    # type: () -> None
    "Should obj"
    assert dig.xget(E(foo='bar'), 'foo') == 'bar'


def test_xget_fn():
    # type: () -> None
    "Should get from function (?)"
    assert dig.xget(lambda x: x + 1, 1) == 2


def test_xget_glob_keys_all():
    # type: () -> None
    "Should get keys of dict"
    obj = {'foo': 1, 'bar': 2}
    resultset = dig.xget(obj, '*')
    textual = str(resultset)
    assert textual == '[foo=1:int, bar=2:int]'


def test_xget_glob_keys_some():
    # type: () -> None
    "Should get keys of dict"
    assert str(dig.xget({
        'foo': 1,
        'bar': 2,
        'fx': 2
    }, 'f*')) == '[foo=1:int, fx=2:int]'


@pytest.mark.parametrize("itr",(
    ['foo', 'bar', 'fx'],
    ('foo', 'bar', 'fx'),
))
def test_xget_glob_members_some(itr):
    # type: () -> None
    "Should get keys of a sequence/collection"
    
    assert str(dig.xget(itr, 'f*')) == "['foo', 'fx']"


def test_xget_glob_attrs_all():
    # type: () -> None
    "Should get keys of dict"
    assert str(dig.xget(E(foo=1, bar=2), '*')) == '[bar=2:int, foo=1:int]'


def test_xget_glob_attrs_some():
    # type: () -> None
    "Should get keys of object"
    assert str(dig.xget(E(foo=1, bar=2), 'f*')) == '[foo=1:int]'


def test_dig_iter():
    # type: () -> None
    "Should "
    assert dig.dig((1, 2, 3, (41, 42, 43)), "3.0") == 41


def test_dig_dict_iter():
    # type: () -> None
    "Should "
    assert dig.dig({'foo': (1, 2)}, 'foo.0') == 1


def test_dig_dict_nested():
    # type: () -> None
    "Should "
    assert dig.dig({'foo': {'bar': 'baz'}}, 'foo.bar') == 'baz'


def test_dig_object():
    # type: () -> None
    "Should "
    assert dig.dig(E(foo='bar', bar=E(jox='jox')), 'bar.jox') == 'jox'


def test_dig_complex():
    # type: () -> None
    "Should "
    ob = E(foo=1, bar=2, fx=(1, 2, 3))
    assert dig.dig(ob, 'f*.1.0') == 1


@pytest.fixture
def attr() -> dig.Attr:
    "Does attr"
    inst = dig.Attr.infer('foo', 'bar')
    return inst


def test_attr_eq(attr: dig.Attr) -> None:
    "Should equal"
    assert attr.eq(dig.Attr.infer('foo', 'bar'))


def test_attr_typecheck(attr: dig.Attr) -> None:
    "Should typecheck"
    assert attr.isa(dig.Attr)


def test_sibling(attr: dig.Attr) -> None:
    "Should be able to test instances for same type as other instance"
    assert attr.sibling(dig.Attr.infer('bar', 'baz'))


@pytest.fixture
def tup_a() -> dig.TupleAttr:
    "Does tupe_attr"
    yield dig.TupleAttr.infer('foo', (1, 2, 3))


def test_tuple_attr_eq(tup_a: dig.TupleAttr) -> None:
    "Should be sane"
    assert tup_a.eq(dig.TupleAttr.infer('foo', (1, 2, 3)))


@testing.fixture.params(
    "PrimType, value",
    (int, 1),
    (tuple, (1, 2)),
    (float, 1.1),
    (str, 'abcd'),
)
def test_infer(PrimType: type, value: Any) -> None:
    "Should create attribute"
    name = str(type(value))
    attr = dig.Attr.infer(name, value)
    same = dig.Attr.infer(name, value)
    assert attr.name == name
    assert attr.PrimType == PrimType
    assert attr == same
