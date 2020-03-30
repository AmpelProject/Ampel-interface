#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/view/SnapView.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 13.01.2018
# Last Modified Date: 12.02.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from datetime import datetime
from dataclasses import dataclass
from typing import Dict, Optional, Union, Any, Literal, Sequence

from ampel.types import StockId
from ampel.content.DataPoint import DataPoint
from ampel.content.Compound import Compound
from ampel.content.T2Record import T2Record
from ampel.content.StockRecord import StockRecord
from ampel.content.LogRecord import LogRecord
from ampel.view.BaseView import BaseView


@dataclass(frozen=True)
class SnapView(BaseView):
	"""
	View of a given ampel object (with unique stock id).
	This class links various instances, mostly from ampel.content,
	possibly originating from different ampel tiers.
	It can also contain external/composite objects in the dict called 'extra'
	(such as spectra or ampel.view.LightCurve instances for ex.)
	The config parameters of a T3 process determines which information are present or not.
	Typically, instances of this class (or of a sub-class such as TransientView) are provided to T3 modules.
	"""

	id: StockId
	stock: Optional[StockRecord] = None
	t0: Optional[Sequence[DataPoint]] = None
	t1: Optional[Sequence[Compound]] = None
	t2: Optional[Sequence[T2Record]] = None
	logs: Optional[Sequence[LogRecord]] = None
	extra: Optional[Dict[str, Any]] = None


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
	) -> Optional[Union[Dict[str, Any], Sequence[Dict[str, Any]]]]:
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
			entries = tuple(j for j in entries if j['name'] == process_name)

		if latest:
			return sorted(entries, key=lambda x: x['dt'])[-1]

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
		entry: Dict[str, Any],
		output: Optional[Union[bool, str]] = None
	) -> Union[float, str, datetime]:
		""" """
		if output == 'raw':
			return entry['dt']

		dt = datetime.fromtimestamp(entry['dt'])

		if output == 'datetime':
			return dt

		return dt.strftime('%d/%m/%Y %H:%M:%S')


	@staticmethod
	def content_summary(view: 'SnapView') -> str:
		""" """
		return "DP: %i, CP: %i, T2: %i" % (
			len(view.t0) if view.t0 else 0,
			len(view.t1) if view.t1 else 0,
			len(view.t2) if view.t2 else 0
		)
