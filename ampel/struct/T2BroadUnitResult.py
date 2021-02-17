#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/struct/T2BroadUnitResult.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 11.02.2021
# Last Modified Date: 17.02.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Optional, Dict, Any
from ampel.enum.T2RunState import T2RunState
from ampel.struct.JournalTweak import JournalTweak


class T2BroadUnitResult:
	"""
	Structure potentialy returned by Ampel T2 units to customize:
	- the T2Document status
	- the T2Record status
	- given keys (tag, status, extra) of the journal entry - from the associated transient document -
	created after a process is run (see JournalRecord `ampel.content.JournalRecord.JournalRecord`)
	"""

	__slots__ = "t2_rec_payload", "t2_doc_status", "t2_record_status", "stock_journal_tweak"

	def __init__(self,
		t2_rec_payload: Dict[str, Any],
		t2_doc_status: int = T2RunState.COMPLETED,
		t2_record_status: int = T2RunState.COMPLETED,
		stock_journal_tweak: Optional[JournalTweak] = None
	) -> None:
		"""
		:param t2_doc_status: integer status of the t2 document (T2Document)
		:param t2_record_status: integer status of the t2 record (T2Record)
		:param stock_journal_tweak: enable the customization of given keys (tag, status, extra)
		of the journal entry - from the associated transient document - created after a t2 process is run
		"""
		self.t2_rec_payload = t2_rec_payload
		self.t2_doc_status = t2_doc_status
		self.t2_record_status = t2_record_status
		self.stock_journal_tweak = stock_journal_tweak
