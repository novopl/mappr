from dataclasses import dataclass
from typing import Any

from sqlalchemy import BigInteger, Column, String
from sqlalchemy.orm import declarative_base

import mappr


Model: Any = declarative_base()  # type: ignore


class UserModel(Model):
    __tablename__ = 'test_models'
    id = Column(BigInteger, primary_key=True)
    email = Column(String(120), unique=True, index=True)
    # handle is the external ID. The real user ID should never cross the service boundary.
    username = Column(String(120), unique=True, index=True)


@dataclass
class User:
    email: str = 'test@example.com'
    username: str = 'test.user'


def test_works(scoped_register):
    mappr.register(User, UserModel, mapping=dict(id=mappr.use_default))

    model = mappr.convert(UserModel, User())

    assert model.id is None
    assert model.email == 'test@example.com'
    assert model.username == 'test.user'
