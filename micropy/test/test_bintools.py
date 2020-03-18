from micropy import bintools


def test_binstr():
    # type: () -> None
    "Should convert an int to a string in conventient human-readable form"
    assert bintools.binstr(0b101) == '00000101'


def test_snv():
    # type: () -> None
    "Should convert an int to a plesantly spaced string"
    assert bintools.snv(0b101) == '0  0  0  0  0  1  0  1'


def test_hexdump():
    # type: () -> None
    "Should print a pleasantly spaced hex dump of a string"
    assert bintools.hexdump('\x01\x02\x03\x3a') == '01 02 03 3a'


def test_shiftl_fn():
    # type: () -> None
    "Should have a correct shift left function"
    assert bintools.ops.shiftl(2, 10) == 10 << 2


def test_shiftr_fn():
    # type: () -> None
    "Should have a correct shift right function"
    assert bintools.ops.shiftr(2, 10) == 10 >> 2
