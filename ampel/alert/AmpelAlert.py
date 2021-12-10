#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/alert/AmpelAlert.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 26.01.2020
# Last Modified Date: 08.12.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

import operator
from typing import Dict, Tuple, Sequence, Optional, Any, Callable, Union
from ampel.types import StockId, Tag

# Do not enable customizations of operators by sub-classes for now
ops: dict[str, Callable[[str, Any], bool]] = {
	'>': operator.gt,
	'<': operator.lt,
	'>=': operator.ge,
	'<=': operator.le,
	'==': operator.eq,
	'!=': operator.ne,
	'is': operator.is_,
	'is not': operator.is_not,
	'contains': operator.contains,
	'exists': None, # type: ignore
}


class AmpelAlert:
	"""
	Implements AmpelAlertProtocol
	"""

	__slots__ = '_id', '_stock', '_datapoints', '_tag', '_extra'

	def __init__(self,
		id: int, #: unique identifier for this alert
		stock: StockId, #: stock this alert belongs to
		datapoints: Sequence[dict[str, Any]],
		tag: Optional[Union[Tag, list[Tag]]] = None, #: Optional tag associated with this alert
		extra: Optional[dict[str, Any]] = None #: Optional information associated with this alert
	) -> None:
		sa = object.__setattr__
		sa(self, '_id', id)
		sa(self, '_stock', stock)
		sa(self, '_datapoints', datapoints)
		sa(self, '_tag', tag)
		sa(self, '_extra', extra)

	@property
	def id(self) -> int:
		return self._id # type: ignore[attr-defined]

	@property
	def stock(self) -> StockId:
		return self._stock # type: ignore[attr-defined]

	@property
	def datapoints(self) -> Sequence[dict[str, Any]]:
		return self._datapoints # type: ignore[attr-defined]

	@property
	def tag(self) -> Union[None, Tag, list[Tag]]:
		return self._tag # type: ignore[attr-defined]

	@property
	def extra(self) -> Optional[dict[str, Any]]:
		return self._extra # type: ignore[attr-defined]

	def __reduce__(self):
		return (
			type(self),
			(self._id, self._stock, self._datapoints, self._tag, self._extra)
		)

	def __setattr__(self, k, v):
		raise ValueError("AmpelAlert is read only")

	def __delattr__(self, k):
		raise ValueError("AmpelAlert is read only")


	def get_values(self,
		key: str,
		filters: Optional[Sequence[dict[str, Any]]] = None
	) -> list[Any]:
		"""
		Example:
			
			get_values("magpsf")
		"""
		data = self.apply_filter(self.datapoints, filters) if filters else self.datapoints
		return [el[key] for el in data if key in el]


	def get_tuples(self,
		key1: str, key2: str,
		filters: Optional[Sequence[dict[str, Any]]] = None
	) -> list[Tuple[Any, Any]]:
		"""
		Example::
			
			get_tuples("jd", "magpsf")
		"""
		data = self.apply_filter(self.datapoints, filters) if filters else self.datapoints
		return [
			(el[key1], el[key2])
			for el in data if key1 in el and key2 in el
		]


	def get_ntuples(self,
		params: list[str], filters: Optional[Sequence[dict[str, Any]]] = None
	) -> list[Tuple]:
		"""
		Example:
			
			get_ntuples(["fid", "jd", "magpsf"])
		"""
		data = self.apply_filter(self.datapoints, filters) if filters else self.datapoints
		return [
			tuple(el[param] for param in params)
			for el in data if all(param in el for param in params)
		]


	def is_new(self) -> bool:
		return len(self.datapoints) == 1


	def dict(self) -> dict[str, Any]:
		return {
			'id': self.id,
			'stock': self.stock,
			'datapoints': self.datapoints,
			'extra': self.extra,
		}


	def apply_filter(self,
		dicts: Sequence[Dict[str, Any]],
		filters: Sequence[Dict[str, Any]]
	) -> Sequence[Dict[str, Any]]:

		if isinstance(filters, dict):
			filters = [filters]
		else:
			if filters is None or not isinstance(filters, (list, tuple)):
				raise ValueError("Parameter 'filters' must be a dict or a sequence of dicts")

		for f in filters:
			attr = f['attribute']
			op = f['operator']
			if op == 'exists':
				if f['value'] is True:
					dicts = [d for d in dicts if attr in d]
				else:
					dicts = [d for d in dicts if attr not in d]
			else:
				dicts = [d for d in dicts if attr in d and ops[op](d[attr], f['value'])]

		return dicts
