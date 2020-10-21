.. _ormsnackis:

Tiny AST to code generation thingy
==================================

A key feature of Kingston is the pattern matching in kingston.match.

To get an idea of what you can build, let's create a rudimentary AST
to Python code generator. This tends to be a quite daunting exercise.

Imports needed
--------------

You will want to import ``ast``, ``kingston.match.Matcher`` and
``kingston.match.TypeMatcher``:

.. code:: python

   >>> import ast
   >>> from kingston.match import Matcher, TypeMatcher

Configure a ``Matcher`` to convert `ast.AST` nodes to strings
-------------------------------------------------------------

.. code:: python

    >>> nodeRep:Matcher[ast.AST, str] = TypeMatcher({
    ...     ast.Interactive: lambda: '',
    ...     ast.FunctionDef: lambda node: f"def {node.name}(",
    ...     ast.arguments: (lambda node: ','.join(arg.arg
    ...                                          for arg in node.args) +
    ...                     '):\n'),
    ...     ast.BinOp: lambda node: '',
    ...     ast.Constant: lambda node: str(node.value),
    ...     ast.Return: lambda node: '    return ',
    ...     ast.Add: lambda: ' + ',
    ... })


As you can see, this isn't recursive and will be very primitive. We
will borrow ``ast.walk()`` for brevity. Note the typing declaration at
the top line. This is to be able to use MyPy to type check our
matchings. Here the declaration means that the matcher accepts
``ast.AST`` nodes as parameters and will return ``str``.

Compile a small AST
-------------------

.. code:: python

   >>> topnode = compile("""
   ... def helo():
   ...     return 1 + 1
   ... """, 'examples.ormsnackis', 'single', ast.PyCF_ONLY_AST)

Given the ``Matcher`` we just created we could only support the most
minimal AST.

Test it
-------

We use the linear list of nodes you get from AST's `walk`_ function to
test without too much work:

.. _walk: https://docs.python.org/3/library/ast.html#ast.walk

.. code:: python

    >>> def test(tree):
    ...     print(''.join(nodeRep(node) for node in ast.walk(tree)))

    >>> if __name__ == '__main__':
    ...     test(topnode)

Running gives the following output:

.. code:: shell

   $ python examples/ormsnackis.py
   def helo():
       return 1 + 1
   $
