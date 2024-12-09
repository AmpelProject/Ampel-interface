from typing import assert_type

from ampel.util.collections import to_set


def test_to_set():

    assert to_set("abc") == {'abc'}
    assert to_set(("abc",)) == {'abc'}

    class sentinel:
        pass

    assert_type(to_set("abc"), set[str])
    assert_type(to_set(("abc",)), set[str])
    assert_type(to_set({1: sentinel()}.values()), set[sentinel])