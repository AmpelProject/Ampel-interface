import warnings
import pytest
from typing import cast, Any

from ampel.secret.AmpelVault import AmpelVault
from ampel.abstract.AbsSecretProvider import AbsSecretProvider
from ampel.secret.NamedSecret import Secret, NamedSecret
from ampel.base.AmpelBaseModel import AmpelBaseModel

from pydantic import ValidationError


class DummySecretProvider(AbsSecretProvider):
    def __init__(self, contents: dict[str, Any]) -> None:
        self.contents = contents

    def tell(self, secret: Secret, ValueType: type) -> bool:
        if isinstance(secret, NamedSecret) and isinstance(
            value := self.contents.get(secret.label), ValueType
        ):
            secret.set(value)
            return True
        return False


class HasSecret(AmpelBaseModel):
    secret: NamedSecret[str]


def test_secret_validation() -> None:
    HasSecret(secret=NamedSecret[str](label="foo"))
    with pytest.raises(ValidationError):
        HasSecret(secret=NamedSecret(label="foo"))


def test_secret_resolution() -> None:
    vault = AmpelVault([DummySecretProvider({"foo": "bar"})])

    secret = vault.get_named_secret("foo", str)
    assert secret is not None
    assert secret.get() == "bar"

    assert (
        HasSecret(secret=secret).secret.get() == "bar"
    ), "model can be instantiated with resolved secret"

    assert vault.get_named_secret("foo", int) is None

def test_implicit_generic_args() -> None:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        class Foo(AmpelBaseModel):
            seekrit: NamedSecret[dict] = NamedSecret(label="dict")

    annotation = cast(type[AmpelBaseModel], Foo.model_fields["seekrit"].annotation)
    assert annotation.get_model_args() == (dict,)
