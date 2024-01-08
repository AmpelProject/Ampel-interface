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