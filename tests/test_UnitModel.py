from pytest_mock import MockerFixture

from ampel.model.UnitModel import UnitModel


def test_validation_hook(mocker: MockerFixture):
    """Validation hook is called on model construction"""

    # no hook
    UnitModel(unit="T2SNCosmo", config=1)

    hook = mocker.patch("ampel.model.UnitModel.UnitModel.post_validate_hook", side_effect=lambda x: x)

    u = UnitModel(unit="T2SNCosmo", config=1)

    assert hook.call_count == 1
    assert hook.call_args.args == (u,)
