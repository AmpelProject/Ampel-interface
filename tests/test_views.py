import pickle
import sys
from collections.abc import Generator, Mapping
from dataclasses import dataclass
from typing import Any, assert_type, no_type_check

import pytest
from pydantic import TypeAdapter
from typing_extensions import TypedDict

from ampel.config.AmpelConfig import AmpelConfig
from ampel.content.T2Document import T2Document
from ampel.content.T3Document import T3Document
from ampel.enum.DocumentCode import DocumentCode
from ampel.struct.AmpelBuffer import AmpelBuffer
from ampel.types import strict_iterable
from ampel.view.SnapView import SnapView
from ampel.view.T2DocView import T2DocView
from ampel.view.T3DocView import T3DocView


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
        "link": sys.maxsize,
        "channel": ["CHANCHAN"],
        "code": DocumentCode.OK,
        "tag": ["TAGGERT"],
        "meta": [{"tier": 2, "code": DocumentCode.OK}],
        "body": [{"foo": "bar"}],
    }
    return doc


@pytest.fixture
def t2_view(t2_doc: T2Document, config: AmpelConfig):
    return T2DocView.of(t2_doc, config)


@pytest.fixture
def buffer(t2_doc: T2Document):
    return AmpelBuffer(
        id=-sys.maxsize,
        t2=[t2_doc],
    )


@pytest.fixture
def snap_view(buffer: AmpelBuffer, config: AmpelConfig):
    return SnapView.of(buffer, config)


@pytest.fixture
def t3_doc():
    doc: T3Document = {
        "unit": "FooUnit",
        "confid": 42,
        "stock": [2 * sys.maxsize],
        "code": DocumentCode.OK,
        "tag": ["TAGGERT"],
        "meta": {},
        "body": [{"foo": "bar"}],
    }
    return doc


@pytest.fixture
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
    if isinstance(view, strict_iterable):
        return [serialize(item) for item in view]
    if isinstance(view, Mapping):
        return {k: serialize(v) for k, v in view.items()}
    return view


def test_confid_resolution(t2_doc: T2Document, t2_view: T2DocView, config: AmpelConfig):
    assert (confid := t2_doc["config"]) is not None
    assert t2_view.confid == confid
    assert t2_view.config == config.get(["confid", confid], dict)


def test_pickle(view: T2DocView | SnapView | T3DocView):
    """__reduce__ provides correct arguments to __init__"""
    unpickled = pickle.loads(pickle.dumps(view))
    assert serialize(unpickled) == serialize(view)


def test_json(view: T2DocView | SnapView | T3DocView):
    model = TypeAdapter(type(view))
    dumped = model.validate_json(model.dump_json(view))
    assert serialize(dumped) == serialize(view)


def test_frozen(view: T2DocView | SnapView | T3DocView):
    with pytest.raises(AttributeError, match="cannot assign to field"):
        view.stock = 1  # type: ignore[misc]


class DictWithKnownSchema(TypedDict):
    foo: str


def test_get_payload(t2_view: T2DocView):
    assert t2_view.get_payload() == {"foo": "bar"}
    assert t2_view.get_payload(DictWithKnownSchema) == {"foo": "bar"}
    with pytest.raises(ValueError, match="No content available"):
        t2_view.get_payload(code=DocumentCode.T2_FAILED_DEPENDENCY, raise_exc=True)

    assert_type(t2_view.get_payload(), Mapping[str, Any] | None)
    assert_type(t2_view.get_payload(raise_exc=True), Mapping[str, Any])
    # NB: because get_payload() returns a constrained type, the inferred return
    # type is exactly one of its members, not the requested subtype
    assert_type(t2_view.get_payload(DictWithKnownSchema), Mapping[str, Any] | None)
    assert_type(
        t2_view.get_payload(DictWithKnownSchema, raise_exc=True), Mapping[str, Any]
    )
    assert_type(t2_view.get_payload(dict, raise_exc=True), Mapping[str, Any])


def test_get_t2_body(snap_view: SnapView):
    assert snap_view.get_t2_body("FooUnit") == {"foo": "bar"}
    assert snap_view.get_t2_body("nonesuch") is None
    with pytest.raises(ValueError, match="No matching body found"):
        snap_view.get_t2_body("nonesuch", raise_exc=True)

    assert_type(snap_view.get_t2_body("FooUnit"), Mapping[str, Any] | None)
    assert_type(snap_view.get_t2_body("FooUnit", dict), Mapping[str, Any] | None)
    assert_type(snap_view.get_t2_body("FooUnit", int), int | None)


def test_snapview_subclass(buffer: AmpelBuffer, config: AmpelConfig):
    """
    Subclassing SnapView should add slots to the subclass
    """
    @dataclass(frozen=True, slots=True)
    class SubView(SnapView):
        extra_thing: int = 2

    assert "id" not in SubView.__slots__
    assert "extra_thing" in SubView.__slots__

    subview = SubView.of(buffer, config)
    assert subview.id == buffer["id"]
    assert subview.extra_thing == 2
