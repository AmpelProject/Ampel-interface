#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/view/T2DocView.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 10.02.2021
# Last Modified Date: 11.02.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from datetime import datetime
from typing import Dict, Optional, Union, Any, Sequence, Literal, overload
from ampel.type import StockId
from ampel.content.T2Document import T2Link
from ampel.content.T2Record import T2Record

TYPE_POINT_T2 = 0 # linked with datapoints, that is with tier 0
TYPE_STATE_T2 = 1 # linked with compounds, that is with tier 1
TYPE_STOCK_T2 = 3 # linked with stock document


class T2DocView:
	"""
	View of a given T2Document (with unique stock id).
	Note: not implementing a static constructor method accepting T2Record
	as argument here to avoid a dependency on pymongo.
	"""

	__slots__ = "unit", "config", "link", "stock", "status", "created", "t2_type", "body", "_frozen"

	stock: StockId
	unit: Union[int, str]
	config: Optional[Dict[str, Any]]
	link: Union[T2Link, Sequence[T2Link]]
	status: int
	t2_type: int
	created: float
	body: Optional[Sequence[T2Record]]


	def __init__(self,
		stock: StockId,
		unit: Union[int, str],
		link: Union[T2Link, Sequence[T2Link]],
		status: int,
		t2_type: int,
		created: float,
		config: Optional[Dict[str, Any]] = None,
		body: Optional[Sequence[T2Record]] = None,
		freeze: bool = True
	):
		self.stock = stock
		self.unit = unit
		self.link = link
		self.status = status
		self.body = body
		self.config = config
		self.created = created
		self.t2_type = t2_type
		self._frozen = freeze


	def freeze(self):
		if not self._frozen:
			self._frozen = True


	def __setattr__(self, k, v):
		if getattr(self, "_frozen", False):
			raise ValueError("SnapView is read only")
		object.__setattr__(self, k, v)


	def serialize(self) -> Dict[str, Any]:
		return {k: getattr(self, k) for k in self.__slots__ if k != '_frozen'}


	def has_payload(self) -> bool:
		return self.body is not None and len(self.body) > 0


	def get_payload(self) -> Optional[Dict[str, Any]]:
		"""
		:returns: The payload (key: 'result') of the first T2Record found with status >= 0
		from the list of t2 records in reversed chronological order
		"""

		if not self.has_payload():
			return None

		for el in reversed(self.body): # type: ignore # inadequate mypy inference
			if 'result' in el and el['status'] >= 0:
				result = el['result']
				if isinstance(result, dict):
					return result
				elif isinstance(result, list) and len(result):
					return result[-1]

		return None


	def get_records(self) -> Optional[Sequence[T2Record]]:
		return self.body if self.has_payload() else None # type: ignore # inadequate mypy inference


	def is_point_type(self) -> bool:
		return self.t2_type == TYPE_POINT_T2


	def is_stock_type(self) -> bool:
		return self.t2_type == TYPE_STOCK_T2


	def is_state_type(self) -> bool:
		return self.t2_type == TYPE_STATE_T2


	@overload
	def get_time_created(self, to_string: Literal[False]) -> Optional[float]:
		...
	@overload
	def get_time_created(self, to_string: Literal[True]) -> Optional[str]:
		...
	def get_time_created(self, to_string: bool = False) -> Optional[Union[float, str]]:

		if to_string:
			return datetime.fromtimestamp(self.created).strftime('%d/%m/%Y %H:%M:%S')

		return self.created


	@overload
	def get_time_modified(self, to_string: Literal[False]) -> Optional[float]:
		...
	@overload
	def get_time_modified(self, to_string: Literal[True]) -> Optional[str]:
		...
	def get_time_modified(self, to_string: bool = False) -> Optional[Union[float, str]]:

		if not self.has_payload():
			return None

		ts = self.body[-1]['ts'] # type: ignore # inadequate mypy inference
		if to_string:
			dt = datetime.fromtimestamp(ts)
			return dt.strftime('%d/%m/%Y %H:%M:%S')

		return ts
