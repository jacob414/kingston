from typing import Any

class FSM:
    state: Any = ...
    def __init__(self, initial: Any) -> None: ...
    def methods(self) -> None: ...
    def transition(self, state: Any, *args: Any, **kwargs: Any) -> Any: ...

def state(name: Any) -> Any: ...
def transits(desc: Any) -> Any: ...
