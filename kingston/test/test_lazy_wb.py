# yapf

from kingston.testing import fixture
import pytest

from kingston import lang

from altered import state, E

from os.path import join, dirname, realpath

from kingston import xxx_kind as kind
from kingston import lazy


from hypothesis import given
from hypothesis import strategies as st

pytestmark = pytest.mark.wbox

@pytest.fixture
def genlist():
    return lazy.GListlike(e for e in (1,2,3))


@fixture.params("index, expected",
                (0, 1),
                (1, 2),
                (2, 3),
                )  # yapf: disable
def test_index(genlist, index, expected) -> None:
    "Should describe"
    assert genlist[index] == expected

def test_len(genlist):
    assert len(genlist) == 3

def test_range(genlist):
    assert genlist[0:1] == [1,2]

def test_str(genlist) -> None:
    "Does test_str"
    assert str(genlist) == '[1, 2, 3] (GListlike)'

def test_repr(genlist) -> None:
    "Does test_str"
    assert repr(genlist) == f'<GListlike, [1, 2, 3]>'
