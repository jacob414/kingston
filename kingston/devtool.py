# yapf
"""
A couple of typical development tools I tend to use..
"""
from textwrap import dedent


def out(formatted, **kwargs):
    print(dedent(formatted.format(**kwargs)))
