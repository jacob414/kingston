# yapf

import os

from typing import (Any, Type, Iterator, Iterable, Tuple, Mapping, Dict,
                    Generator, Callable, Union, Collection, cast)
from itertools import zip_longest as zip

import funcy as fy  # type: ignore
from whatever import _  # type: ignore

from funcy import compact, flatten, walk
from . import lang

import inspect
from inspect import Parameter

from kingston import decl
from kingston.decl import box, unbox, Singular
from kingston import xxx_kind as kind

POSITIONAL = (Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD)
KEYWORD = (Parameter.KEYWORD_ONLY, )


class Default:
    "Symbol for a default function to call if no matching was made."


class Mismatch(ValueError):
    pass


class Conflict(TypeError):
    pass


class Malformed(ValueError):
    pass


SingularTypeCand = Type[Any]
ComplexTypeCand = Iterable[SingularTypeCand]
TypePatternCand = Union[Singular, ComplexTypeCand]
PatternCand = Union[decl.Singular, Iterable[decl.Singular]]
FoundPattern = Union[PatternCand, object, Collection[decl.Singular]]


class Miss:
    "Symbol for a non-breaking miss."


ispos = lambda p: p.kind in POSITIONAL and p or False
iskw = lambda p: p.kind in KEYWORD and p or False


def primparams(fn: Callable) -> Union[Singular, Tuple[Any]]:
    "Aproximate type signature of function `fn´ in Python primitive types"
    fullparams = lang.params(fn)  # type: ignore

    params = lambda: filter(lambda p: p.default is inspect.Signature.empty,
                            fullparams.values())

    positional = map(_.annotation, filter(ispos, params()))
    keyword = map(_.annotation, filter(iskw, params()))

    kind = _.kind

    variadic = tuple(... for x in fullparams.values()
                     if kind(x) == Parameter.VAR_POSITIONAL) + tuple(
                         Mapping for x in fullparams.values()
                         if kind(x) == Parameter.VAR_KEYWORD)

    return unbox(tuple(fy.chain(positional, keyword, variadic)))


def match(cand: PatternCand, pattern: Union[Iterable, Any,
                                            decl.Singular]) -> bool:
    cand = kind.cast_to_hashable(cand)
    pattern = kind.cast_to_hashable(pattern)

    accepted = {cand, Any}

    return True if pattern in accepted else False


def wildcarded(pairs: Iterator) -> FoundPattern:
    return cast(FoundPattern,
                tuple((p_ is Any and Any or c_ for c_, p_ in pairs)))


@fy.curry
def match_in_level(cand, p_):
    if wildcarded(zip(cand, box(p_))) == p_:
        return p_
    else:
        return ()


def trynested(cand, pattern):
    "Search a tree for `pattern`."
    return compact(flatten(walk(match_in_level(cand), pattern)))


def genmatches(cand: PatternCand,
               pattern: FoundPattern) -> Generator[Any, None, None]:
    "Generator that yields sub-patterns found in `pattern`."

    icand, ipattern = box(cand), box(pattern)

    for cval, pval in zip(icand, ipattern):
        if cand in box(pattern):
            # Handles the simplest reality
            yield cand
        else:
            if match(cval, pval):
                yield pval
                continue
            elif not match(cval, pval):
                yield Miss
                continue

    # later, more expensive option, pattern hides inside a tree
    deephit = tuple(pv for pv, b in zip(trynested(icand, ipattern), icand)
                    if match(b, pv))
    if deephit:
        yield deephit


def matches(
    cand: Any,
    pattern: Iterable[Any],
) -> FoundPattern:
    """Decides how composite data structures should be matched, performs
    matching.

    Match failure = raise `Mismatch` exception.
    """

    icand = box(cand)
    ipattern = box(pattern)

    if icand == ipattern:
        return cast(FoundPattern, pattern)

    if fy.is_seqcoll(cand):
        cand = cast(Iterable, cand)

    if Any in ipattern and all(
            match(c_, p_) for c_, p_ in zip(icand, ipattern)):
        return pattern

    for matchcand in genmatches(cand, pattern):
        wildcard = wildcarded(zip(icand, box(matchcand)))
        if wildcard == matchcand:
            return wildcard
        elif cand == matchcand:
            return cand

    raise Mismatch(
        f"kingston.match.matches(): Can't find {cand!r} in {pattern!r}")


