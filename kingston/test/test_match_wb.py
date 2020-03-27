# yapf

import pytest

from typing import Any
from kingston.testing import fixture
from kingston.dig import dig

import funcy
from funcy import flow

from kingston.match import Match, VMatch, Mismatch

pytestmark = pytest.mark.wbox

# Simplified mirroring paramtrically lax ident, for testing convenience
same = lambda *args, **kwargs: args[0] if len(args) == 1 else args


@pytest.fixture
def match() -> Match:
    "A fixture for type matches."
    return Match({
        int: lambda x: x + 4,
        str: lambda s: f"Hello, {s}!",
        (int, str): (lambda amount, chr_: amount*chr_),
        (int, Any): (lambda amount, obj: 10 - amount)
    })


@fixture.params("param, expected",
    (1, 5),
    ('World', 'Hello, World!'),
    ((3, 'x'), 'xxx'),
                ((5, 5), 5),
)  # yapf: disable
def test_match_hits(match, param, expected) -> None:
    "Should hit known values"
    assert match(param) == expected


@pytest.mark.parametrize("param", (
    'x',
    ('x', 'y'),
    2,
    'a0',
    (1, '+', 1),
))  # yapf: disable
def test_vmatch_hits(vmatch, param) -> None:
    "Should hit known values"
    assert vmatch(param) == param


@pytest.fixture
def vmatch() -> VMatch:
    "A fixture for value matches."
    return VMatch({
        ('x', ): same,
        ('x', 'y'): same,
        ((lambda x: x == 2), ): same,
        ('a0', ): (lambda: 'a0'),
        (Any, '+', Any): same,
    })


@pytest.mark.parametrize("param", (
    'x',
    ('x', 'y'),
    2,
    'a0',
    (1, '+', 1),
))  # yapf: disable
def test_vmatch_hits(vmatch, param) -> None:
    "Should hit known values"
    assert vmatch(param) == param


@pytest.mark.parametrize("param", (
    'a',
    ('x', 'y', 'z'),
    1,
    0,
))  # yapf: disable
def test_vmatch_misses(vmatch, param) -> None:
    "Should miss values known not to be present."
    with pytest.raises(Mismatch):
        vmatch(param)
