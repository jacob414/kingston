"""
A stupid but hopefully thought-provoking expression "DSL"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example of a stupid but hopefully thought-provoking expression
builder/evaluator.
"""

from kingston.match import Matcher, TypeMatcher, ValueMatcher
from typing import Any

stupid:Matcher[Any, int] = TypeMatcher({
        int: lambda x: x,
        str: lambda x: 99999,
        (Any, str, Any): ValueMatcher({
            (Any, '+', Any): lambda a, op, b: a + b,
            (Any, '-', Any): lambda a, op, b: a - b,
            (Any, '*', Any): lambda a, op, b: a * b,
            (Any, '/', Any): lambda a, op, b: a / b,
        }),
        (int, int, ...): lambda begin, end, *seq: seq[begin:end],
        (int, ...): lambda n, *seq: seq[0:n]
        # (Callable, ...): ... # Dr McCarthy, I presume? ;-) -- not supported (yet?)
    })

if __name__ == '__main__':
    print(f"Single int -> just an identity op: {stupid(1)}")
    print(f"A string -> just an arbitrary recognizable value: {stupid('hello')}")
    print(f"Addition: stupid(1, '+', 1) == {stupid(1, '+', 1)}")
    print(f"Subtraction: stupid(2, '-', 1) == {stupid(2, '-', 1)}")
    print(f"Multiplication: stupid(2, '*', 2) == {stupid(2, '*', 2)}")
    print(f"Division: stupid(2, '-', 1) == {stupid(2, '-', 1)}")
    print(f"Cute slice thingy, stupid(2,4,1,2,3,4,5) == {stupid(2,4,1,2,3,4,5)}")
