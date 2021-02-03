# yapf
import pytest

from typing import Any, Mapping

from kingston.testing import fixture
from kingston.decl import box

from kingston import xxx_kind as kind

from hypothesis import given
from hypothesis import strategies as st

import io
import sys
import os
import doctest as dt

from functools import partial

import funcy as fy

pytestmark = pytest.mark.wbox


@fixture.doctest(kind.nick)
def test_doctest_nick(doctest):
    assert doctest() == ''

@fixture.doctest(kind.typenick)
def test_doctest_typenick(doctest):
    assert doctest() == ''

@fixture.doctest(kind.deepxrtype)
def test_doctest_deepxrtype(doctest):
    assert doctest() == ''


@fixture.params(
    "param, expected",
    (1, 'int'),
    ([1, 2], 'list'),
    (None, 'None'),
)
def test_nick(param, expected) -> None:
    "Should nick"
    assert kind.nick(param) == expected


@fixture.params("param, expected",
                (1, int),
                ('x', str),
                ((), tuple),
                ((1, 2), (int, int)),
                ([1,2], [int, int]),
)  # yapf: disable
def test_xrtype(param, expected) -> None:
    "Should xrtype"
    assert kind.xrtype(param) == expected


@fixture.params("param, sibling, expected",
                ((1, ), [1], [1]),
                ((1, 2, 3), [], [1, 2, 3]),
                (1, '', '1'),
                (1, 1, 1)
)  # yapf: disable
def test_uniform(param, sibling, expected) -> None:
    "Should "
    assert kind.uniform(param, sibling) == expected


def test_uniform_failure() -> None:
    "Should uniform_failure"
    with pytest.raises(TypeError):
        kind.uniform('x', 1)


@pytest.mark.parametrize("obj", ((
    (1,),
    ('x',),
    ([1, 2, 3]),
    ({'a':1}),
)))  # yapf: disable
def test_hashing_fns(obj) -> None:
    "Should hashing_fns"
    assert type(kind.anyhash(obj)) == type(hash('x'))


@given(st.one_of(st.integers(), st.none(), st.floats(), st.tuples()))
def test_stress_deepxrtype(value):
    kind.deepxrtype(value)


def one_int(x: int) -> int:
    return 1.0


def two_int(a: int, b: int) -> int:
    return a + b


def one_int_and_kw(a: int, **kwargs: Any):
    return a


def only_kw(**kwargs):
    return Mapping


@fixture.params(
    "fn, params",
    (one_int, int),
    (only_kw, Mapping),
    (two_int, (int, int)),
    (one_int_and_kw, (int, Mapping)),
)
def test_primparams(fn, params) -> None:
    "Should convert function signatures to Python primitive(s)."
    assert kind.primparams(fn) == params
