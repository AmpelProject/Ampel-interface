#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/view/SnapView.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 13.01.2018
# Last Modified Date: 09.06.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from datetime import datetime
from typing import Dict, Optional, Union, Any, Literal, Sequence

from ampel.type import StockId
from ampel.content.DataPoint import DataPoint
from ampel.content.Compound import Compound
from ampel.content.T2Record import T2Record
from ampel.content.StockRecord import StockRecord
from ampel.content.LogRecord import LogRecord
from ampel.content.JournalRecord import JournalRecord


class SnapView:
	"""
	View of a given ampel object (with unique stock id).
	This class references various instances of objects from
	package ampel.content, originating from different ampel tiers.
	It can also contain external/composite objects embedded in the dict called 'extra'
	(such as spectra or ampel.view.LightCurve instances for ex.)
	The config parameter of a T3 process determines which information are included.
	Typically, instances of this class (or of subclass such as TransientView) are provided to T3 units.
	"""

	__slots__ = "id", "stock", "t0", "t1", "t2", "log", "extra"


	def __init__(self,
		id: StockId,
		stock: Optional[StockRecord] = None,
		t0: Optional[Sequence[DataPoint]] = None,
		t1: Optional[Sequence[Compound]] = None,
		t2: Optional[Sequence[T2Record]] = None,
		log: Optional[Sequence[LogRecord]] = None,
		extra: Optional[Dict[str, Any]] = None
	):
		self.stock = stock
		self.t0 = t0
		self.t1 = t1
		self.t2 = t2
		self.log = log
		self.extra = extra
		self.id = id


	def __setattr__(self, k, v):
		if hasattr(self, "id"):
			raise ValueError("SnapView is read only")
		object.__setattr__(self, k, v)


	def serialize(self) -> Dict:
		return {k: getattr(self, k) for k in self.__slots__}


	def get_t2_records(self,
		unit_id: Optional[Union[int, str]] = None,
		compound_id: Optional[bytes] = None
	) -> Optional[Sequence[T2Record]]:
		"""
		:param unit_id: limits the returned science record(s) to the one with the provided t2 unit id
		:param compound_id: whether to return the latest science record(s) or not (default: False)
		"""

		if self.t2 is None:
			return None

		if compound_id:

			if unit_id:
				return tuple(
					rec for rec in self.t2
					if rec['link'] == compound_id and rec['unit'] == unit_id
				)

			return tuple(rec for rec in self.t2 if rec['link'] == compound_id)

		if unit_id:
			return tuple(rec for rec in self.t2 if rec['unit'] == unit_id)

		return self.t2


	def get_journal_entries(self,
		tier: Optional[Literal[0, 1, 2, 3]] = None,
		process_name: Optional[str] = None,
		latest: bool = False
	) -> Optional[Union[JournalRecord, Sequence[JournalRecord]]]:
		"""
		:param process_name: return only journal entries associated with a given process name
		:param last: return only the latest entry in the journal (the latest in time)
		Returns journal entries corresponding to a given tier and/or job.
		"""

		if not self.stock:
			return None

		entries = self.stock['journal']

		if tier:
			entries = tuple(j for j in self.stock['journal'] if j['tier'] == tier)

		if process_name:
			entries = tuple(j for j in entries if j['process'] == process_name)

		if latest:
			return sorted(entries, key=lambda x: x['ts'])[-1]

		return entries


	def get_time_created(self,
		output: Literal['raw', 'datetime', 'str'] = 'raw'
	) -> Optional[Union[float, datetime, str]]:
		""" """
		if not self.stock:
			return None
		# Note: journal cannot be empty
		return self._get_time(self.stock['journal'][0], output)


	def get_time_modified(self,
		output: Literal['raw', 'datetime', 'str'] = 'raw'
	) -> Optional[Union[float, datetime, str]]:
		""" """
		if not self.stock:
			return None
		# Note: journal cannot be empty
		return self._get_time(self.stock['journal'][-1], output)


	@classmethod
	def _get_time(cls,
		entry: JournalRecord,
		output: Optional[Union[bool, str]] = None
	) -> Union[float, str, datetime]:
		""" """
		if output == 'raw':
			return entry['ts']

		dt = datetime.fromtimestamp(entry['ts'])

		if output == 'datetime':
			return dt

		return dt.strftime('%d/%m/%Y %H:%M:%S')


	@staticmethod
	def content_summary(view: 'SnapView') -> str:

		return "DP: %i, CP: %i, T2: %i" % (
			len(view.t0) if view.t0 else 0,
			len(view.t1) if view.t1 else 0,
			len(view.t2) if view.t2 else 0
		)
