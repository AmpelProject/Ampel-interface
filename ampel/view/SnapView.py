#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/view/SnapView.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 13.01.2018
# Last Modified Date: 16.02.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from datetime import datetime
from typing import Dict, Optional, Union, Any, Literal, Sequence, Callable

from ampel.type import StockId
from ampel.content.DataPoint import DataPoint
from ampel.content.Compound import Compound
from ampel.content.T2Document import T2Document
from ampel.content.StockDocument import StockDocument
from ampel.content.LogDocument import LogDocument
from ampel.content.JournalRecord import JournalRecord


class SnapView:
	"""
	View of a given ampel object (with unique stock id).

	This class references various instances of objects from
	package ampel.content, originating from different ampel tiers.
	It can also contain external/composite objects embedded in the dict called 'extra',
	for example spectra or cutout images.
	The config parameter of a T3 process determines which information are included.
	Instances of this class (or of subclass such as
	:class:`~ampel.view.TransientView.TransientView`) are provided to
	:meth:`AbsT3Unit.add() <ampel.abstract.AbsT3Unit.AbsT3Unit.add>`.

	"""

	__slots__ = "id", "stock", "t0", "t1", "t2", "log", "extra", "_frozen"

	stock: Optional[StockDocument] #: Stock record, if loaded
	t0: Optional[Sequence[DataPoint]] #: Datapoints, if loaded
	t1: Optional[Sequence[Compound]] #: Compounds, if loaded
	t2: Optional[Sequence[T2Document]] #: T2 documents, if loaded
	log: Optional[Sequence[LogDocument]] #: Event logs, if loaded
	extra: Optional[Dict[str, Any]] #: Free-form, auxiliary information added by instances of :class:`~ampel.t3.complement.AbsT3DataAppender.AbsT3DataAppender`

	def __init__(self,
		id: StockId,
		stock: Optional[StockDocument] = None,
		t0: Optional[Sequence[DataPoint]] = None,
		t1: Optional[Sequence[Compound]] = None,
		t2: Optional[Sequence[T2Document]] = None,
		log: Optional[Sequence[LogDocument]] = None,
		extra: Optional[Dict[str, Any]] = None,
		freeze: bool = True
	):
		self.stock = stock
		self.t0 = t0
		self.t1 = t1
		self.t2 = t2
		self.log = log
		self.extra = extra
		self.id = id
		self._frozen = freeze


	def freeze(self):
		if not self._frozen:
			self._frozen = True


	def __setattr__(self, k, v):
		if getattr(self, "_frozen", False):
			raise ValueError("SnapView is read only")
		object.__setattr__(self, k, v)


	def serialize(self) -> Dict:
		return {k: getattr(self, k) for k in self.__slots__}


	def get_t2_docs(self,
		unit_id: Optional[Union[int, str]] = None,
		compound_id: Optional[bytes] = None
	) -> Optional[Sequence[T2Document]]:
		"""
		Get a subset of T2 documents.

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


	def get_t2_result(self,
		unit_id: Union[int, str],
		compound_id: Optional[bytes] = None
	) -> Optional[Dict[str, Any]]:
		"""
		Get the latest result from the given unit.

		:param unit_id: target unit id
		:param compound_id: restrict to a specific state
		"""

		# from the records that match the unit and compound selection,
		# return the last record that has a result
		for t2 in reversed(self.get_t2_docs(unit_id, compound_id) or []):
			for subrecord in reversed(t2.get("body") or []):
				if "result" in subrecord and subrecord["status"] >= 0:
					result = subrecord["result"]
					if isinstance(result, dict):
						return result
					elif isinstance(result, list) and len(result):
						return result[-1]
		return None


	def get_journal_entries(self,
		tier: Optional[Literal[0, 1, 2, 3]] = None,
		process_name: Optional[str] = None,
		filter_func: Optional[Callable[[JournalRecord], bool]] = None,
	) -> Optional[Sequence[JournalRecord]]:
		"""
		Get a subset of journal entries.

		:param tier: return only journal entries associated with the given tier
		:param process_name: return only journal entries associated with a given process name
		:param latest: return only the latest entry in the journal (the latest in time)

		:returns:
			journal entries corresponding to a given tier and/or job,
			sorted by timestamp.
		"""

		if not self.stock:
			return None

		entries = self.stock['journal']

		if tier is not None:
			entries = tuple(j for j in entries if j['tier'] == tier)

		if process_name is not None:
			entries = tuple(j for j in entries if j['process'] == process_name)

		if filter_func is not None:
			entries = tuple(j for j in entries if filter_func(j))

		return sorted(entries, key=lambda x: x['ts'])


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
