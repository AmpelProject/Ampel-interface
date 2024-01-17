#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/secret/AmpelVault.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                21.06.2021
# Last Modified Date:  22.06.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from typing import Any, overload

from ampel.abstract.AbsSecretProvider import AbsSecretProvider
from ampel.secret.NamedSecret import NamedSecret
from ampel.secret.Secret import Secret, T


class AmpelVault:
	""" Collection of secret providers """

	def __init__(self, providers: list[AbsSecretProvider]) -> None:
		self.providers = providers

	def resolve_secret(self, secret: Secret, ValueType: type) -> bool:
		return any(sp.tell(secret, ValueType) for sp in self.providers)

	@overload
	def get_named_secret(self, label: str) -> None | NamedSecret[Any]:
		...
	
	@overload
	def get_named_secret(self, label: str, ValueType: type[T]) -> None | NamedSecret[T]:
		...
	
	def get_named_secret(self, label, ValueType=object):
		""" Returns a resolved NamedSecret using provided label """
		ns = NamedSecret[ValueType](label=label) # type: ignore[valid-type]
		if self.resolve_secret(ns, ValueType):
			return ns
		return None
