import itertools
from enum import Enum
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, List, Optional

import pydantic
import pytest

import mappr


class UserType(Enum):
    REGULAR = 'REGULAR'
    ORG = 'ORG'


class User(pydantic.BaseModel):
    email: str
    username: str
    name: str
    last_name: str
    type: UserType = UserType.REGULAR
    token: Optional[str]

    roles: List[str] = pydantic.Field(default_factory=list)
    perms: List[str] = pydantic.Field(default_factory=list)

    created_at: datetime
    updated_at: datetime


class UserPublic(pydantic.BaseModel):
    username: str
    name: str
    last_name: str
    type: UserType = UserType.REGULAR
    created_at: datetime


class Role(pydantic.BaseModel):
    name: str
    perms: List[str]
    roles: List['Role']
    created_at: datetime
    updated_at: datetime

    def get_nested_roles(self) -> List['Role']:
        child_roles = (role.get_nested_roles() for role in self.roles)
        return list(itertools.chain(self.roles, *child_roles))


class UserInternal(pydantic.BaseModel):
    id: Optional[int]
    email: str
    username: str
    name: str
    last_name: str
    pw_hash: Optional[str]
    token: Optional[str]
    type: UserType = UserType.REGULAR

    roles: List[Role] = pydantic.Field(default_factory=list)
    perms: List[str] = pydantic.Field(default_factory=list)

    created_at: datetime
    updated_at: datetime


@dataclass
class WonkyUser:
    nick: str
    first_name: str
    last_name: str
    type: UserType
    joined_at: datetime

    def dict(self):
        return asdict(self)


mappr.register(User, UserInternal, mapping=dict(
    id=mappr.set_const(None),
    pw_hash=mappr.set_const(None),
))
mappr.register(User, WonkyUser, mapping=dict(
    nick=lambda o: o.username,
    first_name=lambda o: o.name,
    joined_at=lambda o: o.created_at,
))


@mappr.field_iterator(test=lambda cls: issubclass(cls, pydantic.BaseModel))
def _pydantic_iter_fields(model_cls: Any) -> mappr.FieldIterator:
    yield from model_cls.__fields__.keys()


@pytest.fixture
def user():
    yield User(
        email='fake@example.com',
        username='fake.user',
        name='Fake',
        last_name='User',
        type=UserType.REGULAR,
        token='42',
        roles=[],
        perms=[],
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


def test_user_to_internal(user):
    internal = mappr.convert(UserInternal, user)
    expected = UserInternal(
        email='fake@example.com',
        username='fake.user',
        name='Fake',
        last_name='User',
        type=UserType.REGULAR,
        token='42',
        roles=[],
        perms=[],
        created_at=user.created_at,
        updated_at=user.updated_at,
    )
    assert internal.dict() == expected.dict()


def test_will_create_adhoc_converter_if_strict_is_false(user):
    public = mappr.convert(UserPublic, user, strict=False)
    expected = UserPublic(
        username='fake.user',
        name='Fake',
        last_name='User',
        type=UserType.REGULAR,
        created_at=user.created_at,
    )
    assert public.dict() == expected.dict()


def test_converter_has_to_be_registered_first_if_strict_is_True(user):
    with pytest.raises(mappr.NoConverter):
        mappr.convert(UserPublic, user, strict=True)


def test_user_to_wonky(user):
    wonky = mappr.convert(WonkyUser, user)
    expected = WonkyUser(
        nick='fake.user',
        first_name='Fake',
        last_name='User',
        type=UserType.REGULAR,
        joined_at=user.created_at,
    )

    assert wonky.dict() == expected.dict()
