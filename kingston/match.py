# yapf
"""
The Match module
~~~~~~~~~~~~~~~~

This module implements a technique for pattern matching.
"""

import os

from typing import (Any, Type, Iterable, Tuple, Mapping, Callable, Union, Set,
                    List, Dict, Collection, Sequence, TypeVar, Generic, cast)

from . import lang

from kingston import decl
from kingston.decl import box, unbox, Singular
from kingston import xxx_kind as kind
from kingston.xxx_kind import primparams, xrtype  # type: ignore[attr-defined]

SingularTypeCand = Type[Any]
ComplexTypeCand = Iterable[SingularTypeCand]
TypePatternCand = Union[Singular, ComplexTypeCand]
PatternCand = Union[decl.Singular, Iterable[decl.Singular]]
FoundPattern = Union[PatternCand, object, Collection[decl.Singular]]

Plural = Union[Set[Any], List[Any], Tuple[Any, ...], Dict[Any, Any]]
Dualism = Union[Singular, Plural]


class Conflict(TypeError):
    """Exception raised if a pattern to be matched already have been
    applied to a `Matcher` instance.

    """


class Mismatch(ValueError):
    "Exception to signal matching error in Matcher objects."


class Miss:
    "Symbol for a missed match."


class NoNextValue:
    "Symbol signifying that no more values are available to pattern check for."


class NoNextAnchor:
    "Symbol signifying that no more anchor values exist in a pattern."


def match(cand: Any, pattern: Any) -> bool:
    """*”Primitive”* function that checks an individual value against
    another. Checking against ``Any`` works as a wildcard and will
    always result in ``True``.

    """
    cand = kind.cast_to_hashable(cand)
    pattern = kind.cast_to_hashable(pattern)

    accepted = {cand, Any}

    return True if pattern in accepted else False


peek_nv = lang.infinite_item(1, NoNextValue)  # type: ignore
peek_na = lang.infinite_item(1, NoNextAnchor)  # type: ignore


def move(left: Sequence, pattern: Sequence):
    # def move(left: Sequence, pattern: Sequence) -> Tuple[SeqOrMiss, SeqOrMiss]:
    """One step of the pattern matching process. The ``move()`` function
    will take to sequences (``left``, ``pattern``) that represents the
    current state of matching and produce a tuple representing the
    next (``left``, ``pattern``) pair of the pattern matching.

    :param left: Values that haven't been matched yet.

    :param pattern: Pattern values to match subsequently.

    :return: A pair representing the next step in the matching process.
    :rtype: Tuple[Sequence,Sequence]

    """
    VC, AC = len(left), len(pattern)

    lensum = VC + AC

    if VC == 0 or AC == 0:
        return Miss, Miss

    if pattern == (..., ):
        return (), ()

    if type(left) != type(pattern):
        return Miss, Miss

    V, A = left[0], pattern[0]

    if lensum == 2 and match(V, A):
        return (), ()
    elif lensum == 2 and not match(V, A):
        # abandon
        return Miss, Miss
    elif lensum > 2:
        if match(V, A):
            # advance
            return left[1:], pattern[1:]
        elif A is ...:
            NV, NA = peek_nv(left), peek_na(pattern)
            if match(NV, NA):
                # advance
                return left[1:], pattern[1:]
            else:
                # drag / advance
                if VC == 1:
                    # last element -> unload (drop ...)
                    # 0
                    return left, pattern[1:]
                elif VC > 1:
                    # several elements -> drag (drop one value, keep ...)
                    return left[1:], pattern

        else:
            # abandon
            return Miss, Miss


def matches(values: Sequence,
            patterns: Sequence) -> Union[Sequence, Type[Miss]]:
    """Tries to match ``values`` from ``patterns``.

    :param values: A sequence of values to match.
    :param patterns: A sequence of patterns that may match ``values``.

    :return: The pattern that was matched or ``Miss``.
    :rtype: Union[Sequence, Type[Miss]]

    """
    for pattern in box(patterns):
        # Operate on copies ->
        matched, pending = box(values)[:], box(pattern)[:]
        while matched or pending:
            # (-> comsumes the copies)
            matched, pending = move(matched, pending)
            if matched is Miss:
                break
        if matched is Miss:
            continue
        else:
            return pattern

    return Miss


def resolve_pattern(params: Any, opts: Any) -> TypePatternCand:
    safeboxed = box(unbox(params))
    return safeboxed if len(opts) == 0 else (*safeboxed, Mapping)


