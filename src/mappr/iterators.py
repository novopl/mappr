import dataclasses
from typing import Any, Callable, List, Optional, Type

from . import types


g_field_iterators: List[types.FieldIter] = []


def field_iterator(test=types.TestFn):
    def decorator(fn: Callable[[Any], types.FieldIterator]):
        g_field_iterators.append(types.FieldIter(test=test, iter=fn))
        return fn
    return decorator


def iter_fields(any_cls: Type):
    if field_iter := _find_field_iter(any_cls):
        yield from field_iter.make_iterator(any_cls)


def _find_field_iter(any_cls: Type) -> Optional[types.FieldIter]:
    return next(
        (x for x in g_field_iterators if x.can_handle(any_cls)),
        None
    )


@field_iterator(test=lambda cls: dataclasses.is_dataclass(cls))
def _dataclass_iter_fields(model_cls: Any) -> types.FieldIterator:
    for field in dataclasses.fields(model_cls):
        yield field.name


@field_iterator(test=lambda cls: hasattr(cls, '__table__'))
def _sa_model_iter_fields(model_cls: Any) -> types.FieldIterator:
    yield from model_cls.__table__.columns.keys()
