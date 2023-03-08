import pytest

from ampel.base.AmpelBaseModel import AmpelBaseModel
from ampel.base.AmpelUnit import AmpelUnit

def test_mixed_inheritance():
    class U(AmpelUnit):
        unit_param: int
    
    class M(AmpelBaseModel):
        model_param: int
    
    class Derived1(U, M):
        ...
    
    class Derived2(M, U):
        ...

    # can derive from AmpelUnit first
    Derived1(unit_param=1, model_param=2)
    # but not in reverse
    with pytest.raises(TypeError):
        Derived2(unit_param=1, model_param=2)