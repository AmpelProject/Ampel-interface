import pickle
from typing import Mapping

import pytest

from ampel.config.AmpelConfig import AmpelConfig
from ampel.content.T2Document import T2Document
from ampel.enum.DocumentCode import DocumentCode
from ampel.struct.AmpelBuffer import AmpelBuffer
from ampel.types import strict_iterable
from ampel.view.SnapView import SnapView
from ampel.view.T2DocView import T2DocView


@pytest.fixture
def config():
    return AmpelConfig(
        {
            "channel": {},
            "unit": {"FooUnit": {"base": ["AbsStateT2Unit"]}},
            "confid": {42: {"foo": 42}},
        }
    )


@pytest.fixture
def t2_doc():
    doc: T2Document = {
        "unit": "FooUnit",
        "config": 42,
        "stock": 0,
        "link": 0,
        "code": DocumentCode.OK,
        "tag": ["TAGGERT"],
        "meta": [{}],
        "body": [{"foo": "bar"}],
    }
    return doc


@pytest.fixture
def t2_view(t2_doc, config):
    return T2DocView.of(t2_doc, config)


@pytest.fixture
def buffer(t2_doc):
    return AmpelBuffer(
        id=0,
        t2=[t2_doc],
    )


@pytest.fixture
def snap_view(buffer, config):
    return SnapView.of(buffer, config)


@pytest.fixture(params=["t2_view", "snap_view"])
def view(request):
    yield request.getfixturevalue(request.param)


def serialize(view):
    """Turn a view into a JSON rep for rich comparisons"""
    if hasattr(view, "__slots__"):
        return {k: serialize(getattr(view, k)) for k in view.__slots__}
    elif isinstance(view, strict_iterable):
        return [serialize(item) for item in view]
    elif isinstance(view, Mapping):
        return {k: serialize(v) for k, v in view.items()}
    else:
        return view


def test_confid_resolution(t2_doc, t2_view, config):
    assert t2_view.confid == t2_doc["config"]
    assert t2_view.config == config.get(["confid", t2_doc["config"]], dict)


def test_pickle(view):
    """__reduce__ provides correct arguments to __init__"""
    unpickled = pickle.loads(pickle.dumps(view))
    assert serialize(unpickled) == serialize(view)


def test_frozen(view):
    with pytest.raises(ValueError):
        view.id = 1