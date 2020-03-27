# yapf

from functools import wraps, partial

from inspect import ismethod
from typing import Callable


class FSM(object):
    def __init__(self, initial):
        self.state = initial

    def methods(self):
        attr = partial(getattr, self)
        return (attr(n) for n in dir(self) if ismethod(attr(n)))

    def transition(self, state, *args, **kwargs):
        desc = f"{self.state}->{state}"

        def istransit(m: Callable) -> bool:
            return getattr(m, 'transits', '') == desc

        return (r for r in (transit for transit in (m(state, *args, **kwargs)
                                                    for m in self.methods()
                                                    if istransit(m))))


def state(name):
    def state_decorator(method):
        method.state = name

        @wraps(method)
        def event_handler(machine, *_, **__):
            if machine.state == method.state:
                return method(machine, *_, **__)
            else:
                # print(f"drop {method}, not it's state")
                return None

        return event_handler

    return state_decorator


def transits(desc):
    if '->' in desc:
        current, target = desc.split('->')
    elif '<-' in desc:
        current, target = desc.split('<-')

    def transit_decorator(method):
        def transit_handler(machine, newstate, *_, **__):
            result = method(machine, *_, **__)
            machine.state = target
            return result

        transit_handler.transits = desc
        return transit_handler

    return transit_decorator
