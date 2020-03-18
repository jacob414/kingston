# yapf

from typing import Iterable, Any


def pytest_collection_modifyitems(items: Iterable, config: Any):
    for item in items:
        if not any(item.iter_markers()):
            item.add_marker("bbox")
