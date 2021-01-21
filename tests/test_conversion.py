from dataclasses import dataclass

import pytest

import mappr


@dataclass
class Person:
    name: str
    age: int


class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


def test_raises_TypeNotSupported_if_no_iterator_registered(scoped_register):
    mappr.register(Person, User)

    with pytest.raises(mappr.TypeNotSupported):
        mappr.convert(User, Person(name='John', age=25))
