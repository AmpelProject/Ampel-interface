#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/view/SnapView.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 13.01.2018
# Last Modified Date: 18.06.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from datetime import datetime
from typing import Dict, Optional, Union, Any, Literal, Sequence, Callable

from ampel.types import StockId, UBson
from ampel.struct.AmpelBuffer import AmpelBuffer
from ampel.content.DataPoint import DataPoint
from ampel.content.T1Document import T1Document
from ampel.content.T2Document import T2Document
from ampel.content.T3Document import T3Document
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
	:meth:`AbsT3Unit.process() <ampel.abstract.AbsT3Unit.AbsT3Unit.process>`.

	"""

	__slots__ = 'id', 'stock', 't0', 't1', 't2', 't3', 'logs', 'extra', '_frozen'

	stock: Optional[StockDocument] #: Stock record, if loaded
	t0: Optional[Sequence[DataPoint]] #: Datapoints, if loaded
	t1: Optional[Sequence[T1Document]] #: Compounds, if loaded
	t2: Optional[Sequence[T2Document]] #: T2 documents, if loaded
	t3: Optional[Sequence[T3Document]] #: T3 documents, if loaded
	logs: Optional[Sequence[LogDocument]] #: Logs, if added by T3 complement stage
	extra: Optional[Dict[str, Any]] #: Free-form, auxiliary information added by instances of :class:`~ampel.abstract.AbsBufferComplement.AbsBufferComplement`


	@classmethod
	def of(cls, ampel_buffer: AmpelBuffer) -> 'SnapView':
		return cls(**ampel_buffer)


	def __init__(self,
		id: StockId,
		stock: Optional[StockDocument] = None,
		t0: Optional[Sequence[DataPoint]] = None,
		t1: Optional[Sequence[T1Document]] = None,
		t2: Optional[Sequence[T2Document]] = None,
		t3: Optional[Sequence[T3Document]] = None,
		logs: Optional[Sequence[LogDocument]] = None,
		extra: Optional[Dict[str, Any]] = None,
		freeze: bool = True
	):
		self.stock = stock
		self.t0 = t0
		self.t1 = t1
		self.t2 = t2
		self.t3 = t3
		self.extra = extra
		self.logs = logs
		self.id = id
		self._frozen = freeze


	def freeze(self):
		if not self._frozen:
			self._frozen = True


	def __setattr__(self, k, v):
		if getattr(self, '_frozen', False):
			raise ValueError('SnapView is read only')
		object.__setattr__(self, k, v)


	def serialize(self) -> Dict:
		return {k: getattr(self, k) for k in self.__slots__}


	def get_t2_docs(self,
		unit_id: Optional[Union[int, str]] = None,
		link_id: Optional[int] = None
	) -> Optional[Sequence[T2Document]]:
		"""
		Get a subset of T2 documents.

		:param unit_id: limits the returned science record(s) to the one with the provided t2 unit id
		:param link_id: whether to return the latest science record(s) or not (default: False)

		"""

		if self.t2 is None:
			return None

		if link_id:

			if unit_id:
				return tuple(
					rec for rec in self.t2
					if rec['link'] == link_id and rec['unit'] == unit_id
				)

			return tuple(rec for rec in self.t2 if rec['link'] == link_id)

		if unit_id:
			return tuple(rec for rec in self.t2 if rec['unit'] == unit_id)

		return self.t2


	def get_t2_result(self,
		unit_id: Union[int, str],
		link_id: Optional[int] = None,
		code: Optional[Union[int]] = None
	) -> Optional[UBson]:
		"""
		Get latest result from a given unit.

		:param unit_id: target unit id
		:param link_id: restrict to a specific state
		"""

		# from the records that match the unit and compound selection,
		# return the last record that has a result
		for t2 in self.get_t2_docs(unit_id, link_id) or []:
			if code is not None and t2['code'] != code:
				continue
			for subrecord in reversed(t2.get('body') or []):
				if subrecord:
					return subrecord
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


	def get_time_updated(self,
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

		return 'DP: %i, CP: %i, T2: %i' % (
			len(view.t0) if view.t0 else 0,
			len(view.t1) if view.t1 else 0,
			len(view.t2) if view.t2 else 0
		)
