# yapf

from typing import Any, Generator, List, Union


class GListlike(object):
    """Mimic `list` from a generator.

    **This is mostly a development tool! I strongly recommend against
    use in production.**

    *Performance is likely terrible and it may not implement stuff I
     haven't needed myself yet.*

    Use it in functions where you plan a generator in the end, but
    want to see yielded values in e.g. a debugger.

    """
    __gen__: Generator
    __consumed: List[Any]
    __cursor__: int
    __working__: bool

    def __init__(self, gen, *args, **kwargs):
        super(GListlike, self).__init__(*args, **kwargs)
        self.__gen__ = gen
        self.__consumed__ = []
        self.__cursor__ = 0
        self.__working__ = True

    def takenext(self):
        val = next(self.__gen__)
        self.__consumed__.append(val)
        self.__cursor__ += 1
        return val

    def consume(self):
        "Forward until last item of inner generator."
        while True:
            try:
                self[len(self.__consumed__) + 1]
            except StopIteration:
                self.__working__ = False
                break

    def __len__(self) -> int:
        if self.__working__:
            self.consume()

        return len(self.__consumed__)

    def __str__(self) -> str:
        self.consume()
        return f"{self.__consumed__} (GListlike)"

    def __repr__(self) -> str:
        self.consume()
        return f"<GListlike, {self.__consumed__!r}>"

    def __getitem__(self, index: Union[int, range]):
        if isinstance(index, slice):
            for x in range(index.start, index.stop + 1, index.step or 1):
                self.takenext()
            return self.__consumed__[index.start:index.stop + 1]
        else:
            while True:
                try:
                    return self.__consumed__[index]
                except IndexError:
                    self.takenext()
