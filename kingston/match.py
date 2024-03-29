# yapf
"""
The Match module
~~~~~~~~~~~~~~~~

This module implements a technique for pattern matching.


IDEA: Statement-oriented matcher within the same scope:
with ValueMatcher('sum', 1, 2, 3) as m:
    with m.case('sum', Any, Any, Any) as _, one, two, three:
        print(one + two + three)
    with m.case('avg', ...) as _, *values:
        print(sum(*values))
    with.m.miss() as *missed:
        print('MISS!')
"""

import os

from typing import (Any, Type, Iterable, Tuple, Mapping, Callable, Union, Set,
                    List, Dict, Collection, Sequence, TypeVar, Generic, cast)

import funcy as fy  # type: ignore[import]

from . import lang
from . import decl
from .decl import box, unbox, Singular
from . import xxx_kind as kind
from .xxx_kind import funcnick  # type: ignore[attr-defined]
from .xxx_kind import primparams  # type: ignore[attr-defined]
from .xxx_kind import xrtype  # type: ignore[attr-defined]

SingularTypeCand = Type[Any]
ComplexTypeCand = Iterable[SingularTypeCand]
TypePatternCand = Union[Singular, ComplexTypeCand]
PatternCand = Union[decl.Singular, Iterable[decl.Singular]]
FoundPattern = Union[PatternCand, object, Collection[decl.Singular]]
MatchFunc = Callable[[Any, Any], bool]
Plural = Union[Set[Any], List[Any], Tuple[Any, ...], Dict[Any, Any]]
Dualism = Union[Singular, Plural]


class Conflict(TypeError):
    """Exception raised if a pattern to be matched already have been
    applied to a `Matcher` instance.

    """


class Mismatch(ValueError):
    "Exception to signal matching error in Matcher objects."


class Miss_:
    "Symbol for a missed match."


Miss = (Miss_, )  # Miss constant, a marker for missed matches


class NoNextValue:
    "Symbol signifying that no more values are available to pattern check for."


class NoNextAnchor:
    "Symbol signifying that no more anchor values exist in a pattern."


def match(cand: Any, pattern: Any) -> bool:
    """*”Primitive”* function that checks an individual value against
    another. The ``match()`` function is *only* responsible for
    checking two values, matching markers `Any` and `Ellipsis` are
    handled elsewhere.

    """
    cand, pattern = kind.cast_to_hashable(cand), kind.cast_to_hashable(pattern)
    return cand == pattern


def match_subtype(cand: Any, pattern: Any) -> bool:
    if fy.is_seqcoll(cand):
        return issubclass(type(cand), pattern)

    else:
        return issubclass(cand, pattern)


peek1 = lang.itempadded(1, NoNextValue)  # type: ignore[attr-defined]


def move(matched: Sequence,
         pending: Sequence,
         matchfn: Callable = match) -> Tuple[Sequence, Sequence]:

    if type(matched) != type(pending):
        return Miss, Miss

    n_matched, n_pending = len(matched), len(pending)

    if 0 in {n_matched, n_pending}:
        return Miss, Miss

    value, against = matched[0], pending[0]
    if against is Any:
        # forward
        return matched[1:], pending[1:]
    elif against is ... and n_matched > 1:
        anchor = peek1(pending)
        if anchor is not NoNextValue and matchfn(matched[1], anchor):
            # drag/unload
            return matched[min(n_matched, 2):], pending[min(n_pending, 2):]
        else:
            # drag
            return matched[1:], pending
    elif pending == (..., ):
        return (), ()
    elif against is ...:
        return Miss, Miss
    elif matchfn(value, against):
        # forward
        return matched[1:], pending[1:]  # attempt 1
    else:
        return Miss, Miss


def matches(values: Sequence,
            patterns: Sequence,
            matchfn: Callable = match) -> Sequence:
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
            matched, pending = move(matched, pending, matchfn)
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

DecoratorCases = Tuple[Callable[..., Any], Sequence[Any]]


