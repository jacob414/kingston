# yapf

import pytest

from micropy import fsm


class Machine(fsm.FSM):
    @fsm.state('stopped')
    def start(self: 'Machine') -> str:
        return 'stopped.start'

    # fsm.cond('stopped->running', lambda m: m.engines is On)

    @fsm.transits('stopped->running')
    # @fsm.transits(Stopped, Running)
    def liftoff(self: 'Machine') -> str:
        return 'stopped->running'

    @fsm.state('running')
    def halt(self: 'Machine') -> str:
        return 'running.halt'

    @fsm.state('running')
    def stop(self: 'Machine') -> str:
        return 'running.stop'


def test_calls_method_in_current_state():
    assert Machine('stopped').start() == 'stopped.start'


def test_noops_method_in_other_state():
    assert Machine('stopped').halt() == None


def test_calls_transit_on_transition():
    m = Machine('stopped')
    # m.transition(Running)
    assert 'stopped->running' in set(m.transition('running'))
    assert m.state == 'running'
