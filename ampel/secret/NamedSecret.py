#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/secret/NamedSecret.py
# License:             BSD-3-Clause
# Author:              Jakob van Santen <jakob.van.santen@desy.de>
# Date:                14.08.2020
# Last Modified Date:  30.12.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

import contextlib
from typing import TYPE_CHECKING, ClassVar
from pydantic import model_validator, Field
from ampel.base.AmpelBaseModel import AmpelBaseModel
from ampel.secret.Secret import Secret, T

if TYPE_CHECKING:
	from collections.abc import Generator
	from typing import Self
	from ampel.secret.AmpelVault import AmpelVault

class NamedSecret(AmpelBaseModel, Secret[T]):
	"""
	A Secret:
	- featuring a label used as lookup key during secret resolution
	- holding a simple reference to a sensitive payload value
	"""

	label: str
	value: None | T = Field(default=None, exclude=True) # Exclude from model_dump

	def __repr__(self):
		return f'NamedSecret(label={self.label!r})'

	def get(self) -> T:
		if self.value is None:
			raise ValueError("Secret not yet resolved")
		return self.value

	def set(self, arg: T) -> None:
		if self.value:
			raise ValueError("Secret already resolved")
		self.value = arg

	_vault: ClassVar["None | AmpelVault"] = None

	@model_validator(mode="after")
	def post_validate(self) -> "Self":
		if self._vault is not None:
			ValueType = (args[0]
				if ((args := self.get_model_args()) and isinstance(args[0], type))
				else object
			)
			if not self._vault.resolve_secret(self, ValueType):
				raise TypeError(f"Could not resolve secret {self.label!r} as {getattr(ValueType, '__name__', '<untyped>')}")
		return self

	@classmethod
	@contextlib.contextmanager
	def resolve_with(cls, vault: "None | AmpelVault") -> "Generator[None]":
		prev_vault = cls._vault
		try:
			cls._vault = vault
			yield
		finally:
			cls._vault = prev_vault