class Matcher(dict, Generic[MatchArgT, MatchRetT]):
    """Common base for all matcher classes.

    Since ``Matcher`` is also ``Generic``, you use it to subtype
    concrete instances of matchers you implement.

    """
    __case__: DecoratorCases

    @staticmethod
    def signature(
        handler: Callable
    ) -> Tuple[Callable[..., Any], Sequence[Any]]:  # pragma: nocov
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
        for cb, deco_case in ((getattr(self, name), getattr(self,
                                                            name).__case__)
                              for name in dir(self)
                              if hasattr(getattr(self, name), '__case__')):
            self[deco_case] = cb

        try:
            handler = self.match(args, kwargs)
            return self.invoke(handler, args, kwargs)
        except KeyError:
            try:
                return self.invoke(self[Miss], args, kwargs)
            except KeyError:
                raise Mismatch(f"Mismatched ({args!r}, {kwargs!r})")

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

    def responserep(self, rep: Union[Type, Sequence[Type]],
                    nickfunc: Callable) -> str:
        if fy.is_seqcoll(rep):
            return ','.join(map(nickfunc, cast(Sequence, rep)))
        else:
            return nickfunc(rep)

    def descresponses(self, nickfunc: Callable) -> str:
        return ', '.join(
            f"({self.responserep(key, nickfunc)})->{funcnick(resp)}"
            for key, resp in self.items())


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

    It will try to give a reasonably human representation when
    inspected:

    >>> my_int_matcher
    <TypeMatcher: (int)->λ, (str)->λ >
    >>>

    You can also subclass type matchers and use a decorator to declare
    cases as methods:

    >>> from kingston.match import Matcher, TypeMatcher, case
    >>> from numbers import Number
    >>> class NumberDescriber(TypeMatcher):
    ...    @case
    ...    def describe_one_int(self, one:int) -> str:
    ...        return "One integer"
    ...
    ...    @case
    ...    def describe_two_ints(self, one:int, two:int) -> str:
    ...        return "Two integers"
    ...
    ...    @case
    ...    def describe_one_float(self, one:float) -> str:
    ...        return "One float"
    >>> my_num_matcher:Matcher[Number, str] = NumberDescriber()
    >>> my_num_matcher(1)
    'One integer'
    >>> my_num_matcher(1, 2)
    'Two integers'
    >>> my_num_matcher(1.0)
    'One float'
    >>>

    """
    @staticmethod
    def signature(
            handler: Callable) -> Tuple[Callable[..., Any], Sequence[Any]]:
        return cast(Tuple[Callable[..., Any], Sequence[Any]],
                    unbox(primparams(handler)))

    def match(self, args: Sequence, kwargs: Mapping) -> Callable:
        try:
            return super(TypeMatcher, self).match(args, kwargs)
        except KeyError:
            cand = self.callsign(args, kwargs)
            key = matches(cand, tuple(self), match_subtype)
            return self[key]

    def callsign(self, args: Sequence[MatchArgT],
                 kwargs: Mapping[Any, Any]) -> Sequence:
        return cast(Sequence[Any], xrtype(resolve_pattern(args, kwargs)))

    def __repr__(self) -> str:
        nickfunc = kind.typenick  # type: ignore[attr-defined]
        matchreps = self.descresponses(nickfunc)
        return f"<TypeMatcher: {matchreps} >"


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

    It will try to give a reasonably human representation when
    inspected:

    >>> my_val_matcher
    <ValueMatcher: (1)->λ, (2)->λ, (<class 'kingston.match.Miss_'>)->λ >
    >>>

    You can also declare cases as methods in a custom ``ValueMatcher``
    subclass.

    Use the function ``value_case()`` to declare value
    cases. **Note:** *imported as a shorthand*:

    >>> from kingston.match import Matcher, ValueMatcher
    >>> from kingston.match import value_case as case
    >>> class SimplestEval(ValueMatcher):
    ...     @case(Any, '+', Any)
    ...     def _add(self, a, op, b) -> int:
    ...         return a + b
    ...
    ...     @case(Any, '-', Any)
    ...     def _sub(self, a, op, b) -> int:
    ...         return a - b
    >>> simpl_eval = SimplestEval()
    >>> simpl_eval(1, '+', 2)
    3
    >>> simpl_eval(10, '-', 5)
    5

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

    def __repr__(self) -> str:
        matchreps = self.descresponses(str)
        return f"<ValueMatcher: {matchreps} >"


def type_case(func: TypeMatcher) -> Callable:
    func.__case__ = cast(DecoratorCases, TypeMatcher.signature(func)[1:])
    return func


# Note: Guess based on what I personally use most.
case = type_case


def value_case(*values: Any) -> Callable:
    def wrap(func: ValueMatcher):
        func.__case__ = cast(DecoratorCases, values)
        return func

    return wrap
