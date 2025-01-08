#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/view/T3DocView.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                01.12.2021
# Last Modified Date:  12.12.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Literal, overload

from ampel.config.AmpelConfig import AmpelConfig
from ampel.content.MetaRecord import MetaRecord
from ampel.content.T3Document import T3Document
from ampel.types import StockId, Tag, TBson, UBson

if TYPE_CHECKING:
	from typing import Self


@dataclass(frozen=True, slots=True, kw_only=True)
class T3DocView:
	"""
	View of a given T3Document.
	A t3 view contains read-only information from a T3Document
	and provides convenience methods to access it.
	"""

	stock: None | Sequence[StockId] = None
	unit: str
	confid: int
	config: None | dict[str, Any] = None
	tag: None | Tag | Sequence[Tag] = None
	code: int
	meta: MetaRecord
	body: UBson = None


	@classmethod # Static ctor
	def of(cls, doc: T3Document, conf: AmpelConfig) -> "Self":

		if 'config' in doc:
			config = doc['config']
		else:
			config = conf._config['confid'][doc['confid']] # noqa: SLF001

		return cls(
			unit = doc['unit'],
			tag = doc.get('tag') or [],
			code = doc['code'],
			meta = doc['meta'],
			stock = doc.get('stock'),
			body = doc.get('body'),
			config = config,
			confid = doc['confid']
		)

	@overload
	def get_body(self) -> None | dict[str, Any]:
		...
	@overload
	def get_body(self, *, raise_exc: Literal[True]) -> dict[str, Any]:
		...
	@overload
	def get_body(self, ret_type: type[TBson]) -> None | TBson:
		...
	@overload
	def get_body(self, ret_type: type[TBson], *, raise_exc: Literal[True]) -> TBson:
		...
	@overload
	def get_body(self, ret_type: type[TBson], *, raise_exc: Literal[False]) -> None | TBson:
		...
	def get_body(self, ret_type: type[TBson] = dict, *, raise_exc: bool = False) -> None | TBson: # type: ignore[assignment]
		"""
		:param raise_exc: raise exception if the body has not the expected type

		reveal_type(t3dv.get_body()) -> Union[builtins.dict[builtins.str, Any], None]
		reveal_type(t3dv.get_body(raise_exc=True)) -> builtins.dict[builtins.str, Any]
		reveal_type(t3dv.get_body(str)) -> Union[builtins.str, None]
		reveal_type(t3dv.get_body(str, raise_exc=True)) -> builtins.str
		"""
		return self.body if isinstance(self.body, ret_type) else None


	@overload
	def get_time_created(self, to_string: Literal[False]) -> None | float:
		...
	@overload
	def get_time_created(self, to_string: Literal[True]) -> None | str:
		...
	def get_time_created(self, to_string: bool = False) -> None | float | str:

		if to_string:
			return datetime.fromtimestamp(self.meta['ts'], tz=timezone.utc).strftime('%d/%m/%Y %H:%M:%S')

		return self.meta['ts']
