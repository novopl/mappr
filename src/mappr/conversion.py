from typing import Type, TypeVar

from . import iterators, mappers, registry


T = TypeVar('T')


def convert(dst_type: Type[T], src_obj, strict: bool = True) -> T:
    """ Convert an object to a given type.

    Args:
        dst_type:   Target type. This is the type of the return value.
        src_obj:    An object to convert. A registered converter will be used
                    to map between the attributes of this object and the target
                    type.
        strict:     If set to ``False`` and the converter is not found for the
                    given type pair, it will create an ad-hoc one that maps
                    the attributes by their name. Defaults to ``True``

    Returns:
        A newly created instance of ``dst_type`` with values initialized
        from ``src_obj``.
    """
    converter = registry.get_converter(src_obj.__class__, dst_type, strict=strict)
    values = {}

    for name in iterators.iter_fields(converter.dst_type):
        mapping_fn = converter.mapping.get(name, mappers.alias(name))

        if mapping_fn != mappers.use_default:
            values[name] = mapping_fn(src_obj, name)

    return converter.dst_type(**values)
