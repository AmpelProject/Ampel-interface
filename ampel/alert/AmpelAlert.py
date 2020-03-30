#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/alert/AmpelAlert.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 26.01.2020
# Last Modified Date: 05.02.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

import operator
from dataclasses import dataclass
from typing import Dict, Tuple, List, Sequence, Optional, Any, ClassVar, Set, Callable, Union
from ampel.types import StockId

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

@dataclass(frozen=True)
class AmpelAlert:
	""" """

	_kw_mappings: ClassVar[Dict[str, str]]
	# static set is populated by __init_subclass__
	_kws_set: ClassVar[Set[str]]

	stock_id: StockId
	id: Union[int, str]

	# pylint: disable=unused-argument
	def __init_subclass__(cls, **kwargs):
		super().__init_subclass__(**kwargs)
		if hasattr(cls, "_kw_mappings") and cls._kw_mappings is not None:
			# Build set to optimize perf
			cls._kws_set = set(cls._kw_mappings.keys())
		else:
			cls._kws_set = set()


	def get_values(self,
		param_name: str,
		# datapoints: Sequence[Dict],
		field: str,
		filters: Optional[Sequence[Dict[str, Any]]] = None
	) -> List[Any]:
		""" ex: get_values("mag") """

		if param_name in self._kws_set:
			param_name = self._kw_mappings[param_name]

		dps = self.apply_filter(getattr(self, field), filters) if filters else getattr(self, field)
		return [el[param_name] for el in dps if param_name in el]


	def get_tuples(self,
		param1: str, param2: str, field: str,
		filters: Optional[Sequence[Dict[str, Any]]] = None
	) -> List[Tuple[Any, Any]]:
		""" ex: get_tuples("obs_date", "mag") """

		if param1 in self._kws_set:
			param1 = self._kw_mappings[param1]

		if param2 in self._kws_set:
			param2 = self._kw_mappings[param2]

		dps = self.apply_filter(getattr(self, field), filters) if filters else getattr(self, field)

		return [
			(el[param1], el[param2])
			for el in dps if param1 in el and param2 in el
		]


	def get_ntuples(self,
		params: List[str], field: str,
		filters: Optional[Sequence[Dict[str, Any]]] = None
	) -> List[Tuple]:
		""" ex: get_ntuples(["fid", "obs_date", "mag"]) """

		# If any of the provided parameter matches defined keyword mappings
		if self._kws_set & set(params):
			params = params.copy()
			for i, param in enumerate(params):
				if param in self._kws_set:
					params[i] = self._kw_mappings[param]

		dps = self.apply_filter(getattr(self, field), filters) if filters else getattr(self, field)

		return [
			tuple(el[param] for param in params)
			for el in dps if all(param in el for param in params)
		]


	@classmethod
	def apply_filter(cls,
		dicts: Sequence[Dict],
		filters: Sequence[Dict[str, Any]]
	) -> Sequence[Dict]:
		"""
		"""

		if isinstance(filters, dict):
			filters = [filters]
		else:
			if filters is None or not isinstance(filters, (list, tuple)):
				raise ValueError("Filters must be dicts or list/tuple of dict")

		for filtre in filters:

			op = ops[filtre['operator']]
			filter_attr_name = filtre['attribute']
			attr_name = (
				filter_attr_name if filter_attr_name not in cls._kws_set
				else cls._kw_mappings[filter_attr_name]
			)

			dicts = [
				d for d in dicts
				if attr_name in d and op(d[attr_name], filtre['value'])
			]

		return dicts
