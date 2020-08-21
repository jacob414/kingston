# yapf
"""
A couple of typical development tools I tend to use..
"""
from textwrap import dedent
from itertools import count


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
