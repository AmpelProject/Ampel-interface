from ampel.alert.AmpelAlert import AmpelAlert
from ampel.protocol.AmpelAlertProtocol import AmpelAlertProtocol


def test_protocol():
    alert = AmpelAlert(0, 0, [])
    assert isinstance(alert, AmpelAlertProtocol), "dataclass fields recognized as protocol"

    assert alert.tag is None, "defaults are populated"
