#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/struct/UnitResult.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 04.05.2021
# Last Modified Date: 17.06.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Optional
from ampel.types import UBson
from ampel.struct.JournalAttributes import JournalAttributes


class UnitResult:
	"""
	Structure potentialy returned by Ampel units to customize
	document code, meta or the stock journal entry.
	"""

	__slots__ = 'body', 'code', 'journal'

	def __init__(self,
		body: UBson = None,
		code: Optional[int] = None,
		journal: Optional[JournalAttributes] = None
	) -> None:
		"""
		:param body: content for the field 'body'  of the associated tier document
		:param code: customize DocumentCode (ex: DocumentCode.RERUN_REQUESTED or any int)
		:param journal: customization of the journal entry associated with the stock document
		"""
		self.body = body
		self.code = code
		self.journal = journal
