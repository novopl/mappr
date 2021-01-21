import pytest


@pytest.fixture
def scoped_register():
    from mappr.conversion import g_converters

    reset_token = g_converters.set([])
    yield
    g_converters.reset(reset_token)
