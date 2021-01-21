from dataclasses import asdict, dataclass

import mappr


@dataclass
class Src:
    text: str = 'hello'
    num: int = 10


@dataclass
class Dst:
    content: str = 'world'
    count: int = 20


# TODO: tests are not idempotent because of this.
mappr.register_iso(Src, Dst, mapping=dict(
    content='text',
    count='num'
))


def test_can_convert_src_to_dst():
    src = Src()

    result = mappr.convert(Dst, src)

    expected = Dst(content='hello', count=10)
    assert asdict(result) == asdict(expected)


def test_can_convert_dst_to_src():
    dst = Dst()

    result = mappr.convert(Src, dst)

    expected = Src(text='world', num=20)
    assert asdict(result) == asdict(expected)
