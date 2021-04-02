#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/struct/T2BroadUnitResult.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 11.02.2021
# Last Modified Date: 02.04.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Optional, Dict, Any, Union, List
from ampel.enum.T2RunState import T2RunState
from ampel.struct.JournalTweak import JournalTweak

Tag = Union[int, str]

class T2BroadUnitResult:
	"""
	Structure potentialy returned by Ampel T2 units to customize:
	
	- :attr:`T2Document.status <ampel.content.T2Document.T2Document.status>`
	- :attr:`T2Document.tag <ampel.content.T2Document.T2Document.tag>`
	- :attr:`T2Record.status <ampel.content.T2Record.T2Record.status>`
	- given keys (tag, status, extra) of the journal entry, from the associated transient document,
	  created after a process is run (see :class:`~ampel.content.JournalRecord.JournalRecord`)
	"""

	__slots__ = "rec_payload", "rec_status", "doc_status", "doc_tag", "stock_journal_tweak"

	def __init__(self,
		rec_payload: Dict[str, Any],
		rec_status: int = T2RunState.COMPLETED,
		doc_status: int = T2RunState.COMPLETED,
		doc_tag: Optional[Union[Tag, List[Tag]]] = None,
		stock_journal_tweak: Optional[JournalTweak] = None
	) -> None:
		"""
		:param doc_status:
		:param rec_status: integer status of the t2 record (T2Record)
		:param stock_journal_tweak: enable the customization of given keys (tag, status, extra)
		of the journal entry - from the associated transient document - created after a t2 process is run
		"""
		#: result of unit invocation
		self.rec_payload = rec_payload

		#: integer status of the associated :class:`~ampel.content.T2Record.T2Record`
		#: with the current invocation of this unit
		self.rec_status = rec_status

		#: integer status of the :class:`~ampel.content.T2Document.T2Document`
		#: associated with all invocations of this unit
		self.doc_status = doc_status

		#: tag(s) to be added to :class:`~ampel.content.T2Document.T2Document`
		self.doc_tag = doc_tag

		#: extra items to add to the :class:`~ampel.content.JournalRecord.JournalRecord`
		#: associated with the current invocation of this unit
		self.stock_journal_tweak = stock_journal_tweak
