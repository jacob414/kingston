# yapf

import sys
import io
from typing import Any, Tuple, List, Callable, Optional
import pdb
import traceback

import distutils.cmd

import funcy  # type: ignore
import pytest  # type: ignore

from altered import state  # type: ignore

import pycodestyle  # type: ignore
import mypy.api  # type: ignore

from flake8.api import legacy as flake8  # type: ignore


class fixture(object):
    @staticmethod
    def params(namelist: str, *values: Any) -> Any:
        "Does params"
        return pytest.mark.parametrize(namelist, values)


class ReviewProject(distutils.cmd.Command):  # pragma: nocov
    user_options: List[str] = []

    def initialize_options(self: 'ReviewProject') -> None:
        pass

    def finalize_options(self: 'ReviewProject') -> None:
        pass

    @staticmethod
    def lint() -> Tuple[int, str, str]:
        print('     flake8...')
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

        issues = sum(funcy.walk_values(lambda x: x[0], reports).values())
        if issues > 0:
            ReviewProject.separator_line()
            print()
            print(f'{issues} issues found.')


def hook_uncatched(pm_func: Optional[Callable] = None
                   ) -> None:  # pragma: nocov
    """Installs an exception hook that triggers a debugger post-mortem on
    unhandled exceptions.

    """

    if pm_func is None:
        pm_func = pdb.post_mortem

    def unhandled(type_: Any, value: Any, tb: Any) -> None:
        """Catches unhandled exceptions, print stack trace and executes
        debugger post-mortem entry point.

        """
        traceback.print_exception(type_, value, tb)
        print()  # lf
        pm_func(tb)

    sys.excepthook = unhandled
    return unhandled
