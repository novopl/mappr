from dataclasses import asdict, dataclass

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


@dataclass
class Account:
    name: str
    age: str

    def __init__(self):
        super(Account, self).__init__()


def test_raises_TypeNotSupported_if_no_iterator_registered(scoped_register):
    mappr.register(Person, User)

    with pytest.raises(mappr.TypeNotSupported):
        mappr.convert(User, Person(name='John', age=25))


def test_constructor_strategy_doesnt_work_without_appropriate_ctor(scoped_register):
    mappr.register(Person, Account)

    with pytest.raises(TypeError) as exc_info:
        mappr.convert(Account, Person(name='John', age=25))

    assert 'got an unexpected keyword argument' in str(exc_info.value)


def test_can_override_strategy_for_single_conversion(scoped_register):
    mappr.register(Person, Account)

    account = mappr.convert(
        Account,
        Person(name='John', age=25),
        strategy=mappr.Strategy.SETATTR
    )

    assert asdict(account) == {
        'name': 'John',
        'age': 25,
    }
