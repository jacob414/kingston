import distutils.cmd
from contextlib import contextmanager as contextmanager
from typing import Any, Callable, List, Optional, Tuple

class fixture:
    @staticmethod
    def params(namelist: str, *values: Any) -> Any: ...

class ReviewProject(distutils.cmd.Command):
    user_options: List[str] = ...
    def initialize_options(self) -> None: ...
    def finalize_options(self) -> None: ...
    @staticmethod
    def lint() -> Tuple[int, str, str]: ...
    @staticmethod
    def style() -> Tuple[int, str, str]: ...
    @staticmethod
    def types() -> Tuple[int, str, str]: ...
    @staticmethod
    def separator_line() -> None: ...
    def run(self) -> None: ...

def hook_uncatched(pm_func: Optional[Callable]=...) -> None: ...