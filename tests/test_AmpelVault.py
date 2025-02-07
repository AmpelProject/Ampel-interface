import warnings
from typing import Any, cast

import pytest
from pydantic import ValidationError

from ampel.abstract.AbsSecretProvider import AbsSecretProvider
from ampel.base.AmpelBaseModel import AmpelBaseModel
from ampel.secret.AmpelVault import AmpelVault
from ampel.secret.NamedSecret import NamedSecret, Secret


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
    """Secret fields can be initialized with and without type hints, but validate if fields are provided"""
    secret = HasSecret(secret=NamedSecret[str](label="foo", value="bar")).secret
    assert HasSecret(secret=NamedSecret(label="foo", value="bar")).secret == secret
    assert HasSecret(**{"secret": {"label": "foo", "value": "bar"}}).secret == secret  # type: ignore[arg-type]
    # type parameter defaults to Any
    NamedSecret(label="foo", value=1)
    # validation fails with explicit type hint
    with pytest.raises(ValidationError):
        NamedSecret[str](label="foo", value=1)  # type: ignore[arg-type]
    # validation succeeds with correct type hint
    int_secret = NamedSecret[int](label="foo", value=1)
    # but passing the value to a model field will fail
    with pytest.raises(ValidationError):
        HasSecret(secret=int_secret)  # type: ignore[arg-type]


def test_secret_validation_hook() -> None:
    class HasSecret(AmpelBaseModel):
        secret: NamedSecret[str]
    
    vault = AmpelVault([DummySecretProvider({"foo": "bar"})])

    with NamedSecret.resolve_with(vault):
        resolved = HasSecret.model_validate({"secret": {"label": "foo"}})
    unresolved = HasSecret.model_validate({"secret": {"label": "foo"}})
    assert resolved.secret.get() == "bar"
    with pytest.raises(ValueError, match="Secret not yet resolved"):
        unresolved.secret.get()
    
    # get_named_secret can be used to fetch optional secrets even in a resolving context
    with NamedSecret.resolve_with(vault):
        ns = vault.get_named_secret("foo", str)
        assert ns is not None
        assert ns.get() == "bar"
        assert vault.get_named_secret("foo", int) is None


def test_secret_resolution() -> None:
    vault = AmpelVault([DummySecretProvider({"foo": "bar"})])

    secret = vault.get_named_secret("foo", str)
    assert secret is not None
    assert secret.get() == "bar"

    assert (
        HasSecret(secret=secret).secret.get() == "bar"
    ), "model can be instantiated with resolved secret"

    assert vault.get_named_secret("foo", int) is None


def test_value_set():
    secret = NamedSecret[int](label="foo")
    with pytest.raises(ValueError, match="Secret not yet resolved"):
        secret.get()
    secret.set(1)
    assert secret.get() == 1
    with pytest.raises(ValueError, match="Secret already resolved"):
        secret.set(1)


def test_implicit_generic_args() -> None:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        class Foo(AmpelBaseModel):
            seekrit: NamedSecret[dict] = NamedSecret(label="dict")

    annotation = cast(type[AmpelBaseModel], Foo.model_fields["seekrit"].annotation)
    assert annotation.get_model_args() == (dict,)
