# yapf

from kingston.testing import fixture
import pytest

from kingston import lang

from altered import state, E

from os.path import join, dirname, realpath

from kingston import xxx_kind as kind

from hypothesis import given
from hypothesis import strategies as st

# pytestmark = pytest.mark.wbox


class Sample(object):
    """Documentation for Sample

    """
@fixture.params("value, expected",
                (1, (int, )),
                ('x', (str,)),
                ((10, 'x', ('y', 'z')), (int, str, (str, str))),
                (Sample, ('Sample',)),
                )  # yapf: disable
def test_describe(value, expected) -> None:
    "Should describe"
    assert kind.describe(value) == expected


@given(st.one_of(st.integers(), st.none(), st.floats(), st.tuples()))
def test_stress_describe(value):
    kind.describe(value)
