#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/view/T3Store.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                01.12.2021
# Last Modified Date:  02.01.2022
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from typing import Any
from collections.abc import Container, Iterator, Iterable, Sequence
from ampel.types import JDict, OneOrMany
from ampel.view.T3DocView import T3DocView
from ampel.view.ReadOnlyDict import ReadOnlyDict
from ampel.content.T3Document import T3Document
from ampel.config.AmpelConfig import AmpelConfig
from ampel.util.mappings import dictify
from ampel.util.hash import build_unsafe_dict_id


class T3Store:

	__slots__ = 'views', 'units', 'session'
	views: None | Sequence[T3DocView]
	session: None | JDict
	units: set[str]


	@classmethod # Static ctor
	def of(cls, docs: None | Sequence[T3Document], conf: AmpelConfig) -> "T3Store":
		return cls(
			views = tuple(
				T3DocView.of(doc, conf)
				for doc in docs
			) if docs else None
		)


	def __init__(self, views: None | Sequence[T3DocView] = None, session: None | JDict = None):
		object.__setattr__(self, 'views', views)
		object.__setattr__(self, 'session', ReadOnlyDict(session) if session else None)
		object.__setattr__(self, 'units', set(v.unit for v in views) if views else set())


	def __setattr__(self, k, v):
		raise ValueError("T3Store is read only")


	def __delattr__(self, k):
		raise ValueError("T3Store is read only")


	def add_view(self, t3v: T3DocView) -> None:
		self.units.add(t3v.unit)
		if self.views:
			l = list(self.views) if self.views else []
			l.append(t3v)
			object.__setattr__(self, 'views', tuple(l))
		else:
			object.__setattr__(self, 'views', (t3v, ))


	def add_session_info(self, d: JDict) -> None:
		if self.session:
			object.__setattr__(self, 'session', ReadOnlyDict(self.session | d))
		else:
			object.__setattr__(self, 'session', ReadOnlyDict(d))


	def contains(self, unit: str | Iterable[str]) -> bool:
		if isinstance(unit, str):
			return unit in self.units
		return bool(len(set(unit) - self.units))


	def get_mandatory_view(self,
		unit: None | str | Container[str] = None, *,
		config: None | int | JDict = None,
		code: None | int = None
	) -> T3DocView:
		""" really tired of @overload """
		if (x := self.get_view(unit, config=config, code=code)):
			return x
		raise ValueError(f"{unit} results are required")

			
	def get_view(self,
		unit: None | str | Container[str] = None, *,
		config: None | int | JDict = None,
		code: None | int = None
	) -> None | T3DocView:
		return next(
			self.get_views(unit, config, code),
			None
		)


	def get_views(self,
		unit: str | Container[str] | None = None,
		config: None | OneOrMany[int | JDict] = None,
		code: None | int = None
	) -> Iterator[T3DocView]:
		"""
		Get a subset of T3 documents.

		:param unit: limits the returned science record(s) to the one with the provided t2 unit id
		"""

		if not self.views:
			return None

		units: None | Container[str] = [unit] if isinstance(unit, str) else unit

		if config is None:
			configs = None
		elif isinstance(config, dict):
			configs = [build_unsafe_dict_id(dictify(config))]
		elif isinstance(config, int):
			configs = [config]
		elif isinstance(config, Sequence):
			configs = [
				el if isinstance(el, int) else build_unsafe_dict_id(dictify(el))
				for el in config
			]
		else:
			configs = config

		for t3v in self.views:
			if units and t3v.unit not in units:
				continue
			if configs and t3v.confid not in configs:
				continue
			if code is not None and t3v.code != code:
				continue
			yield t3v
