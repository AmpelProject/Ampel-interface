#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/alert/AmpelAlert.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 26.01.2020
# Last Modified Date: 25.05.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

import operator
from typing import Dict, Tuple, List, Sequence, Optional, Any, Callable, Union
from ampel.types import StockId

osa = object.__setattr__

# Do not enable customizations of operators by sub-classes for now
ops: Dict[str, Callable[[str, Any], bool]] = {
	'>': operator.gt,
	'<': operator.lt,
	'>=': operator.ge,
	'<=': operator.le,
	'==': operator.eq,
	'!=': operator.ne,
	'is': operator.is_,
	'is not': operator.is_not
}

def __ro__(self, *args, **kwargs):
	raise RuntimeError("Cannot modify AmpelAlert")


class AmpelAlert:

	__slots__ = 'id', 'stock_id', 'dps', 'new'
	__setattr__ = __ro__

	id: int #: unique identifier for this alert
	stock_id: StockId #: stock this alert belongs to
	dps: Sequence[Dict] #: datapoints


	def __init__(self, id: Union[int, str], stock_id: StockId, dps: Sequence[Dict]) -> None:
		osa(self, 'id', id)
		osa(self, 'stock_id', stock_id)
		osa(self, 'dps', dps)


	def __reduce__(self):
		return (type(self), (self.id, self.stock_id, self.dps))


	def get_values(self,
		key: str,
		filters: Optional[Sequence[Dict[str, Any]]] = None,
		data: Optional[Sequence[Dict]] = None
	) -> List[Any]:
		"""
		Example:
			
			get_values("magpsf")
		"""

		if not data:
			data = self.dps

		if filters:
			data = AmpelAlert.apply_filter(data, filters)

		return [el[key] for el in data if key in el]


	def get_tuples(self,
		key1: str, key2: str,
		filters: Optional[Sequence[Dict[str, Any]]] = None,
		data: Optional[Sequence[Dict]] = None
	) -> List[Tuple[Any, Any]]:
		"""
		Example::
			
			get_tuples("jd", "magpsf")
		"""

		if not data:
			data = self.dps

		if filters:
			data = AmpelAlert.apply_filter(data, filters)

		return [
			(el[key1], el[key2])
			for el in data if key1 in el and key2 in el
		]


	def get_ntuples(self,
		params: List[str],
		filters: Optional[Sequence[Dict[str, Any]]] = None,
		data: Optional[Sequence[Dict]] = None
	) -> List[Tuple]:
		"""
		Example:
			
			get_ntuples(["fid", "jd", "magpsf"])
		"""

		if not data:
			data = self.dps

		if filters:
			data = AmpelAlert.apply_filter(data, filters)

		return [
			tuple(el[param] for param in params)
			for el in data if all(param in el for param in params)
		]


	def is_new(self) -> bool:
		return len(self.dps) == 1


	def dict(self) -> Dict[str, Any]:
		return {'id': self.id, 'stock_id': self.stock_id, 'dps': self.dps}


	@staticmethod
	def apply_filter(
		dicts: Sequence[Dict],
		filters: Sequence[Dict[str, Any]]
	) -> Sequence[Dict]:

		if isinstance(filters, dict):
			filters = [filters]
		else:
			if filters is None or not isinstance(filters, (list, tuple)):
				raise ValueError("Parameter 'filters' must be a dict or a sequence of dicts")

		for f in filters:
			op = ops[f['operator']]
			f_attr = f['attribute']
			f_val = f['value']
			dicts = [d for d in dicts if f_attr in d and op(d[f_attr], f_val)]

		return dicts
