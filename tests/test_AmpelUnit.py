import pytest

from ampel.base.AmpelBaseModel import AmpelBaseModel
from ampel.base.AmpelUnit import AmpelUnit


def test_mixed_inheritance():
    class U(AmpelUnit):
        unit_param: int

    class M(AmpelBaseModel):
        basemodel_param: int

    class Derived1(U, M):
        ...

    class Derived2(M, U):
        ...

    kwargs = {"unit_param": 1, "basemodel_param": 2}

    # can derive from AmpelUnit first
    assert Derived1(**kwargs).dict() == kwargs
    # or from AmpelBaseModel first
    assert Derived2(**kwargs).dict() == kwargs


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
    assert isinstance(unit.item, Item), "item should be an instance of Item (rather than dict)"
    assert unit.item.a == 1