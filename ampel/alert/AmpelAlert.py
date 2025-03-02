#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/alert/AmpelAlert.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                26.01.2020
# Last Modified Date:  02.01.2022
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

import operator
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any

from ampel.types import JDict, StockId, Tag

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
	'exists': None, # type: ignore[dict-item]
}


@dataclass(frozen=True, slots=True)
class AmpelAlert:
	"""
	Implements AmpelAlertProtocol
	"""

	id: int #: unique identifier for this alert
	stock: StockId #: stock this alert belongs to
	datapoints: Sequence[JDict]
	tag: None | Tag | list[Tag] = None #: Optional tag associated with this alert
	extra: None | JDict = None #: Optional information associated with this alert

	def __hash__(self) -> int:
		return id(self)

	def get_values(self,
		key: str,
		filters: None | Sequence[JDict] = None
	) -> list[Any]:
		"""
		Example:
			
			get_values("magpsf")
		"""
		data = self.apply_filter(self.datapoints, filters) if filters else self.datapoints
		return [el[key] for el in data if key in el]


	def get_tuples(self,
		key1: str, key2: str,
		filters: None | Sequence[JDict] = None
	) -> list[tuple[Any, Any]]:
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
		params: list[str],
		filters: None | Sequence[JDict] = None
	) -> list[tuple]:
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


	def apply_filter(self,
		dicts: Sequence[JDict],
		filters: Sequence[JDict]
	) -> Sequence[JDict]:

		if isinstance(filters, dict):
			filters = [filters]
		elif filters is None or not isinstance(filters, list | tuple):
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


	def dict(self) -> JDict:
		return {
			'id': self.id,
			'stock': self.stock,
			'datapoints': self.datapoints,
			'extra': self.extra,
		}
