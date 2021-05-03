#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/struct/JournalAttributes.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 15.10.2018
# Last Modified Date: 03.05.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Dict, Optional, Sequence, Union, Any
from ampel.type import Tag


class JournalAttributes:
	"""
	Structure potentialy returned by Ampel units to customize
	the stock journal entry created after a process is run.
	"""

	__slots__ = 'tag', 'code', 'extra'

	#: code / status
	code: Optional[int]

	#: journal entry tag(s)
	tag: Optional[Union[Tag, Sequence[Tag]]]

	#: if provided, will be included as-is under the journal root key 'extra'
	extra: Optional[Dict[str, Any]]

	def __init__(self,
		code: Optional[int] = None,
		tag: Optional[Union[Tag, Sequence[Tag]]] = None,
		extra: Optional[Dict[str, Any]] = None
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
