#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/view/SnapView.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                13.01.2018
# Last Modified Date:  24.11.2022
# Last Modified By:    simeon reusch

from datetime import datetime
from typing import Any, Literal, overload
from collections.abc import Container, Callable, Iterator, Sequence

from ampel.types import OneOrMany, StockId, T2Link, UBson, T
from ampel.struct.AmpelBuffer import AmpelBuffer
from ampel.config.AmpelConfig import AmpelConfig
from ampel.content.DataPoint import DataPoint
from ampel.content.T1Document import T1Document
from ampel.view.T2DocView import T2DocView
from ampel.content.StockDocument import StockDocument
from ampel.content.LogDocument import LogDocument
from ampel.content.JournalRecord import JournalRecord
from ampel.util.freeze import recursive_freeze as rf


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
	:meth:`AbsT3ReviewUnit.process() <ampel.abstract.AbsT3ReviewUnit.AbsT3ReviewUnit.process>`.

	"""

	__slots__ = 'id', 'stock', 'origin', 't0', 't1', 't2', 'logs', 'extra'

	id: StockId
	stock: None | StockDocument
	origin: None | OneOrMany[int]
	t0: None | Sequence[DataPoint]
	t1: None | Sequence[T1Document]
	t2: None | Sequence[T2DocView]
	logs: None | Sequence[LogDocument]
	extra: None | dict[str, Any]


	@classmethod
	def of(cls, ab: AmpelBuffer, conf: None | AmpelConfig = None, freeze: bool = True) -> 'SnapView':

		if freeze:
			return cls(
				id = ab['id'],
				stock = rf(ab['stock']) if ab.get('stock') else None,
				origin = ab.get('origin'),
				t0 = tuple(rf(el) for el in ab['t0']) if ab.get('t0') else None, # type: ignore[union-attr]
				t1 = tuple(rf(el) for el in ab['t1']) if ab.get('t1') else None, # type: ignore[union-attr]
				t2 = tuple(T2DocView.of(rf(el), conf) for el in ab['t2']) if ab.get('t2') else None, # type: ignore[union-attr]
				logs = tuple(rf(el) for el in ab['logs']) if ab.get('logs') else None, # type: ignore[union-attr]
				extra = rf(ab['extra']) if ab.get('extra') else None
			)

		return cls(
			id = ab['id'],
			stock = ab.get('stock'),
			origin = ab.get('origin'),
			t0 = ab.get('t0'),
			t1 = ab.get('t1'),
			t2 = [T2DocView.of(el, conf) for el in ab['t2']] if ab.get('t2') else None, # type: ignore[union-attr]
			logs = ab.get('logs'),
			extra = ab.get('extra')
		)


	def __init__(self,
		id: StockId,
		stock: None | StockDocument = None,
		origin: None | OneOrMany[int] = None,
		t0: None | Sequence[DataPoint] = None,
		t1: None | Sequence[T1Document] = None,
		t2: None | Sequence[T2DocView] = None,
		logs: None | Sequence[LogDocument] = None, # Logs, if added by T3 complement stage
		extra: None | dict[str, Any] = None # Free-form information addable via instances of AbsBufferComplement
	):
		sa = object.__setattr__
		sa(self, 'id', id)
		sa(self, 'stock', stock)
		sa(self, 'origin', origin)
		sa(self, 't0', t0)
		sa(self, 't1', t1)
		sa(self, 't2', t2)
		sa(self, 'logs', logs)
		sa(self, 'extra', extra)


	def __setattr__(self, k, v):
		raise ValueError('SnapView is read only')


	def __delattr__(self, k):
		raise ValueError("SnapView is read only")


	def __reduce__(self):
		return (
			type(self),
			(
				self.id, self.stock, self.origin, self.t0,
				self.t1, self.t2, self.logs, self.extra
			)
		)


	def serialize(self) -> dict:
		return {k: getattr(self, k) for k in self.__slots__}


	# TODO: add config filter
	def get_t2_views(self,
		unit: None | str | list[str] | tuple[str, ...] = None,
		link: None | T2Link = None,
		code: None | int = None,
	) -> Iterator[T2DocView]:
		"""
		Get a subset of T2 documents.

		:param unit: limits the returned science record(s) to the one with the provided t2 unit id
		:param link: whether to return the latest science record(s) or not (default: False)

		"""

		if not self.t2:
			return None

		units: None | Container[str] = [unit] if isinstance(unit, str) else unit

		for t2v in self.t2:
			if link and t2v.link != link:
				continue
			if units and t2v.unit not in units:
				continue
			if code is not None and t2v.code != code:
				continue
			yield t2v


	def get_raw_t2_body(self,
		unit: str | list[str] | tuple[str, ...],
		link: None | T2Link = None,
		code: None | int = None,
	) -> None | Sequence[UBson]:
		"""
		:param link: restrict to a specific link
		:param code: restrict to a specific code
		"""

		# from the records that match the unit and compound selection,
		# return the last record that has a result
		for t2v in self.get_t2_views(unit, link=link, code=code):
			return t2v.body
		return None


	def get_latest_t2_body(self,
		unit: str | list[str] | tuple[str, ...],
		link: None | T2Link = None,
		code: None | int = None,
	) -> UBson:
		"""
		Get latest t2 body element from a given unit.

		:param unit_id: target unit id
		:param link_id: restrict to a specific link
		"""

		# from the records that match the unit and compound selection,
		# return the last record that has a result
		if (t2v := next(self.get_t2_views(unit, link=link, code=code), None)):
			for subrecord in reversed(t2v.body or []):
				if subrecord:
					return subrecord
		return None


	@overload
	def get_t2_body(self, unit: str | list[str] | tuple[str, ...]) -> None | dict[str, Any]:
		...
	@overload
	def get_t2_body(self, unit: str | list[str] | tuple[str, ...], ret_type: type[T]) -> None | T:
		...
	@overload
	def get_t2_body(self, unit: str | list[str] | tuple[str, ...], *, raise_exc: Literal[True]) -> T:
		...
	def get_t2_body(self,
		unit: str | list[str] | tuple[str, ...],
		ret_type: type[T] = dict, # type: ignore[assignment]
		*,
		data_slice: int = -1, # latest
		link: None | T2Link = None,
		code: None | int = None,
		raise_exc: bool = False
	) -> None | T:
		"""
		Get latest t2 body element from a given unit.
		:param ret_type: expected body element type. If isinstance check is not fullfied
		None will be returned (unless multiple unit are to be matched and another
		unit fullfill the criteria) or an exception will be raised if raise_exc is True
		:param link: restrict to a specific link
		"""
		for t2v in self.get_t2_views(unit, link=link, code=code):
			if t2v.body:
				ret = t2v.body[data_slice]
				if isinstance(ret, ret_type):
					return ret
		return None


	def get_t2_value(self,
		unit: str | tuple[str, ...],
		key: str,
		rtype: type[T], *,
		code: None | int = None
	) -> None | T:
		"""
		Examples:
		get_t2_value(("T2NedSNCosmo", "T2SNCosmo"), "fit_result", dict)

		see T2DocView.get_value(...) for more info
		"""
		for t2v in self.get_t2_views(unit):
			if (x := t2v.get_value(key, rtype, code=code)):
				return x
		return None


	@overload
	def get_t2_ntuple(self,
		unit: str | tuple[str, ...], key: tuple[str, ...], rtype: type[T], *,
		no_none: Literal[False], require_all_keys: bool = ..., code: None | int = ...
	) -> None | tuple[None | T, ...]:
		...

	@overload
	def get_t2_ntuple(self,
		unit: str | tuple[str, ...], key: tuple[str, ...], rtype: type[T], *,
		no_none: Literal[True], require_all_keys: bool = ..., code: None | int = ...
	) -> None | tuple[T, ...]:
		...

	def get_t2_ntuple(self,
		unit: str | tuple[str, ...],
		key: tuple[str, ...],
		rtype: type[T], *,
		no_none: bool = False,
		require_all_keys: bool = True,
		code: None | int = None
	) -> None | tuple[T, ...] | tuple[None | T, ...]:
		"""
		Examples:
		get_t2_ntuple("T2NedTap", ("ra", "dec", "z", "zunc"), float)
		get_t2_ntuple(("T2NedSNCosmo", "T2SNCosmo"), ("fit_result", "covariance"), dict)

		see T2DocView.get_ntuple(...) for more info
		"""

		for t2v in self.get_t2_views(unit):
			if (x := t2v.get_ntuple( # type: ignore
				key, rtype, no_none = no_none, require_all_keys = require_all_keys, code = code
			)):
				return x
		return None


	def get_journal_entries(self,
		tier: None | Literal[0, 1, 2, 3] = None,
		process_name: None | str = None,
		filter_func: None | Callable[[JournalRecord], bool] = None,
	) -> Iterator[JournalRecord]:
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

		# Journal entries are sorted chronologically
		for je in self.stock['journal']:

			if tier is not None and je['tier'] != tier:
				continue

			if process_name and je['process'] != process_name:
				continue

			if filter_func and not filter_func(je):
				continue

			yield je


	def get_time_created(self,
		output: Literal['raw', 'datetime', 'str'] = 'raw'
	) -> None | float | datetime | str:

		if not self.stock:
			return None
		# Journal cannot be empty
		return self._get_time(self.stock['journal'][0], output)


	def get_time_updated(self,
		output: Literal['raw', 'datetime', 'str'] = 'raw'
	) -> None | float | datetime | str:

		if not self.stock:
			return None
		# Journal cannot be empty
		return self._get_time(self.stock['journal'][-1], output)


	@classmethod
	def _get_time(cls,
		entry: JournalRecord,
		output: None | bool | str = None
	) -> float | str | datetime:

		if output == 'raw':
			return entry['ts']

		dt = datetime.fromtimestamp(entry['ts'])

		if output == 'datetime':
			return dt

		return dt.strftime('%d/%m/%Y %H:%M:%S')


	def content_summary(self) -> str:
		return 'DP: %i, CP: %i, T2: %i' % (
			len(self.t0) if self.t0 else 0,
			len(self.t1) if self.t1 else 0,
			len(self.t2) if self.t2 else 0
		)
