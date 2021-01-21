""" A conversion system to ease converting between different types.

This will be especially useful types <-> models conversions.
"""
from .conversion import (  # noqa: F401
    convert,
    register,
    register_iso,
    TypeConverter,
)
from .exc import (  # noqa: F401
    ConverterAlreadyExists,
    Error,
    NoConverter,
)
from .iterators import (  # noqa: F401
    field_iterator,
    iter_fields,
)
from .mappers import (  # noqa: F401
    alias,
    set_const,
    use_default,
)
from .types import (  # noqa: F401
    FieldIterator,
    MappingFn,
    ConverterFn,
)

__version__ = '0.1.20'
