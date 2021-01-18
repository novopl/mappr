import dataclasses

import pytest

import mappr


@dataclasses.dataclass
class Src:
    text: str = 'hello'
    num: int = 10


@dataclasses.dataclass
class Dst:
    text: str
    num: int = 20


def test_use_default():
    basic = mappr.TypeConverter(Src, Dst)
    with_default = mappr.TypeConverter(Src, Dst, mapping=dict(
        num=mappr.use_default,
    ))

    src = Src()

    assert basic.convert(src) == Dst(text='hello', num=10)
    assert with_default.convert(src) == Dst(text='hello', num=20)


def test_cannot_register_converter_twice_for_the_same_types():
    mappr.register(Src, Dst, mapping=dict(
        num=mappr.use_default,
    ))

    with pytest.raises(mappr.ConverterAlreadyExists):
        mappr.register(Src, Dst)
