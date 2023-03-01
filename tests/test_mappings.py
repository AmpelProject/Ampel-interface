import sys

import pytest

from ampel.util import mappings


@pytest.mark.parametrize(
    "target,key,value",
    [
        ({"foo": {"a1": 2}}, "foo.a1", 2),
        ({1000000: {"foo": 1}}, "1_000_000.foo", 1),
        ({-99: {"foo": 1}}, "-0099.foo", 1),
        ({-99: {"foo": 1}}, [-99, "foo"], 1),
        *(
            ({"foo": {"bar": {k: {1: 58}}}}, f"foo.bar.{k}", {1: 58})
            for k in (85, -sys.maxsize, sys.maxsize)
        ),
    ],
)
def test_get_by_path(target, key, value):
    assert mappings.get_by_path(target, key) == value
