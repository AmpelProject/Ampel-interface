import warnings
from collections.abc import Sequence

import pytest

from ampel.base.AmpelBaseModel import AmpelBaseModel
from ampel.base.AmpelUnit import AmpelUnit
from ampel.secret.NamedSecret import NamedSecret
from ampel.types import Traceless


def test_mixed_inheritance():
    class U(AmpelUnit):
        unit_param: int
        unit_param_with_default: int = 3

    class M(AmpelBaseModel):
        basemodel_param: int
        basemodel_param_with_default: int = 2

    class PrivateMixin:
        """Set a 'private' variable to test whether BaseModel.__setattr__ works"""

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self._foo = 1

    class Derived1(PrivateMixin, U, M):
        ...

    class Derived2(PrivateMixin, M, U):
        ...

    kwargs = {"unit_param": 1, "basemodel_param": 2}
    defaults = {"unit_param_with_default": 3, "basemodel_param_with_default": 2}

    # can derive from AmpelUnit first
    assert Derived1(**kwargs).dict() == kwargs | defaults
    # or from AmpelBaseModel first
    assert Derived2(**kwargs).dict() == kwargs | defaults


def test_embedded_model():
    """
    parameters that are themselves models are converted to instances of those models
    """

    class Item(AmpelBaseModel):
        a: int = 2
        b: int = 3

    class Unit(AmpelUnit):
        item: Item

    unit = Unit(item={"a": 1})
    assert isinstance(
        unit.item, Item
    ), "item should be an instance of Item (rather than dict)"
    assert unit.item.a == 1


def test_validate():
    """Validate returns default fields"""

    class Unit(AmpelUnit):
        required: str
        thing1: int = 1
        thing2: None | bool = None

    with pytest.raises(TypeError):
        Unit.validate({})

    assert Unit.validate({"required": "yes"}) == {
        "required": "yes",
        "thing1": 1,
        "thing2": None,
    }


def test_secret_without_type():
    class UnitWithSecret(AmpelUnit):
        secret: NamedSecret[str] = NamedSecret(label="foo")
        # a type where isinstance(annotation, type) is True, but
        # issubclass(annotation, AmpelBaseModel) throws TypeError
        other: Sequence[int] = [1]

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        assert UnitWithSecret().secret.get_model_args() == (str,)


def test_slots():
    class Slots:
        __slots__ = ("cherry", "banana", "bubblegum")

        cherry: int
        banana: int
        bubblegum: int

    class SlotMachine(AmpelUnit, Slots):
        _slot_defaults = {"cherry": 3, "banana": 1}

    assert SlotMachine._sks == set(Slots.__slots__)

    with pytest.raises(TypeError):
        SlotMachine()

    unit = SlotMachine(bubblegum=5)
    assert unit.cherry == 3
    assert unit.banana == 1
    assert unit.bubblegum == 5
    assert unit.dict() == {"cherry": 3, "banana": 1, "bubblegum": 5}


def test_default_override():
    class Base(AmpelUnit):
        a: int = 1

    class Derived(Base):
        """override default without providing new annotation"""
        a = 2

    with pytest.raises(TypeError):
        Derived(a="blah")

    assert Derived.get_model_keys() == {"a"}

    assert Derived().a == 2

    class SlotDerived(Base):
        """appanently you can provide defaults this way too"""
        a: int
        _slot_defaults = {"a": 3}
    
    assert SlotDerived().a == 3

def test_trace_content():
    class Unit(AmpelUnit):
        config: int = 1
        runtime: Traceless[str]

    Unit.validate({}) == {"config": 1}
    with pytest.raises(TypeError):
        Unit.validate_all({})

    with pytest.raises(TypeError):
        Unit()

    assert Unit(runtime="hola")._get_trace_content() == {"config": 1}
    assert Unit(runtime="hola").dict() == {"config": 1}

    Unit.validate_all({"runtime": "hola"}) == {"config": 1, "runtime": "hola"}


def test_dict():
    class Model(AmpelBaseModel):
        param: int = 1

    class Unit(AmpelUnit):
        a: list[int] = [1, 2, 3]
        b: dict[str, int] = {"a": 1}
        c: Model

    assert Unit(c=Model()).dict() == {"a": [1, 2, 3], "b": {"a": 1}, "c": {"param": 1}}
    assert Unit(a=[1, 2, 3], c=Model()).dict(exclude_defaults=True) == {
        "c": {"param": 1}
    }
    assert Unit(a=[1, 2, 3], c=Model()).dict(exclude_unset=True) == {
        "a": [1, 2, 3],
        "c": {"param": 1},
    }
    assert Unit(a=[1, 2, 3], c=Model()).dict(exclude={"a"}, exclude_defaults=True) == {
        "c": {"param": 1},
    }
