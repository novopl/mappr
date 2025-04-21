from dataclasses import dataclass

import mappr


# A few sample models to demonstrate mappr.
@dataclass
class User:
    username: str
    first_name: str
    last_name: str
    email: str


@dataclass
class Person:
    nick: str
    name: str
    email: str


@dataclass
class UserPublic:
    username: str
    first_name: str


# We can register a mapper from ``User`` to ``Person``. Fields not specified in
# mapping will be copied directly. The source type needs the have attributes
# that match the name, otherwise an exception is raised.
mappr.register(User, Person, mapping=dict(
    nick=lambda o, _: o.username,
    name=lambda o, _: f"{o.first_name} {o.last_name}",
))

# We can now create a an instance of ``User`` so we can test our converter.
user = User(
    username='john.doe',
    first_name='John',
    last_name='Doe',
    email='john.doe@example.com',
)

# This will use the converter registered above. To allow conversion in the
# reverse direction, you need to register the appropriate converter first.
# Each converter works only one way.
assert mappr.convert(Person, user) == Person(
    nick='john.doe',
    name='John Doe',
    email='john.doe@example.com',
)

# For simple conversions, where the target type attributes are a subset of
# source's attributes, we can just pass ``strict=False`` to let mappr create
# an ad-hoc converter. This will only work if the attribute names are
# exactly the same.
assert mappr.convert(UserPublic, user, strict=False) == UserPublic(
    username='john.doe',
    first_name='John',
)
