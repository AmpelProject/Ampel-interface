import pytest
from types import UnionType
from typing import Generic, TypeVar, Union, get_origin
from ampel.base.AmpelBaseModel import AmpelBaseModel
from ampel.base.AmpelUnit import AmpelUnit
from pydantic import ValidationError


def test_dict_view():
    class Base(AmpelBaseModel):
        base: int = 1

    class Derived(Base):
        derived: int = 2

    # base can't be instantiated with dict repr of derived
    with pytest.raises(ValidationError):
        Base(**Derived().dict())

    # base _can_ be instantiated with a slice of derived
    base = Base(**Derived(base=42, derived=3).dict(include=set(Base.get_model_keys())))

    assert base.dict() == Base(base=42).dict()


def test_default_override():
    class Base(AmpelBaseModel):
        base: int = 1

    class Derived(Base):
        base: int = 2

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

    class AllOf(AmpelBaseModel, Generic[T]):
        all_of: list[T]

    class AnyOf(AmpelBaseModel, Generic[T]):
        any_of: list[T | AllOf[T]]

    class Inner(AmpelBaseModel):
        a: int

    class Outer(AmpelBaseModel):
        field: Inner | AnyOf[Inner] | AllOf[Inner]

    assert Outer(**value).model_dump() == value


@pytest.mark.parametrize("base", [AmpelBaseModel, AmpelUnit])
def test_implicit_default_none(base: type):
    """
    Implicit default None is added for both Union (typing.Union[a,b]) and
    UnionType (a | b) annotations that include None
    """

    class ImplicitDefault(base):
        union: None | Union[int, str]
        union_type: None | int

    assert get_origin(ImplicitDefault.__annotations__['union']) is Union
    assert get_origin(ImplicitDefault.__annotations__['union_type']) is UnionType

    assert ImplicitDefault().dict() == {"union": None, "union_type": None}


