#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/view/T2DocView.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                10.02.2021
# Last Modified Date:  01.12.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from datetime import datetime
from typing import Any, Literal, overload
from collections.abc import Sequence
from ampel.types import StockId, UBson, T2Link, Tag, T
from ampel.content.MetaRecord import MetaRecord
from ampel.content.T2Document import T2Document
from ampel.config.AmpelConfig import AmpelConfig

TYPE_POINT_T2 = 0 # linked with datapoints, that is with tier 0
TYPE_STATE_T2 = 1 # linked with compounds, that is with tier 1
TYPE_STOCK_T2 = 3 # linked with stock document


class T2DocView:
	"""
	View of a given T2Document (with unique stock id).
	A t2 view contains read-only information from a T2Document
	and provides convenience methods to access it.
	"""

	__slots__ = 'unit', 'config', 'link', 'stock', 'tag', 'code', 'meta', 't2_type', 'body'

	stock: StockId | Sequence[StockId]
	unit: int | str
	config: None | dict[str, Any]
	link: T2Link
	tag: Sequence[Tag]
	code: int
	t2_type: int
	meta: Sequence[MetaRecord]
	body: None | Sequence[UBson]


	@classmethod # Static ctor
	def of(cls, doc: T2Document, conf: None | AmpelConfig = None) -> "T2DocView":
		"""
		We might want to move this method elsewhere in the future
		"""

		if conf:
			t2_unit_info = conf.get(f'unit.{doc["unit"]}', dict)
			if not t2_unit_info:
				raise ValueError(f'Unknown T2 unit {doc["unit"]}')

			if 'AbsStockT2Unit' in t2_unit_info['base']:
				t2_type: int = TYPE_STOCK_T2
			elif 'AbsPointT2Unit' in t2_unit_info['base']:
				t2_type = TYPE_POINT_T2
			else: # quick n dirty
				t2_type = TYPE_STATE_T2
		else:
			t2_type = -1

		return cls(
			stock = doc['stock'],
			unit = doc['unit'],
			t2_type = t2_type,
			link = doc['link'],
			tag = doc.get('tag', []),
			code = doc['code'],
			meta = doc.get('meta', []),
			body = doc.get('body'),
			config = conf.get(f'confid.{doc["config"]}', dict) if (conf and doc['config']) else None
		)


	def __init__(self,
		stock: StockId | Sequence[StockId],
		unit: int | str,
		link: T2Link,
		tag: Sequence[Tag],
		code: int,
		t2_type: int,
		meta: Sequence[MetaRecord],
		config: None | dict[str, Any] = None,
		body: None | Sequence[UBson] = None
	):
		sa = object.__setattr__
		sa(self, 'stock', stock)
		sa(self, 'unit', unit)
		sa(self, 'link', link)
		sa(self, 'tag', tag)
		sa(self, 'code', code)
		sa(self, 'body', body)
		sa(self, 'meta', meta)
		sa(self, 'config', config)
		sa(self, 't2_type', t2_type)


	def __setattr__(self, k, v):
		raise ValueError("T2DocView is read only")


	def __delattr__(self, k):
		raise ValueError("T2DocView is read only")


	def __reduce__(self):
		return (
			type(self), (
				self.stock, self.unit, self.link, self.tag, self.code,
				self.body, self.meta, self.config, self.t2_type
			)
		)


	def serialize(self) -> dict[str, Any]:
		return {k: getattr(self, k) for k in self.__slots__ if k != '_frozen'}


	def has_content(self) -> bool:
		return True if self.body else False


	def get_payload(self, code: None | int = None) -> UBson:
		"""
		:returns: the content of the last array element of body associated with a meta code >= 0 or equals code arg.
		"""
		if not self.body:
			return None

		idx = len(
			[
				el for el in self.meta
				if el['tier'] == 2 and
				(el['code'] >= 0 if code is None else el['code'] == code)
			]
		) - 1

		if idx == -1:
			return None

		# A manual/admin $unset: {body: 1} was used to delete bad data
		if idx > len(self.body) - 1:
			idx = len(self.body) - 1

		return self.body[idx] if idx >= 0 else None


	def is_point_type(self) -> bool:
		return self.t2_type == TYPE_POINT_T2


	def is_stock_type(self) -> bool:
		return self.t2_type == TYPE_STOCK_T2


	def is_state_type(self) -> bool:
		return self.t2_type == TYPE_STATE_T2


	def get_value(self,
		key: str,
		rtype: type[T], *,
		code: None | int = None,
	) -> None | T:
		"""
		:returns: the value of a given key from the content of the last array element of body
		associated with a meta code >= 0 or equals code arg

		Examples:
		get_value("fit_result", dict)
		"""
		r = self.get_payload(code)
		if isinstance(r, dict) and key in r:
			return r[key]
		return None


	@overload
	def get_ntuple(self,
		key: tuple[str, ...], rtype: type[T], *,
		no_none: Literal[True], require_all_keys: bool, code: None | int
	) -> None | tuple[T, ...]:
		...

	@overload
	def get_ntuple(self,
		key: tuple[str, ...], rtype: type[T], *,
		no_none: Literal[False], require_all_keys: bool, code: None | int
	) -> None | tuple[None | T, ...]:
		...

	def get_ntuple(self,
		key: tuple[str, ...],
		rtype: type[T], *,
		no_none: bool = False,
		require_all_keys: bool = True,
		code: None | int = None,
	) -> None | tuple[T, ...] | tuple[None | T, ...]:
		"""
		Returns a tuple of n values from the content of the last array element of body
		associated with a meta code >= 0 or equals code arg

		Examples:

		In []: tv = T2DocView(
			body=[{'a': 1, 'b': None, 'c': 3}], unit=None, link=None, tag=None,
			code=0, t2_type=0, meta=[{'tier': 2, 'code':0}], stock=0
		)

		In []: tv.get_ntuple(("a", "b"), int, no_none = False)
		Out[]: (1, None)

		In []: tv.get_ntuple(("a", "b"), int, no_none = True)
		Out[]: None

		In []: tv = T2DocView(body=[{'a': 1, 'c': 3}], ...)

		In []: tv.get_ntuple(("a", "b"), int)
		Out[]: None

		In []: tv.get_ntuple(("a", "b"), int, require_all_keys = False)
		Out[]: (1, None)

		In []: tv.get_ntuple(("a", "b"), int, require_all_keys = False, no_none = True)
		Out[]: None
		"""

		r = self.get_payload(code)

		if isinstance(r, dict):
			if r and (sks := r.keys() & key):

				if require_all_keys and len(sks) != len(key):
					return None

				t = tuple(
					r[k] if (k in r and isinstance(r[k], rtype)) else None
					for k in key
				)

				return None if (no_none and None in t) else t # type: ignore[return-value]

		return None


	@overload
	def get_time_created(self, to_string: Literal[False]) -> None | float:
		...
	@overload
	def get_time_created(self, to_string: Literal[True]) -> None | str:
		...
	def get_time_created(self, to_string: bool = False) -> None | float | str:

		ts = self.meta[0]['ts']

		if to_string:
			return datetime.fromtimestamp(ts).strftime('%d/%m/%Y %H:%M:%S')

		return ts


	@overload
	def get_time_updated(self, to_string: Literal[False]) -> None | float:
		...
	@overload
	def get_time_updated(self, to_string: Literal[True]) -> None | str:
		...
	def get_time_updated(self, to_string: bool = False) -> None | float | str:

		if not self.has_content():
			return None

		ts = self.meta[-1]['ts']
		if to_string:
			return datetime.fromtimestamp(ts).strftime('%d/%m/%Y %H:%M:%S')

		return ts
