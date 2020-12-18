# yapf
import pytest

from typing import Any, Mapping

from kingston.testing import fixture
from kingston.decl import box
from kingston import aop
from kingston.aop import Aspects

from hypothesis import given
from hypothesis import strategies as st

import io
import sys
import os
import doctest as dt

from functools import partial

import funcy as fy

pytestmark = pytest.mark.bbox


@fixture.doctest(aop.Aspects)
def test_doctest_Aspects(doctest):
    assert doctest() == ''
