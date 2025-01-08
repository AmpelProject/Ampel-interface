#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/view/T2DocView.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                10.02.2021
# Last Modified Date:  01.03.2023
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Literal, overload

from ampel.config.AmpelConfig import AmpelConfig
from ampel.content.MetaRecord import MetaRecord
from ampel.content.T2Document import T2Document
from ampel.types import StockId, T2Link, Tag, TBson, UBson

TYPE_POINT_T2 = 0 # linked with datapoints (tier 0)
TYPE_STATE_T2 = 1 # linked with compounds (tier 1)
TYPE_STOCK_T2 = 3 # linked with stock document

if TYPE_CHECKING:
	from typing import Self


@dataclass(frozen=True, slots=True, kw_only=True)
class T2DocView:
	"""
	View of a given T2Document (with unique stock id).
	A t2 view contains read-only information from a T2Document
	and provides convenience methods to access it.
	"""

	stock: StockId | Sequence[StockId]
	unit: int | str
	confid: None | int
	config: None | dict[str, Any] = None
	link: T2Link
	tag: Sequence[Tag]
	code: int
	t2_type: int
	meta: Sequence[MetaRecord]
	body: None | Sequence[UBson] = None


	@classmethod # Static ctor
	def of(cls, doc: T2Document, conf: None | AmpelConfig = None) -> "Self":

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

		dc = doc['config']
		return cls(
			stock = doc['stock'],
			unit = doc['unit'],
			confid = dc if isinstance(dc, int) else None,
			t2_type = t2_type,
			link = doc['link'],
			tag = doc.get('tag', []),
			code = doc['code'],
			meta = doc.get('meta', []),
			body = doc.get('body'),
			config = dc if isinstance(dc, dict) else (
				conf.get(('confid', dc), dict) if (conf and dc is not None) else None
			)
		)


	def has_content(self) -> bool:
		return bool(self.body)

	@overload
	def get_payload(self, *, code: None | int=None) -> None | Mapping[str, Any]:
		...

	@overload
	def get_payload(self, *, raise_exc: Literal[True], code: None | int=None) -> Mapping[str, Any]:
		...

	@overload
	def get_payload(self, rtype: type[TBson], *, code: None | int=None) -> None | TBson:
		...
	
	@overload
	def get_payload(self, rtype: type[TBson], *, raise_exc: Literal[True], code: None | int=None) ->  TBson:
		...

	def get_payload(self,
		rtype: type[TBson]=Mapping,  # type: ignore[assignment]
		*,
		raise_exc: bool = False,
		code: None | int = None,
	) -> None | TBson | UBson:
		"""
		:returns: the content of the last array element of body associated with a meta code >= 0 or equals code arg.
		"""
		if not self.body:
			if raise_exc:
				raise ValueError("T2 doc has no body")
			return None

		idx = len(
			[
				el for el in self.meta
				if el['tier'] == 2 and
				(el['code'] >= 0 if code is None else el['code'] == code)
			]
		) - 1

		if idx == -1:
			if raise_exc:
				raise ValueError("No content available")
			return None

		# A manual/admin $unset: {body: 1} was used to delete bad data
		idx = min(idx, len(self.body) - 1)
		if idx < 0:
			if raise_exc:
				raise ValueError("No content available")
			return None

		return self.body[idx]


	def is_point_type(self) -> bool:
		return self.t2_type == TYPE_POINT_T2


	def is_stock_type(self) -> bool:
		return self.t2_type == TYPE_STOCK_T2


	def is_state_type(self) -> bool:
		return self.t2_type == TYPE_STATE_T2


	def get_value(self,
		key: str,
		rtype: type[TBson], *,
		code: None | int = None,
	) -> None | TBson:
		"""
		:returns: the value of a given key from the content of the last array element of body
		associated with a meta code >= 0 or equals code arg

		Examples:
		get_value("fit_result", dict)
		"""
		r = self.get_payload(code=code)
		if isinstance(r, Mapping) and key in r:
			return r[key]
		return None


	@overload
	def get_ntuple(self,
		key: tuple[str, ...], rtype: type[TBson], *,
		no_none: Literal[True], require_all_keys: bool, code: None | int
	) -> None | tuple[TBson, ...]:
		...

	@overload
	def get_ntuple(self,
		key: tuple[str, ...], rtype: type[TBson], *,
		no_none: Literal[False], require_all_keys: bool, code: None | int
	) -> None | tuple[None | TBson, ...]:
		...

	def get_ntuple(self,
		key: tuple[str, ...],
		rtype: type[TBson], *,
		no_none: bool = False,
		require_all_keys: bool = True,
		code: None | int = None,
	) -> None | tuple[TBson, ...] | tuple[None | TBson, ...]:
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

		r = self.get_payload(code=code)

		if (
			isinstance(r, dict)
			and r and (sks := r.keys() & key)
		):
			if require_all_keys and len(sks) != len(key):
				return None

			t = tuple(
				r[k] if (k in r and isinstance(r[k], rtype)) else None
				for k in key
			)

			return None if (no_none and None in t) else t

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
			return datetime.fromtimestamp(ts, tz=timezone.utc).strftime('%d/%m/%Y %H:%M:%S')

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
			return datetime.fromtimestamp(ts, tz=timezone.utc).strftime('%d/%m/%Y %H:%M:%S')

		return ts
