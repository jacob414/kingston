# yapf

from typing import Any, Callable, Union, Collection

from collections.abc import Iterable

import funcy
from funcy import flow


class PipingExperiment(object):
    """An experiment pushing the pipe concept a bit longer. Not sure where
    I'm going with this but curious.

    """
    def __init__(self, seed):
        # type: (Any) -> PipingExperiment
        self.result = seed

    def __or__(self, step):
        # type: (Callable) -> PipingExperiment
        self.result = step(self.result)
        return self


P = PipingExperiment

IT = type(int)
itrt = Iterable

NarrowingPredicate = Union[Any, Callable[[Any], bool]]


class Narrowable(object):
    def narrow(self, pred):
        # type: (NarrowingPredicate) -> Narrowable

        if callable(pred):
            # Narrow by a callabale predicate
            pred_ = flow.ignore(Exception, False)(pred)
            return narrowable(self.base([el for el in self if pred_(el)]))

        else:
            # Narrow by exact Match
            return narrowable(self.base([el for el in self if pred == el]))

    def __getitem__(self, idx):
        # type: (Any) -> Any
        "Finds individual node in itself or searches.."
        try:
            return self.__class__(self.base.__getitem__(self, idx))
        except AttributeError:
            return self.narrow(idx)
        except TypeError:
            return self.narrow(idx)
        except KeyError:
            return self.narrow(idx)
        except IndexError:
            return self.narrow(idx)


def narrowable(src):
    # type: (Union[Any, Collection]) -> Narrowable
    "Creates the base class an initializes a Narrowable collection."

    class Narrower(Narrowable, src.__class__):
        base = src.__class__

    return Narrower(src)
