# yapf

from pprint import pformat
import json
import jsonpickle  # type: ignore
import os
import funcy

from typing import Any


def expose(x: Any, shrink_right: int = 1) -> str:
    """Abuses modules `json` and `jsonpickle` to expose internals of
    (almost) any object.

    """
    return json.loads(jsonpickle.dumps(x))


def look(x: Any, shrink_right: int = 1) -> None:
    """Dumps any object to stdout using the technique in `expose()`.

    The parameter `shrink_right` is used to set narrowing of
    indentation. (Use `0` to turn off).

    """
    print(pformat(expose(x, shrink_right)).replace('    ', shrink_right * ' '))


def guessdesc(value: Any) -> str:
    "Guesstimate a plausible description of a value."
    denoms = funcy.compact([
        getattr(value, 'name', ''),
        getattr(value, 'desc', ''),
        getattr(value, 'id', '')
    ])
    named = denoms[0] if len(denoms) == 1 else ''
    spec = value.__class__.__name__
    if named:
        desc = f'{named}:{spec}'
        return desc
    else:
        desc = f'{value!r}:{spec}'
        return desc


def genabneuyaml(cursor: Any, ident=0, name=None, maxrecur=100,
                 spacing='  ') -> None:
    "Generate lines of 'AbneuYAML' (see `abneuyaml()` below)."
    spaces = spacing * ident
    before = spaces
    desc = guessdesc(cursor)
    if name:
        desc = f"{name}={desc}"
    yield before, desc
    if ident > maxrecur:
        print(f"abneuyaml: high recursion ({maxrecur}) reached, "
              "circular structure? at {desc}")
    if hasattr(cursor, '__dict__'):
        ident = ident + 1
        for attr, value in cursor.__dict__.items():
            for before, desc in genabneuyaml(value,
                                             ident=ident,
                                             name=attr,
                                             maxrecur=maxrecur):
                yield before, desc


def abneuyaml(cursor: Any, ident=0, name=None, maxrecur=100) -> None:
    """Encode any object in a format that is 'almost, but not entirely
    unlike YAML'

    """
    return os.linesep.join(
        [''.join(enc) for enc in genabneuyaml(cursor, maxrecur=maxrecur)])
