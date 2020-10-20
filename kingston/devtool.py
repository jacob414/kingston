# yapf
"""
A couple of typical development tools I tend to use..
"""
import sys
from typing import Any, Callable, Iterable, Mapping

from itertools import count
import textwrap

import funcy as fy  # type: ignore


class PrintfDebugging(object):
    """Documentation for PrintfDebugging

    """
    def __init__(self, say=print):
        super(PrintfDebugging, self).__init__()
        self.spaces = ''
        self.say = say

    def indent(self):
        self.spaces = self.spaces + '  '

    def dedent(self):
        self.spaces = self.spaces[-2:]

    def silent(self):
        self.say = fy.identity

    def loud(self):
        self.say = print

    def __call__(self, formatted, **kwargs):
        self.say(self.spaces + textwrap.dedent(formatted.format(**kwargs)))


out = PrintfDebugging()


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


def retryit(question="Retry (Y/n)?", default='Y', **kwargs) -> bool:
    "Does retryit"
    while True:
        answer = input(question.format(**kwargs)).upper()
        if answer == 'Y':
            return True
        elif answer == '':
            return True
        elif answer == 'Q':
            sys.exit(0)
        else:
            return False


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
        import ipdb  # type: ignore
        ipdb.set_trace()  # type: ignore
        ret = fn(*params, **kwargs)
        out(f"   retried, was now {ret!r}")
        return ret
    else:
        return f'*{num} failed*'


