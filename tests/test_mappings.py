import json
import sys

import pytest
from ampel.config.AmpelConfig import AmpelConfig
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


@pytest.mark.parametrize(
    "target,key,value",
    [
        ({1: {"foo": "bar"}}, ["confid", 1], {"foo": "bar"}),
        ({-1: {"foo": "bar"}}, "confid.-1", {"foo": "bar"}),
    ],
)
def test_AmpelConfig_get_with_path(target, key, value):
    ac = AmpelConfig({"channel": {}, "confid": target})
    assert ac.get(key, dict) == value
    with pytest.raises(ValueError):
        ac.get(key, int)


def test_AmpelConfig_get_raise_exc():
    with pytest.raises(ValueError):
        AmpelConfig({"channel": {}, "confid": {1: "foo"}}).get(
            ["confid", 2], raise_exc=True
        )


@pytest.mark.parametrize("key", ["1", "-1_000", str(-sys.maxsize), str(sys.maxsize)])
@pytest.mark.parametrize("section", ["channel", "confid"])
def test_AmpelConfig_intify_on_load(key, section, tmp_path):
    """
    stringified dict keys are intified on load
    """
    path = tmp_path / "config.json"

    path.write_text(
        json.dumps(
            {"channel": {key: {"channel": "CHAN"}}, "confid": {key: {"foo": 42}}}
        )
    )
    ac = AmpelConfig.load(str(path))
    assert ac.get([section, key], dict) is not None
    assert ac.get([section, int(key)], dict) is not None
    assert ac.get(f"{section}.{key}", dict) is not None
