import dataclasses

import mappr


@dataclasses.dataclass
class Src:
    text: str = 'hello'
    num: int = 10


@dataclasses.dataclass
class Dst:
    text: str
    num: int = 20


def test_auto_generated_converter(scoped_register):
    mappr.register(Src, Dst)

    assert mappr.convert(Dst, Src()) == Dst(text='hello', num=10)


def test_use_default(scoped_register):
    mappr.register(Src, Dst, mapping=dict(num=mappr.use_default))

    assert mappr.convert(Dst, Src()) == Dst(text='hello', num=20)
