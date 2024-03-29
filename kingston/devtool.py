# yapf
"""
A couple of typical development tools I tend to use..
"""
import sys
from typing import Any, Callable, Iterable, Mapping

from itertools import count
import textwrap
import hashlib

import pprint

import funcy as fy  # type: ignore


def fingerprint(obj: Any) -> str:
    return hashlib.sha1(obj).hexdigest()[0:6]


def explore(obj: Any) -> str:
    """Formats a representaion of any object, also following opaque
    objects to see what's inside.

    Uses package `jsonpickle` in combination with built-in modules
    `json` and `pprint`.

    """
    import jsonpickle as jp
    from json import loads
    return pprint.pformat(loads(jp.dumps(obj)))


class PrintfDebugging:
    """Documentation for PrintfDebugging

    """
    def __init__(self, say=print, indent=2):
        self.spaces = ''
        self.steps = indent
        self.say = say

    def indent(self, extra=None):
        if extra is not None:
            self.steps = extra

        indentation = self.steps * ' '

        self.spaces = self.spaces + indentation

    def dedent(self):
        self.spaces = self.spaces[:-self.steps]

    def silent(self):
        self.say = fy.identity

    def loud(self):
        self.say = print

    def __call__(self, formatted, **kwargs):
        try:
            dedented = textwrap.dedent(formatted)
        except TypeError:
            dedented = pprint.pformat(formatted)
        try:
            self.say(self.spaces + dedented.format(**kwargs))
        except AttributeError:
            self.say(self.spaces + dedented)


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
