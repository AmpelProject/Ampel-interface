#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-core/ampel/secret/AESecret.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 20.06.2021
# Last Modified Date: 20.06.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Optional
from pydantic import BaseModel
from ampel.secret.Secret import Secret


class AESecret(Secret[str], BaseModel):
	"""
	AES encrypted secret.

	To create an encrypted secret, please:
	- go to https://bitwiseshiftleft.github.io/sjcl/demo/
	- enter the shared password in the green box
	- enter the secret message (authtoken for example) in the red box
	- leave authenticated data empty
	- in "Cipher Parameters", check the option CCM. (OCB2 will *not* work)
	- click on the red arrow "encrypt"
	- copy the "Ciphertext" JSON dict
	- use it in your config (section 'secrets')

	Make sure the 'shared password' used in step 2 is known to us.
	"""

	iv: str
	v: int
	iter: int
	ks: int
	ts: int
	mode: str
	adata: str
	cipher: str
	salt: str
	ct: str

	value: Optional[str]

	def __repr__(self):
		return '<AESecret>'

	def set(self, value: str) -> None:
		self.value = value

	def get(self) -> str:
		if self.value is None:
			raise ValueError("AES payload not decrypted yet")
		return self.value