MatchArgT = TypeVar('MatchArgT')
MatchRetT = TypeVar('MatchRetT')


class Matcher(dict, Generic[MatchArgT, MatchRetT]):
    """Common base for all matcher classes.

    Since ``Matcher`` is also ``Generic``, you use it to subtype
    concrete instances of matchers you implement.

    """
    def signature(self, handler: Callable) -> Sequence:  # pragma: nocov
        ...

    def callsign(self, args: Sequence[MatchArgT],
                 kwargs: Mapping[Any, Any]) -> Sequence:  # pragma: nocov
        ...

    def _raise_on_conflict(self, dispatch):
        try:
            conflicting = self[dispatch]
            raise Conflict(f'Pattern {dispatch} had a previous conflict '
                           f'{dispatch}={conflicting}')
        except KeyError:
            pass

    def case(self, handler: Callable) -> Callable:
        dispatch = self.signature(handler)
        self._raise_on_conflict(dispatch)
        self[dispatch] = handler
        return handler

    def missed(self, handler: Callable) -> Callable:
        self[Miss] = handler
        return handler

    def match(self, args: Sequence, kwargs: Mapping) -> Callable:
        cand = self.callsign(args, kwargs)
        key = matches(cand, tuple(self))
        return self[key]

    def invoke(self, handler: Callable, args: Sequence, kwargs: Mapping):
        return handler() if lang.arity(handler) == 0 else handler(
            *box(unbox(args)), **kwargs)

    def __call__(self, *args: Any, **kwargs: Any) -> MatchRetT:
        try:
            return self.invoke(self.match(args, kwargs), args, kwargs)
        except KeyError:
            try:
                return self.invoke(self[Miss], args, kwargs)
            except KeyError:
                raise Mismatch

    def explain(self, out=False):  # pragma: nocov
        """Development convenience tool -

        creates a summary of what patterns matcher object contain
        and which functions the matchings map to.

        """
        lines = (f"- A {self.__class__.__name__}", )
        for matching in self:
            fn = self[matching]
            lines = (*lines, f"    - {matching!r} : {kind.nick(fn)}")

        text = os.linesep.join(lines)
        if out:
            print(text)
        else:
            return text


class TypeMatcher(Matcher):
    """Concrete implementation of a type matcher instance.

    If you want to type a type matcher, use standard technique when
    using ``Generic`` types:

    >>> from kingston.match import Matcher, TypeMatcher
    >>> my_int_matcher:Matcher[int, int] = TypeMatcher({
    ...    int: lambda x: x+1,
    ...    str: lambda x: 'str'})
    >>> my_int_matcher(10)
    11
    >>> my_int_matcher(20)
    21
    >>> my_int_matcher('foo')  # ok at runtime but fails mypy
    'str'
    >>>
    """
    def signature(self, handler: Callable) -> Sequence:
        return cast(Sequence, unbox(primparams(handler)))

    def callsign(self, args: Sequence[MatchArgT],
                 kwargs: Mapping[Any, Any]) -> Sequence:
        return cast(Sequence[Any], xrtype(resolve_pattern(args, kwargs)))


class ValueMatcher(Matcher):
    """Concrete implementation of a value matching instance.

    If you want to type a type matcher, use standard technique when
    using ``Generic`` types:

    >>> from kingston.match import ValueMatcher, Miss
    >>> my_val_matcher:Matcher[int, str] = ValueMatcher({
    ...    1: lambda x: 'one!',
    ...    2: lambda x: 'two!',
    ...    Miss: lambda x: 'many!'})
    >>> my_val_matcher(1)
    'one!'
    >>> my_val_matcher(2)
    'two!'
    >>> my_val_matcher(3)
    'many!'
    >>> my_val_matcher('x')  # ok at runtime but fails mypy (& missleading..)
    'many!'
    >>>
    """
    def callsign(self, args: Sequence[MatchArgT],
                 kwargs: Mapping[Any, Any]) -> Sequence:
        return cast(Sequence[Any], unbox(resolve_pattern(args, kwargs)))

    def case(self, *params: Any, **opts: Any) -> Callable:
        """Decorator to add a function. The types of the parameters. The types
        that will be matched is taken from the signature of the
        decorated function.

        """
        def wrap(handler, *xparams, **xopts):
            dispatch = unbox(params)
            self._raise_on_conflict(dispatch)
            self[dispatch] = handler
            return handler

        return wrap
