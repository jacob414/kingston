# yapf

import hashlib
import fnmatch

from . import lang
from dataclasses import dataclass
from functools import singledispatch

import funcy


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

        @eq.register(cls.PrimType)
        def _(other):
            "Does _"
            return other == obj.raw_value

        obj.eq = eq

        lang.bind_methods(cls, obj)

        return obj

    def __init__(self, name, value):
        self.name = name

    @staticmethod
    def isa(other):
        return isinstance(other, Attr.__class__)

    def sibling(self, other):
        return isinstance(other.__class__, Attr.__class__)

    def eq(self, other):
        return self.eq(self, other)

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

        elif self.PrimType is lang.Undefined:
            return '????'

        else:
            return self.PrimType(self)

    @property
    def type_name(self):
        "Return name of primitive type"

        # NB: Special case to avoid infinite recursion.
        if self.PrimType is str:
            return 'str'

        else:
            return self.PrimType.__name__

    def __str__(self):
        return "{}={}:{}".format(self.name, self.raw_value, self.type_name)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        "Does __hash__"
        value = self.PrimType(self)
        return hashlib.sha1('{}:{}'.format(self.name, value)).hexdigest()

    def __eq__(self, other):
        if hasattr(other, 'name'):
            return (other.name == self.name
                    and other.raw_value == self.raw_value)
        else:
            return other == self.raw_value


for name, PrimType in (('IntAttr', int),
                       ('FloatAttr', float),
                       ('TupleAttr', tuple),
                       ('ListAttr', list),
                       ('StrAttr', str)):  # yapf: disable
    AttrClass = lang.mkclass(name, (Attr, PrimType))
    AttrClass.PrimType = PrimType

    locals()[name] = AttrClass
    Attr.infer_types[PrimType] = AttrClass


def xget(obj, idx):
    "Does foo"
    if lang.isprimitive(obj):
        return obj
    if callable(obj):
        return obj(idx)  # ???

    def attempt_many():
        "Does attempt_many"
        vars_ = lang.pubvars(obj)
        attrs = fnmatch.filter(vars_, idx)
        if funcy.is_seqcoll(obj) or isinstance(obj, set):
            return attrs
        else:
            return [Attr.infer(attr, xget(obj, attr)) for attr in attrs]

    try:
        try:
            return obj[lang.maybe_int(idx)]
        except KeyError:
            return attempt_many()
    except TypeError:
        try:
            return getattr(obj, idx)
        except AttributeError:
            return attempt_many()


class AttrQuery(tuple):
    def __new__(cls, parts, *params, **opts):
        "Does __new__"
        pt, = lang.primbases(cls)
        instance = pt.__new__(cls, parts, *params, **opts)
        return instance

    @staticmethod
    def from_text(text):
        return AttrQuery(tuple(text.split('.')))


def idig(obj, path):
    "Recursive query for attributes from `obj` by a sequence spec."
    key = path.pop(0)
    point = xget(obj, key)
    if path:
        return idig(point, path)
    else:
        return point


def dig(obj, path):
    "Recursive query for attributes from `obj` by string spec."

    return idig(obj, path.split('.'))
