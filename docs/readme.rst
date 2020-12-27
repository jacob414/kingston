.. _readme:

Kingston README
===============

I use the excellent `Funcy <https://funcy.readthedocs.io/>`__ library
for Python a lot. This is my collection of extras that I have designed
to work closely together with funcy. Funcy Kingston (Reference, see
`here <https://youtu.be/U79o7qwul48>`__).

`Run on Repl.it <https://repl.it/@jacob414/kingston>`__

Kingston is auto-formatted using
`yapf <https://github.com/google/yapf>`__.

Pattern matching using extended ``dict``'s
------------------------------------------

``match.Match`` objects are callable objects using a ``dict`` semantic
that also matches calls based on the type of the calling parameters:

.. code:: python

   >>> from kingston import match
   >>> foo = match.TypeMatcher({
   ...     int: lambda x: x*100,
   ...     str: lambda x: f'Hello {x}'
   ... })
   >>> foo(10)
   1000
   >>> foo('bar')
   'Hello bar'
   >>>

.. code:: python

   >>> from kingston import match
   >>> foo = match.TypeMatcher({
   ...     int: lambda x: x * 100,
   ...     str: lambda x: f'Hello {x}',
   ...     (int, int): lambda a, b: a + b
   ... })
   >>> foo(10)
   1000
   >>> foo('bar')
   'Hello bar'
   >>>
   >>> foo(1, 2)
   3
   >>>

You can use ``typing.Any`` as a wildcard:

.. code:: python

   >>> from typing import Any
   >>> from kingston import match
   >>> foo = match.TypeMatcher({
   ...     int: lambda x: x * 100,
   ...     str: (lambda x: f"Hello {x}"),
   ...     (int, Any): (lambda num, x: num * x)
   ... })
   >>> foo(10)
   1000
   >>> foo('bar')
   'Hello bar'
   >>> foo(3, 'X')
   'XXX'
   >>> foo(10, 10)
   100
   >>>

You can also subclass type matchers and use a decorator to declare cases
as methods:

.. code:: python

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

Typing pattern matchers
~~~~~~~~~~~~~~~~~~~~~~~

``match.Match`` objects can be typed using Python's standard
`typing <https://docs.python.org/3/library/typing.html>`__ mechanism. It
is done using
`Generics <https://mypy.readthedocs.io/en/stable/generics.html>`__:

The two subtypes are *[argument type, return type]*.

.. code:: python

   >>> from kingston import match
   >>> foo:match.Matcher[int, int] = match.TypeMatcher({
   ...    int: lambda x: x+1,
   ...    str: lambda x: 'hello'})
   >>> foo(10)
   11
   >>> foo('bar')  # fails on mypy but would be ok at runtime
   'hello'
   >>>

Match by value(s)
~~~~~~~~~~~~~~~~~

``match.ValueMatcher`` will use the *values* of the parameters to do the
same as as ``match.Match``:

.. code:: python

   >>> from kingston import match
   >>> foo = match.ValueMatcher({'x': (lambda: 'An x!'), ('x', 'y'): (lambda x,y: 3*(x+y))})
   >>> foo('x')
   'An x!'
   >>> foo('x', 'y')
   'xyxyxy'
   >>>

Same as with the type matcher above, ``typing.Any`` works as a wildcard
with the value matcher as well:

.. code:: python

   >>> from kingston import match
   >>> from typing import Any
   >>> foo = match.ValueMatcher({
   ...     'x': lambda x: 'An X!',
   ...     ('y', Any): lambda x, y: 3 * (x + y)
   ... })
   >>> foo('x')
   'An X!'
   >>> foo('y', 'x')
   'yxyxyx'
   >>>

You can also declare cases as methods in a custom ``ValueMatcher``
subclass.

Use the function ``value_case()`` to declare value cases. **Note:**
*imported as a shorthand*:

.. code:: python

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
   >>>

Aspect Oriented Programming with terse syntax
---------------------------------------------

Kingston also implement a technique to do
`AOP <https://en.wikipedia.org/wiki/Aspect-oriented_programming>`__ with
an opinionated terse syntax that I like. It lives in the
``kingston.aop`` module.

