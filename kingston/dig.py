# yapf
"""This module if for reading values from live objects. The general
idea is that you use a function ``kingston.dig.dig()`` with an object
and a string. The string is (somewhat) inspired by a CSS selector. It
specifies how to get a certain sub-element.

The goal is that these spec-strings should be storable for future
re-use.

This module is a work in progress module and thus subject to change.

"""

import hashlib
import fnmatch

from typing import Any

from . import lang
from .match import Miss

from dataclasses import dataclass
from functools import singledispatch

from collections import deque

import funcy as fy


@dataclass
class Attr:
    infer_types = {}
    PrimType = lang.Undefined
    __bind__ = []

    @classmethod
    def create(cls, name, value):

        obj = cls.__new__(cls, value)
        obj.name = name

        @singledispatch
        def eq(other):
            raise NotImplementedError("Attr: eq not implemented for {}".format(
                type(other)))

        @eq.register(Attr)
        def _(other):
            "Does _"
            return other.name == obj.name and other == obj

        obj.eq = eq

        lang.bind_methods(cls, obj)

        return obj

    @staticmethod
    def isa(other):
        return isinstance(other, Attr.__class__)

    def sibling(self, other):
        return isinstance(other.__class__, Attr.__class__)

    @classmethod
    def infer(cls, name, value):
        PrimType = Attr.infer_types[type(value)]
        return PrimType.create(name, value)

    @property
    def raw_value(self):
        "Cast value to primitive type."

        # NB: Special case to avoid infinite recursion.
        if self.PrimType is str:
            return str.__str__(self)

        else:
            return self.PrimType(self)

    @property
    def type_name(self):
        "Return name of primitive type"
        return self.PrimType.__name__

    def __str__(self):
        return "{}={}:{}".format(self.name, self.raw_value, self.type_name)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        "Does __hash__"
        value = self.PrimType(self)
        return hashlib.sha1('{}:{}'.format(self.name, value)).hexdigest()


for name, PrimType in (('IntAttr', int),
                       ('FloatAttr', float),
                       ('TupleAttr', tuple),
                       ('ListAttr', list),
                       ('StrAttr', str)):  # yapf: disable
    AttrClass = lang.mkclass(name, (Attr, PrimType))
    AttrClass.PrimType = PrimType

    locals()[name] = AttrClass
    Attr.infer_types[PrimType] = AttrClass


def subattr(obj: Any, path: str) -> Any:
    left = deque(path.split('.'))
    attr = obj

    while left:
        attrname = left.popleft()
        attr = getattr(attr, attrname)

    return attr


def xget(obj: Any, idx: Any) -> Any:
    """Single point of entry function to fetch a value / attribute /
    element from an object.

    :param obj: The object to find attribute / value in.
    :param idx: Symbolic index.

    """
    if lang.isprimitive(obj):
        return obj
    elif callable(obj):
        return obj(idx)  # ???

    def attempt_many():
        "Does attempt_many"
        vars_ = lang.pubvars(obj)
        attrs = fnmatch.filter(vars_, idx)
        if fy.is_seqcoll(obj) or isinstance(obj, set):
            return attrs
        else:
            return [Attr.infer(attr, xget(obj, attr)) for attr in attrs]

    try:
        try:
            return obj[idx]
        except KeyError:
            return attempt_many()
    except TypeError:
        try:
            return getattr(obj, idx)
        except AttributeError:
            return attempt_many()


def idig(obj: Any, path: Any) -> Any:
    "Recursive query for attributes from `obj` by a sequence spec."
    key = path.pop(0)
    point = xget(obj, key)
    if path:
        return idig(point, path)
    else:
        return point


def dig(obj: Any, path: str) -> Any:
    """Dig after object content from object content based on a string
    spec.

    :param obj: A live object that values should be digged from.
    :param path: String representation of the *”path”*
    """

    try:
        # Most dig operations are simply subattr()
        return subattr(obj, path)
    except AttributeError:
        pass

    return idig(obj, lang.detect_numbers(path.split('.')))
