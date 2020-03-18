# yapf

from micropy import view


def test_view_single():
    # type: () -> None
    "Should "
    assert view.nice(1) == '1'


def test_view_dict():
    # type: () -> None
    "Does test_view_dict"
    assert view.nice({'foo': 'bar'}) == "{'foo': 'bar'}"


def test_view_list():
    # type: () -> None
    "Should show list type"
    assert view.nice([1, 2, 3, 4]) == '[1, 2, 3, 4]'


def test_bits_print():
    # type: () -> None
    "Should "
    assert view.visual_bits_print(1) \
        == '0  0  0  0  0  0  0  1\n0  1  2  3  4  5  6  7'
