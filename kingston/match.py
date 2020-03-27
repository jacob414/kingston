# yapf

from typing import Any, Iterable, Callable, Union
import itertools
import funcy  # type: ignore
from funcy import flow
from functools import partial
from . import lang

import inspect


class Mismatch(ValueError):
    pass


class Conflict(TypeError):
    pass


class Match(dict):
    """Multiple dispatch as a callable subclass of `dict`:

    Define a mapping of types. Call for an instance, the parameter
    type should be mapped by `type(obj)` returning a callable that
    will further process the instance.

    """
    def checkpred(self, key: Any, value: Any) -> None:
        if key in self:
            confl = self[key]
            raise Conflict(f'Pattern {key} had a previous conflict '
                           f'{key}={confl}')

    @staticmethod
    def wccmp(needle: Any, match: Any):
        if match is Any:
            return True
        elif callable(match):
            return flow.silent(match)(needle)
        else:
            return needle == match

    def case(*params: Any) -> Callable:
        """Decorator to add a function. The types of the parameters. The types
        that will be matched is taken from the signature of the
        decorated function.

        """
        self, fn = params
        disp = tuple(arg.annotation
                     for arg in inspect.signature(fn).parameters.values())

        self[disp] = fn

        return fn

    def type_match(self, call: Callable, *params: Any, **opts: Any) -> Any:
        "Does type_match"
        fparams = tuple(funcy.flatten(params))
        T = tuple(type(p) for p in fparams)
        if len(T) == 1:
            call = self[T[0]]
        else:
            scan = partial(self.wc_scan, call, fparams, **opts)
            call = funcy.fallback(lambda: self[T],
                                  lambda: self[type(T)],
                                  scan)  # yapf: disable
        return call() if lang.arity(call) == 0 else call(*fparams, **opts)

    def wc_scan(self, call: Callable, values: Iterable, **opts: Any):
        for preds, fn in self.items():
            if callable(preds) and flow.silent(preds)(*values, **opts):
                call = fn
            elif funcy.iterable(preds):
                for pred in preds:
                    if all(
                            VMatch.wccmp(a, b)
                            for a, b in itertools.zip_longest(values, preds)):
                        call = fn
        return call

    def __call__(self, *params: Any,
                 **opts: Any) -> Union[Iterable[Any], Iterable]:
        "Return the value keyed by the type of parameter `obj`"
        call = flow.raiser(Mismatch,
                           f"Match: no match for parameters {params!r}")
        return self.type_match(call, *params, **opts)

    def __setitem__(self, key: Any, value: Any) -> None:
        "Insert new matching, but check for pre-existing matches first."
        self.checkpred(key, value)
        super().__setitem__(key, value)


class VMatch(Match):
    def checkpred(self, key: Any, value: Any) -> None:
        super().checkpred(key, value)
        try:
            self(key)
            raise Conflict(f'Pattern {key} could already be type matched.')
        except Mismatch:
            pass

    def value_match(self, call: Callable, *params, **opts):
        """
        Match parameters by value
        """
        fparams = tuple(funcy.flatten(params))
        try:
            # Exact match
            call = self[fparams]
        except KeyError:
            for preds, fn in self.items():
                if callable(preds) and flow.silent(preds)(*fparams, **opts):
                    call = fn
                elif funcy.iterable(preds):
                    call = self.wc_scan(call, fparams, **opts)

        return call() if lang.arity(call) == 0 else call(*fparams, **opts)

    def __call__(self, *params: Any,
                 **opts: Any) -> Union[Iterable[Any], Iterable]:
        """
        Handle call to this instance.
        """
        call = flow.raiser(Mismatch,
                           f"Value Match: no match for parameters {params!r}")
        return self.value_match(call, *params, **opts)
