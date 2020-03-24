# yapf

import pprint
import textwrap


def nice(ob, compress=2):
    # type: (ob) -> None
    "Does nice"
    return textwrap.dedent(pprint.pformat(ob)).replace(compress * ' ', ' ')


def binstr(value, width=8):
    prefixd = width + 3
    fmt = "#{}b".format(prefixd)
    return format(value, fmt).strip().replace('0b', '').zfill(width)


def nv(value, width=8):
    return binstr(value, width)


def snv(value, width=8):
    return '\n'.join(('  '.join(idx % 2 == 2 and ch + ' ' or ch
                                for idx, ch in enumerate(nv(value, width))),
                      '0  1  2  3  4  5  6  7'))


def visual_bits_print(value, width=8):
    out = snv(value, width)
    print(out)
    return out
