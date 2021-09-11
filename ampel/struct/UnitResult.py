#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/struct/UnitResult.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 04.05.2021
# Last Modified Date: 11.09.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Optional, Union, Sequence
from ampel.types import UBson, Tag
from ampel.struct.JournalAttributes import JournalAttributes


class UnitResult:
	"""
	Structure potentialy returned by Ampel units to customize
	document body, code, tag or the stock journal entry.
	"""

	__slots__ = 'body', 'tag', 'code', 'journal'

	def __init__(self,
		body: UBson = None,
		tag: Optional[Union[Tag, Sequence[Tag]]] = None,
		code: Optional[int] = None,
		journal: Optional[JournalAttributes] = None
	) -> None:
		"""
		:param body: content for the field 'body' of the associated tier document
		:param tag: tag(s) to be added to the content of the field 'tag' of the associated tier document.
		Note that tags are 'public' attributes (they are not channel bound) and as such, they:
		- are visible by any projection
		- can be used for any db queries
		:param code: customize 'code' of the associated tier document:
		- Either a member of `ampel.enum.DocumentCode` such as DocumentCode.RERUN_REQUESTED (negative values)
		- Or any positive integer number (custom defined for a particular ampel unit)
		:param journal: customization of the journal entry associated with the stock document
		"""
		self.body = body
		self.tag = tag
		self.code = code
		self.journal = journal
