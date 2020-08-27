# yapf
"""
A couple of typical development tools I tend to use..
"""
from typing import Any, Callable, Iterable, Mapping

from itertools import count
from textwrap import dedent


def out(formatted, **kwargs):
    print(dedent(formatted.format(**kwargs)))


class LoopSentinel(object):
    """Documentation for LoopSentinel

    """
    def __init__(
        self,
        limit=20,  # a somewhat informed guess, at least I tend to start here
        msgfmt="Halting prob? Round {round} of {limit}"):
        self.limit = limit
        self.rounds = count(0)
        self.msgfmt = msgfmt

    def guard(self):
        cur = next(self.rounds)
        if cur >= self.limit:
            # Oops, crash out of whatever
            raise NotImplementedError(
                self.msgfmt.format(round=cur, limit=self.limit))


out = print


def trial(
    num: int,
    fn: Callable,
    params: Iterable,
    kwargs: Mapping,
    result: Any,
    failmsg: str = None,
) -> Any:
    if failmsg is None:
        failmsg = "FAIL: {num} raised {exc}. ({fn})(*{params}, **{kwargs})"
    try:
        ret = fn(*params, **kwargs)
        assert ret == result
        out(f"OK: {num}")
        return ret
    except AssertionError:
        out(f"FAILED {num} result wrong {ret!r}")
        retry = retryit()
    except Exception as exc:
        out(failmsg.format(**locals()))
        retry = retryit()

    if retry:
        import ipdb
        ipdb.set_trace()
        ret = fn(*params, **kwargs)
        out(f"   retried, was now {ret!r}")
        return ret
    else:
        return f'*{num} failed*'
