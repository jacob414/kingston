# yapf
import pytest

from micropy import primitives as P


def incr(x: int) -> int:
    return x + 1


def test_pipe_experiment():
    # type: () -> None
    "Should 1. add 1, 2. add 1, 3. profit?"
    showr = "It is {}!".format

    assert (P.PipingExperiment(5) | incr | incr | showr).result == "It is 7!"
