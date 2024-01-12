import pytest
from typing import Generic, TypeVar
from ampel.base.AmpelBaseModel import AmpelBaseModel
from ampel.base.AmpelABC import AmpelABC
from ampel.base.decorator import abstractmethod


def test_check_methods():
    class Base(AmpelABC, abstract=True):
        @abstractmethod
        def foo(self, arg: int) -> None:
            ...

    with pytest.raises(NotImplementedError):

        class NotImplemented(Base):
            ...

    with pytest.raises(TypeError):

        class WrongImplementation(Base):
            def foo(self, arg: int, blarg: str) -> None:
                ...

    class CorrectImplementation(Base):
        def foo(self, arg: int) -> None:
            ...


def test_generic_with_basemodel():
    """AmpelABC can mix with the combination of AmpelBaseModel and Generic"""

    T = TypeVar("T")

    class Base(AmpelABC, AmpelBaseModel, Generic[T], abstract=True):
        @abstractmethod
        def foo(self, arg: T) -> None:
            ...

    class CorrectImplementation(Base[int]):
        def foo(self, arg: int) -> None:
            ...

    assert CorrectImplementation().foo(42) is None
