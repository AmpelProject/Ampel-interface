#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsSecretProvider.py
# License           : BSD-3-Clause
# Author            : Jakob van Santen <jakob.van.santen@desy.de>
# Date              : 14.08.2020
# Last Modified Date: 21.06.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Type
from ampel.abstract.Secret import Secret
from ampel.base.AmpelABC import AmpelABC
from ampel.base.decorator import abstractmethod


class AbsSecretProvider(AmpelABC, abstract=True):
	"""
	Interface to a secret store used to resolve secrets.
	The underlying store may be as simple as a dict loaded from a JSON file
	or a complete key manager like Vault.
	"""

	@abstractmethod
	def tell(self, arg: Secret, ValueType: Type) -> bool:
		"""
		Potentially update an initialized Secret instance with
		the actual sensitive information associable with it.
		:returns: True if the Secret was told/resolved or False
		if the provided Secret is either unknown to this secret
		provider, or resolves to a value of the wrong type.
		"""
