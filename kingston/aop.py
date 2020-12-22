# yapf
"""Terse Aspect Oriented Programming
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module implements a technique for Aspect Oriented Programming
that tries to keeps the code as terse as possible.

It works in two modes:

  - Decorator syntax: instantiate an ``Aspects`` object and use it as
    a decorator to declare rules that will invoke an aspect.

  - Pass a ``dict`` to the constructor of an ``Aspect`` with rules
    defined as a tuple of checking functions and the handler function
    as a value.

For examples, see the definition of ``Aspects``.
"""

from typing import Any, Callable, Collection, Mapping, Optional
import funcy as fy  # type: ignore[import]

from kingston.decl import box


class AspectNotFound(Exception):
    "Raised if no aspect can be found covering a call."


def raise_for(params: Collection, opts: Mapping) -> None:
    raise AspectNotFound(f"No aspect covers {(params, opts)}")


class Aspects(dict):
    """Aspect Oriented Programming as a dict subclass / using decorators.
    Declare aspects using decorators
    --------------------------------

    Define an ``Aspect`` object as empty::

    >>> when = Aspects()

    Then declare aspects using decorators::

    >>> @when(lambda x: x == 1, y=lambda y: y == 1)
    ... def labbo(x, y=1):
    ...     return 11
    >>> @when(lambda x: x == 1, z=lambda z: z == 2)
    ... def labbo(x, z=2):
    ...     return 12

    Aspect 1 above will be triggered if you call it with positional
    parameter 0 as ``1``and a keyword parameter ``y=1``::

    >>> labbo(1, y=1)
    11

    Aspect 2 is triggered by parameters ``1, z=2``::

    >>> labbo(1, z=2)
    12

    Any other combination of parameters will raise a
    ``AspectNotFound`` exception::

    >>> labbo(123) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    AspectNotFound
    >>>

    Declare aspects directly as keys in a mapping
    ---------------------------------------------

    You might find this better if you want brievity and/or point free
    style.

    >>> given = Aspects({
    ...     (lambda x: x == 1,): lambda x: 1,
    ...     (lambda x: x > 1,): lambda x: x * x
    ... })

    Calls work the same as above::

    >>> given(1)
    1
    >>> given(2)
    4
    >>> given(0) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    AspectNotFound
    >>>
    """
    def checkpoint(point: Collection, params: Collection,
                   opts: Mapping) -> Optional[Collection]:
        try:
            positional, keyworded = point

            p_ok = all(chk(p) for chk, p in zip(positional, params))
            if keyworded and opts:
                kw_ok = all(chk[1](p)
                            for chk, p in zip(box(keyworded), opts.values()))
            else:
                kw_ok = True
        except ValueError:
            p_ok = all(chk(p) for chk, p in zip(point, params))
            kw_ok = True
        if p_ok and kw_ok:
            return point
        else:
            return None

    def search(self, params: Collection, opts: Mapping):
        try:
            check = fy.rpartial(Aspects.checkpoint, params, opts)
            return self[next(filter(check, self.keys()))]
        except StopIteration:
            raise_for(params, opts)

    def invoke(self, *params: Any, **opts: Any) -> Any:
        return self.search(params, opts)(*params, **opts)

    def decorate(self, params: Collection, opts: Mapping):
        def wrap(decorated: Callable) -> Callable:
            self[params, tuple(opts.items())] = decorated
            return self.invoke

        return wrap

    def __call__(self, *params, **opts) -> Callable:

        if all(map(callable, fy.merge(params, opts.values()))):
            return self.decorate(params, opts)

        else:
            return self.search(params, opts)(*params, **opts)
