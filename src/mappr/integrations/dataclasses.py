import dataclasses
from typing import Type

from mappr import types
from mappr.iterators import field_iterator


@field_iterator(test=lambda cls: dataclasses.is_dataclass(cls))
def dataclass_iter_fields(model_cls: Type) -> types.FieldIterator:
    yield from (f.name for f in dataclasses.fields(model_cls))