It's used in two main ways:

With decorators
~~~~~~~~~~~~~~~

Define an ``=Aspects=`` object as an empty object:

.. code:: python

   >>> from kingston.aop import Aspects
   >>> when = Aspects()
   >>>

Then declare your aspects using the object as a decorator:

.. code:: python

   >>> @when(lambda x: x == 1, y=lambda y: y == 1)
   ... def labbo(x, y=1):
   ...     return 11
   >>> @when(lambda x: x == 1, z=lambda z: z == 2)
   ... def labbo(x, z=2):
   ...     return 12
   >>>

Aspect 1 above will be triggered if you call it with positional
parameter 0 as ``1`` and a keyword parameter ``y=1``:

.. code:: python

   >>> labbo(1, y=1)
   11
   >>>

Aspect 2 is triggered by parameters ``1, z=2``:

.. code:: python

   >>> labbo(1, z=2)
   12
   >>>

Any other combination of parameters will raise a ``AspectNotFound``
exception:

.. code:: python

   >>> labbo(123) # doctest: +IGNORE_EXCEPTION_DETAIL
   Traceback (most recent call last):
   AspectNotFound
   >>>
   >>>

With a mapping of aspects
~~~~~~~~~~~~~~~~~~~~~~~~~

You might find this better if you want brievity and/or point free style.

.. code:: python

   >>> given = Aspects({
   ...     (lambda x: x == 1,): lambda x: 1,
   ...     (lambda x: x > 1,): lambda x: x * x
   ... })
   >>>

Calls work the same as above:

.. code:: python

   >>> given(1)
   1
   >>> given(2)
   4
   >>> given(0) # doctest: +IGNORE_EXCEPTION_DETAIL
   Traceback (most recent call last):
   AspectNotFound
   >>>

Nice things
-----------

dig()
~~~~~

Deep value grabbing from almost any object. Somewhat inspired by CSS
selectors, but not very complete. This part of the API is unstable — it
will (hopefully) be developed further in the future.

.. code:: python

   >>> from kingston import dig
   >>> dig.xget((1, 2, 3), 1)
   2
   >>> dig.xget({'foo': 'bar'}, 'foo')
   'bar'
   >>> dig.dig({'foo': 1, 'bar': [1,2,3]}, 'bar.1')
   2
   >>> dig.dig({'foo': 1, 'bar': [1,{'baz':'jox'},3]}, 'bar.1.baz')
   'jox'
   >>>

The difference between ``dig.dig()`` and ``funcy.get_in()`` is that you
can use shell-like blob patterns to get several values keyed by similar
names:

.. code:: python

   >>> from kingston import dig
   >>> res = dig.dig({'foo': 1, 'foop': 2}, 'f*')
   >>> res
   [foo=1:int, foop=2:int]
   >>> # (textual representation of an indexable object)
   >>> res[0]
   foo=1:int
   >>> res[1]
   foop=2:int
   >>>

Testing tools
-------------

Kingston has some testing tools as well. Also, due to Kingston's
opinionated nature, they are only targeted towards
`pytest <https://pytest.org>`__.

Shortform for pytest.mark.parametrize
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

I tend to use pytest.mark.parametrize in the same form everywhere. Thus
I have implemented this short-form:

.. code:: python

   >>> from kingston.testing import fixture
   >>> @fixture.params(
   ...     "a, b",
   ...     (1, 1),
   ...     (2, 2),
   ... )
   ... def test_dummy_compare(a, b):
   ...     assert a == b
   >>>

Doctests as fixtures
~~~~~~~~~~~~~~~~~~~~

There is a test decorator that generates pytest fixtures from a function
or an object. Use it like this:

.. code:: python

   >>> def my_doctested_func():
   ...   """
   ...   >>> 1 + 1
   ...   2
   ...   >>> mystring = 'abc'
   ...   >>> mystring
   ...   'abc'
   ...   """
   ...   pass
   >>> from kingston.testing import fixture
   >>> @fixture.doctest(my_doctested_func)
   ... def test_doctest_my_doctested(doctest):  # fixture name always 'doctest'
   ...     res = doctest()
   ...     assert res == '', res
   >>>

