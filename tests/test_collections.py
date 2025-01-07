
from ampel.util.collections import to_set


def test_to_set():

    assert to_set("abc") == {'abc'}
    assert to_set(("abc",)) == {'abc'}
