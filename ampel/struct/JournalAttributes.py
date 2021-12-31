#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/struct/JournalAttributes.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 15.10.2018
# Last Modified Date: 12.05.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Optional, Union, Any
from collections.abc import Sequence
from ampel.types import Tag
from ampel.content.JournalRecord import JournalRecord


class JournalAttributes:
	"""
	Structure potentialy used by Ampel units to customize
	the stock journal entry created after a process is run.
	"""

	__slots__ = 'tag', 'code', 'extra'

	#: code / status
	code: Optional[int]

	#: journal entry tag(s)
	tag: Optional[Union[Tag, Sequence[Tag]]]

	#: if provided, will be included as-is under the journal root key 'extra'
	extra: Optional[dict[str, Any]]


	def __init__(self,
		code: Optional[int] = None,
		tag: Optional[Union[Tag, Sequence[Tag]]] = None,
		extra: Optional[dict[str, Any]] = None
	) -> None:
		"""
		:param code: potential integer code of the executed process
		:param tag: journal entry tag(s)
		:param extra: optional dict, which if provided, will be included 'as is' under journal root key 'extra'
		Note regarding the type of extra: as of june 2020, mypy does not support recursive / json type
		-> https://github.com/python/mypy/issues/731
		"""
		self.tag = tag
		self.extra = extra
		self.code = code


	def dict(self) -> JournalRecord:
		d: JournalRecord = {}
		if self.tag:
			d['tag'] = self.tag
		if self.code:
			d['code'] = self.code
		if self.extra:
			d['extra'] = self.extra
		return d
			

	def into(self, prime: JournalRecord) -> JournalRecord:

		if self.code:
			prime['code'] = self.code

		if self.tag:
			prime['tag'] = self.tag

		if self.extra:
			if 'extra' in prime:
				prime['extra'] = self.extra | prime['extra']
			else:
				prime['extra'] = self.extra

		return prime
