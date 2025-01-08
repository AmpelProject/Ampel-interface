from copy import deepcopy

import pytest
from pydantic import ValidationError

from ampel.alert.AmpelAlert import AmpelAlert
from ampel.base.AmpelBaseModel import AmpelBaseModel
from ampel.protocol.AmpelAlertProtocol import AmpelAlertProtocol


def test_protocol():
    alert = AmpelAlert(0, 0, [])
    assert isinstance(
        alert, AmpelAlertProtocol
    ), "dataclass fields recognized as protocol"

    assert alert.tag is None, "defaults are populated"

    class Model(AmpelBaseModel):
        alerts: list[AmpelAlertProtocol]

    # this works: AmpelAlert is a structural sub-type of AmpelAlertProtocol
    m = Model(
        alerts=[AmpelAlert(id=0, stock="stockystock", datapoints=[{"id": 0}])]
    )
    assert isinstance(
        m.model_dump(mode="json")["alerts"][0], dict
    ), "dataclass serialized as dict"
    # this does not: pydantic does not know how to deserialize a dict to AmpelAlertProtocol
    with pytest.raises(ValidationError):
        Model(**m.model_dump(mode="json"))


def test_hash():
    """AmpelAlert should be hashable"""
    alert = AmpelAlert(id=0, stock="stockystock", datapoints=[{"id": 0}])
    assert hash(alert) != hash(deepcopy(alert)), "hash is not the same after deepcopy"
