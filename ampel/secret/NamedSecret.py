#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/secret/NamedSecret.py
# License           : BSD-3-Clause
# Author            : Jakob van Santen <jakob.van.santen@desy.de>
# Date              : 14.08.2020
# Last Modified Date: 20.06.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Optional
from ampel.secret.Secret import Secret, T
from pydantic import BaseModel


class NamedSecret(Secret[T], BaseModel):
	"""
	A Secret:
	- featuring a label used as lookup key during secret resolution
	- holding a simple reference to a sensitive payload value
	"""

	label: str
	value: Optional[T] = None

	def __repr__(self):
		return '<NamedSecret>'

	def get(self) -> T:
		if self.value is None:
			raise ValueError("Secret not yet resolved")
		return self.value

	def set(self, arg: T) -> None:
		if self.value:
			raise ValueError("Secret already resolved")
		self.value = arg
