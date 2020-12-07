.. _changelog:

Kingston Changelog
==================

.. _section-1:

0.7.4
-----

-  Implements subtype matching in match.TypeMatcher
-  More options for devtool.PrintfDebugging
-  Tiny style fixes

.. _section-2:

0.7.3
-----

-  More readable error messages in case of ``Mismatch`` exception from
   matchers.
-  Implemented new notation for matchers as subclasses where cases are
   declared using a decorator.

.. _section-3:

0.7.2
-----

-  Fix version, incorrect imports in ``kingston.testing`` could cause
   false positives in CI settings.

.. _section-4:

0.7.1
-----

-  Fix version, invalid metadata in ``setup.py``

.. _section-5:

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

.. _section-6:

0.6.8
-----

-  Fixes for ``kingston.match``
-  ``kingston.testing.trial()`` / ``kingston.testing.retryit()``, moved
   to ``kingston.devtool``.

.. _section-7:

0.6.7
-----

-  Bugfix in ``kingston.match.Match.case()``

.. _section-8:

0.6.6
-----

-  Polish release, mosly QA work
-  Smaller bugfixes
-  Coverage analysis with
   `pytest-cov <https://pytest-cov.readthedocs.io/en/latest/>`__
-  Trimmed code base after coverage analysis

.. _section-9:

0.6.5
-----

-  New module ``kingston.match``, a mechanism for *”pattern matching”*
   using subclasses of ``dict``'s to store patterns and references to
   ``callable``'s.

.. _section-10:

0.6.4
-----

-  Built a more formal project structure.
-  Started to use light-weight CI in the form of a GitHub action
   invoking `Tox <https://tox.readthedocs.io/en/latest/>`__.

.. _section-11:

0.6.3
-----

-  Project renamed to *”Kingston”* and re-licenced under LGPL v3