def arg_symbolic(params: Iterable, opts: Mapping):
    compacted = fy.compact((*params, opts))
    return tuple((Mapping if type(p) is dict else p) for p in compacted)


def resolve_pattern(params: Any, opts: Any) -> TypePatternCand:
    return unbox(arg_symbolic(params, opts))


class Match(dict):
    """Multiple dispatch as a callable subclass of `dict`:

    Define a mapping of types. Call for an instance, the parameter
    type should be mapped by `type(obj)` returning a callable that
    will further process the instance.

    """
    def explain(self, out=False):  # pragma: nocov
        lines = (f"- A {self.__class__.__name__}", )
        for matching in self:
            fn = self[matching]
            lines = (*lines, f"    - {matching!r} : {kind.nick(fn)}")

        text = os.linesep.join(lines)
        if out:
            print(text)
        else:
            return text

    @property
    def __name__(self):
        return self.__class__.__name__

    def checkpred(self, key: Any, value: Any) -> None:
        try:
            key = unbox(key)
            confl = self[key]
            raise Conflict(f'Pattern {key} had a previous conflict '
                           f'{key}={confl}')
        except KeyError:
            pass

    def case(self, *args: Any) -> Callable:
        """Decorator to add a function. The types that will be matched is
        taken from the signature of the decorated function.

        """
        fn = fy.first(args)
        disp = primparams(fn)
        self.checkpred(disp, None)
        self[disp] = fn

        return fn

    def default(self, fn):
        "Assigns a default matching"
        self[Default] = fn
        return fn

    def type_match(self, *params: Any, **opts: Any) -> Any:
        "Does type_match"
        T = resolve_pattern(params, opts)

        if fy.is_seqcoll(T):
            # T = cast(ComplexTypeCand, tuple(type(p) for p in T))
            T = cast(ComplexTypeCand, kind.xrtype(T))
        elif T is Mapping:  # keyword arg only
            pass
        else:
            T = type(T)  # type: ignore

        try:
            key = matches(T, tuple(self))
        except Mismatch:
            if Default in self:
                key = Default
            else:
                raise

        call = self[key]

        return call(*box(unbox(params)), **opts)

    def __call__(self, *params: Any, **opts: Any) -> Union[Tuple[Any], Tuple]:
        "Return the value keyed by the type of parameter `obj`"
        return self.type_match(*params, **opts)

    def __setitem__(self, key: Any, value: Any) -> None:
        "Insert new matching, but check for pre-existing matches first."
        self.checkpred(key, value)
        super().__setitem__(key, value)


class VMatch(Match):
    def checkpred(self, key: Any, value: Any) -> None:
        super().checkpred(key, value)
        try:
            key = unbox(key)
            confl = self[key]
            raise Conflict(
                f'Pattern {key} could already be type matched ({confl}).')
        except KeyError:
            pass

    def value_match(self, *params, **opts):
        """
        Match parameters by value

        """
        fparams = unbox(params)
        try:
            key = matches(fparams, tuple(self))
        except Mismatch:
            if Default in self:
                key = Default
            else:
                raise

        call = self[key]
        return call() if lang.arity(call) == 0 else call(*fparams, **opts)

    def case(self, *params: Any, **opts: Any) -> Callable:
        """Decorator to add a function. The types of the parameters. The types
        that will be matched is taken from the signature of the
        decorated function.

        """
        def wrap(fn, *xparams, **xopts):
            self.checkpred(params, None)
            self[params] = fn
            return fn

        return wrap

    def __call__(self, *params: Any, **opts: Any) -> Union[Tuple[Any], Tuple]:
        """
        Handle call to this instance.
        """
        return self.value_match(*params, **opts)
