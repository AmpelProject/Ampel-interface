import pickle
from collections.abc import Generator, Mapping
from typing import no_type_check

import pytest

from ampel.config.AmpelConfig import AmpelConfig
from ampel.content.T2Document import T2Document
from ampel.content.T3Document import T3Document
from ampel.enum.DocumentCode import DocumentCode
from ampel.struct.AmpelBuffer import AmpelBuffer
from ampel.types import strict_iterable
from ampel.view.SnapView import SnapView
from ampel.view.T2DocView import T2DocView
from ampel.view.T3DocView import T3DocView


@pytest.fixture()
def config():
    return AmpelConfig(
        {
            "channel": {},
            "unit": {"FooUnit": {"base": ["AbsStateT2Unit"]}},
            "confid": {42: {"foo": 42}},
        }
    )


@pytest.fixture()
def t2_doc():
    doc: T2Document = {
        "unit": "FooUnit",
        "config": 42,
        "stock": 0,
        "link": 0,
        "channel": ["CHANCHAN"],
        "code": DocumentCode.OK,
        "tag": ["TAGGERT"],
        "meta": [{}],
        "body": [{"foo": "bar"}],
    }
    return doc


@pytest.fixture()
def t2_view(t2_doc: T2Document, config: AmpelConfig):
    return T2DocView.of(t2_doc, config)


@pytest.fixture()
def buffer(t2_doc: T2Document):
    return AmpelBuffer(
        id=0,
        t2=[t2_doc],
    )


@pytest.fixture()
def snap_view(buffer: AmpelBuffer, config: AmpelConfig):
    return SnapView.of(buffer, config)


@pytest.fixture()
def t3_doc():
    doc: T3Document = {
        "unit": "FooUnit",
        "confid": 42,
        "stock": [0],
        "code": DocumentCode.OK,
        "tag": ["TAGGERT"],
        "meta": {},
        "body": [{"foo": "bar"}],
    }
    return doc

@pytest.fixture()
def t3_view(t3_doc: T3Document, config: AmpelConfig):
    return T3DocView.of(t3_doc, config)

@pytest.fixture(params=["t2_view", "snap_view", "t3_view"])
def view(request) -> Generator[T2DocView | SnapView | T3DocView, None, None]:
    return request.getfixturevalue(request.param)

@no_type_check
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


def test_confid_resolution(t2_doc: T2Document, t2_view: T2DocView, config: AmpelConfig):
    assert (confid := t2_doc["config"]) is not None
    assert t2_view.confid == confid
    assert t2_view.config == config.get(["confid", confid], dict)


def test_pickle(view: T2DocView | SnapView | T3DocView):
    """__reduce__ provides correct arguments to __init__"""
    unpickled = pickle.loads(pickle.dumps(view))
    assert serialize(unpickled) == serialize(view)


def test_frozen(view: T2DocView | SnapView | T3DocView):
    with pytest.raises(ValueError, match="is read only"):
        view.id = 1