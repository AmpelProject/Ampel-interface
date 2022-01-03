import pytest
from ampel.base.AmpelBaseModel import AmpelBaseModel

def test_dict_view():

    class Base(AmpelBaseModel):
        base: int = 1
    
    class Derived(Base):
        derived: int = 2
    
    # base can't be instantiated with dict repr of derived
    with pytest.raises(ValueError):
        Base(**Derived().dict())
    
    # base _can_ be instantiated with a slice of derived
    base = Base(**Derived(base=42, derived=3).dict(include=Base._aks))

    assert base.dict() == Base(base=42).dict()


def test_default_override():
    class Base(AmpelBaseModel):
        base: int = 1
    
    class Derived(Base):
        base = 2
    
    assert Derived().base == 2
