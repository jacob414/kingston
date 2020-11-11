# yapf

import os
import sys
import io
from typing import (Any, Tuple, List, Dict, Callable, Optional, Iterable,
                    Mapping, Optional, Generator, cast)
import pdb
import traceback
import contextlib
import doctest as dt
import re
import ast

import distutils.cmd

import funcy as fy  # type: ignore
import pytest  # type: ignore

from _pytest import mark
ParameterSet = mark.structures.ParameterSet

from altered import state, E  # type: ignore

from hypothesis import strategies as st

from .decl import box, unbox, Singular
from .decl import Plural  # type: ignore
from .dig import dig

between = lambda from_, to_: st.integers(min_value=from_, max_value=to_)
ints = st.integers()
diff_ints = lambda n: st.lists(
    between(0, n), min_size=n, max_size=n, unique=True)
int_or_none = st.one_of(st.none(), st.integers())
idx = lambda max_: st.integers(min_value=0, max_value=max_)

# Simplified mirroring paramtrically lax ident, for testing convenience
same = lambda *args, **kwargs: args[0] if len(args) == 1 else args


class fixture:
    @staticmethod
    def params(namelist: str, *values: Any) -> Any:
        "Does params"
        return pytest.mark.parametrize(namelist, values)

    class DocTestFixture:
        "Class for `.doctest` embedded namespace."

        def __init__(self):
            self.ns = {}

        def __call__(self, func: Callable):
            mod = sys.modules[func.__module__]

            examples = fy.select(
                fy.isa(dt.Example),
                dt.DocTestParser().parse(str(func.__doc__), func.__name__))

            def scenario(atest):
                def outcome():
                    runner, out = dt.DocTestRunner(), io.StringIO()
                    atest.globs.update(self.ns)
                    res = runner.run(atest, out=out.write, clear_globs=False)
                    self.ns.update(atest.globs)
                    if res.failed == 0:
                        return ''
                    else:  # pragma: nocov
                        return os.linesep.join(out.getvalue().split(
                            os.linesep)[1:])

                return outcome

            def maybe_lineof(obj):
                code = getattr(obj, '__code__', False)
                if code:
                    return code.co_firstlineno
                else:
                    return -1

            def collect():
                self.ns.update(mod.__dict__)
                for example in examples:
                    atest = dt.DocTest([example], self.ns, mod.__name__,
                                       mod.__file__, maybe_lineof(func),
                                       str(func.__doc__))
                    yield scenario(atest)

            return pytest.mark.parametrize("doctest", collect())

    doctest: DocTestFixture


fixture.doctest = fixture.DocTestFixture()


class ReviewProject(distutils.cmd.Command):  # pragma: nocov
    user_options: List[str] = []

    def initialize_options(self: 'ReviewProject') -> None:
        pass

    def finalize_options(self: 'ReviewProject') -> None:
        pass

    @staticmethod
    def lint() -> Tuple[int, str, str]:
        print('     flake8...')
        from flake8.api import legacy as flake8  # type: ignore
        out, err = io.StringIO(), io.StringIO()
        guide = flake8.get_style_guide()
        with state(sys, stdout=out, stderr=err):
            report = guide.check_files('.')
        return (report.total_errors, out.getvalue(), err.getvalue())

    @staticmethod
    def style() -> Tuple[int, str, str]:
        """Runs pycodestyle, unpleasantly white-boxy call.  ..but it doesn't
         seem to be written for integration, so:

        """
        import pycodestyle  # type: ignore

        print('     pycodestyle...')
        code = 0
        warn, err = io.StringIO(), io.StringIO()
        with state(sys, argv=[], stdout=warn, stderr=err):
            try:
                pycodestyle._main()
            except SystemExit as exc:
                code = exc.code
        return code, warn.getvalue(), err.getvalue()

    @staticmethod
    def types() -> Tuple[int, str, str]:
        "Runs MyPy, the standard Python type checker."
        import mypy.api  # type: ignore
        print('     MyPy...')
        warn, err, code = mypy.api.run(['.'])
        return code, warn, err

    @staticmethod
    def separator_line() -> None:
        "Prints a separating line of 79 characters wide."
        print()
        print(79 * '-')

    def run(self: 'ReviewProject') -> None:
        "Runs the setup task `'review'`."
        reports = {
            'flake8': ReviewProject.lint(),
            'pycodestyle': ReviewProject.style(),
            'mypy': ReviewProject.types(),
        }

        for tool in reports:
            code, warn, err = reports[tool]
            if code != 0:
                ReviewProject.separator_line()
                print(f'{tool}: code {code}')
                print('WARN')
                print(warn)
                print('ERROR')
                print(err)

        issues = sum(fy.walk_values(lambda x: x[0], reports).values())
        if issues > 0:
            ReviewProject.separator_line()
            print()
            print(f'{issues} issues found.')


def hook_uncatched(
        pm_func: Optional[Callable] = None) -> None:  # pragma: nocov
    """Installs an exception hook that triggers a debugger post-mortem on
    unhandled exceptions.

    """
    def unhandled(type_: Any, value: Any, tb: Any) -> None:
        """Catches unhandled exceptions, print stack trace and executes
        debugger post-mortem entry point.

        """
        traceback.print_exception(type_, value, tb)
        print()  # lf

        if pm_func is None:
            pm_func = pdb.post_mortem

        pm_func(tb)

    sys.excepthook = unhandled
