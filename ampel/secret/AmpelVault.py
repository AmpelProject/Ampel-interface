#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/secret/AmpelVault.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 21.06.2021
# Last Modified Date: 22.06.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Any, List, Optional, Type, overload
from ampel.abstract.AbsSecretProvider import AbsSecretProvider
from ampel.abstract.Secret import Secret, T
from ampel.secret.NamedSecret import NamedSecret


class AmpelVault:
	""" Collection of secret providers """

	def __init__(self, providers: List[AbsSecretProvider]) -> None:
		self.providers = providers

	def resolve_secret(self, secret: Secret, ValueType: Type) -> bool:

		for sp in self.providers:
			if sp.tell(secret, ValueType):
				return True
		return False

	@overload
	def get_named_secret(self, label: str) -> Optional[NamedSecret[Any]]:
		...
	
	@overload
	def get_named_secret(self, label: str, ValueType: Type[T]) -> Optional[NamedSecret[T]]:
		...
	
	def get_named_secret(self, label, ValueType=object):
		""" Returns a resolved NamedSecret using provided label """
		ns: NamedSecret = NamedSecret(label=label)
		if self.resolve_secret(ns, ValueType):
			return ns
		return None
