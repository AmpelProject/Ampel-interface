import pytest
from typing import Generic, TypeVar
from ampel.base.AmpelBaseModel import AmpelBaseModel


def test_dict_view():
    class Base(AmpelBaseModel):
        base: int = 1

    class Derived(Base):
        derived: int = 2

    # base can't be instantiated with dict repr of derived
    with pytest.raises(TypeError):
        Base(**Derived().dict())

    # base _can_ be instantiated with a slice of derived
    base = Base(**Derived(base=42, derived=3).dict(include=Base.get_model_keys()))

    assert base.dict() == Base(base=42).dict()


def test_default_override():
    class Base(AmpelBaseModel):
        base: int = 1

    class Derived(Base):
        base = 2

    assert Derived().base == 2


@pytest.mark.parametrize(
    "value",
    [
        {"field": {"a": 1}},
        {"field": {"all_of": [{"a": 1}]}},
        {"field": {"any_of": [{"a": 1}]}},
        {"field": {"any_of": [{"all_of": [{"a": 1}]}]}},
    ],
    ids=["value", "all_of", "any_of", "any_of_nested"],
)
def test_nested_typevar(value):
    """AmpelBaseModel can validate deeply nested generics"""

    T = TypeVar("T")

    class AllOf(Generic[T], AmpelBaseModel):
        all_of: list[T]

    class AnyOf(Generic[T], AmpelBaseModel):
        any_of: list[T | AllOf[T]]

    class Inner(AmpelBaseModel):
        a: int

    class Outer(AmpelBaseModel):
        field: Inner | AnyOf[Inner] | AllOf[Inner]

    Outer(**value)
