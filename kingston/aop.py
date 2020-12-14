from typing import Any, Callable, Collection
from functools import wraps
from pyrsistent import pmap, PMap


class AspectNotFound(Exception):
    "Raised if no aspect can be found covering a call."


class Aspects(dict):
    """Aspect Oriented Programming as a dict subclass / using decorators.

    """
    def invoke(self, xparams: Collection, xopts: PMap) -> Any:

        for positional, keyed in self.keys():
            if set(xopts) & set(keyed) and (positional, keyed) in self:
                return self[(positional, keyed)](*xparams, **xopts)

        raise AspectNotFound(f"No aspect covers {(xparams, xopts)}")

    def __call__(self, *params, **opts) -> Callable:
        def wrap(decorated: Callable) -> Callable:
            @wraps(decorated)
            def call(*xparams: Any, **xopts: Any) -> Any:
                return self.invoke(xparams, pmap(xopts))

            self[(params, pmap(opts))] = decorated
            return call

        return wrap
