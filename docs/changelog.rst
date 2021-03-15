.. _changelog:

Kingston Changelog
==================

.. _section-1:

0.7.8
-----

-  Slight refactor / yak shave & fix version
-  Redesigns kingston.match.matches() to ensure that marker values
   \`Any\` and \`…\` are never sent to the comparision function. Fixes
   seldom triggered edge-case eg when you want to feed values straight
   to the \`re\` module.
-  Implements sensible \`str()\` and \`repr()\` handlers for
   \`kingston.match.Matcher\` objects.
-  Shaves off 1 iteration when matching against \`…\` marker values.
-  A few internal naming improvements.
-  Filled in missing typing stub for \`kingston.aop\`

.. _section-2:

0.7.7
-----

-  Fix version, fixes an edge case when type matching against sequences
   with exactly 1 value.

.. _section-3:

0.7.6
-----

-  Require that recursive ``match.TypeMatcher``'s are declared
   explicitly case by case.

.. _section-4:

0.7.5
-----

-  Implements a mechanism for AOP with terse syntax
-  Small internal refinements

.. _section-5:

0.7.4
-----

-  Implements subtype matching in match.TypeMatcher
-  More options for devtool.PrintfDebugging
-  Tiny style fixes

.. _section-6:

0.7.3
-----

-  More readable error messages in case of ``Mismatch`` exception from
   matchers.
-  Implemented new notation for matchers as subclasses where cases are
   declared using a decorator.

.. _section-7:

0.7.2
-----

-  Fix version, incorrect imports in ``kingston.testing`` could cause
   false positives in CI settings.

.. _section-8:

0.7.1
-----

-  Fix version, invalid metadata in ``setup.py``

.. _section-9:

0.7.0
-----

-  The module ``kingston.match`` can now do a wildcard match using
   ``...`` (``Ellipsis``) objects, i.e. an arbitrary long group of
   ``Any`` matchings.
-  Many more refactoring and fixes in ``kingston.match``
-  Testing utility ``kingston.testing.fixture`` and extract and run
   doctests as `pytest
   fixtures <https://docs.pytest.org/en/stable/fixture.html>`__.
-  Dropped the homegrown pipe operator overloading mechanism, use
   `SSPipe <https://sspipe.github.io/>`__ instead.
-  Can build as a `Conda
   Package <https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/packages.html>`__.
-  Dropped obsolete dependencies, e.g. ``pysistence``.
-  More extensive usage of `MyPy <https://mypy.readthedocs.io/>`__
   gradual typing mechanism.

.. _section-10:

0.6.8
-----

-  Fixes for ``kingston.match``
-  ``kingston.testing.trial()`` / ``kingston.testing.retryit()``, moved
   to ``kingston.devtool``.

.. _section-11:

0.6.7
-----

-  Bugfix in ``kingston.match.Match.case()``

.. _section-12:

0.6.6
-----

-  Polish release, mosly QA work
-  Smaller bugfixes
-  Coverage analysis with
   `pytest-cov <https://pytest-cov.readthedocs.io/en/latest/>`__
-  Trimmed code base after coverage analysis

.. _section-13:

0.6.5
-----

-  New module ``kingston.match``, a mechanism for *”pattern matching”*
   using subclasses of ``dict``'s to store patterns and references to
   ``callable``'s.

.. _section-14:

0.6.4
-----

-  Built a more formal project structure.
-  Started to use light-weight CI in the form of a GitHub action
   invoking `Tox <https://tox.readthedocs.io/en/latest/>`__.

.. _section-15:

0.6.3
-----

-  Project renamed to *”Kingston”* and re-licenced under LGPL v3
