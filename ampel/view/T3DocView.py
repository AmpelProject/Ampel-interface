#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/view/T3DocView.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 01.12.2021
# Last Modified Date: 12.12.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from datetime import datetime
from typing import Optional, Union, Any, Sequence, Literal, Type, overload
from ampel.types import StockId, UBson, TBson, Tag
from ampel.content.MetaRecord import MetaRecord
from ampel.content.T3Document import T3Document
from ampel.config.AmpelConfig import AmpelConfig


class T3DocView:
	"""
	View of a given T3Document.
	A t3 view contains read-only information from a T3Document
	and provides convenience methods to access it.
	"""

	__slots__ = 'unit', 'confid', 'config', 'stock', 'tag', 'code', 'meta', 'body'

	stock: Optional[Sequence[StockId]]
	unit: str
	confid: int
	config: Optional[dict[str, Any]]
	tag: Optional[Union[Tag, Sequence[Tag]]]
	code: int
	meta: MetaRecord
	body: UBson


	@classmethod # Static ctor
	def of(cls, doc: T3Document, conf: AmpelConfig) -> "T3DocView":

		if 'config' in doc:
			config = doc['config']
		else:
			config = conf._config['confid'][doc['confid']]

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


	def __init__(self,
		unit: str,
		code: int,
		meta: MetaRecord,
		confid: int,
		tag: Optional[Union[Tag, Sequence[Tag]]] = None,
		stock: Optional[Sequence[StockId]] = None,
		config: Optional[dict[str, Any]] = None,
		body: UBson = None
	):
		sa = object.__setattr__
		sa(self, 'stock', stock)
		sa(self, 'unit', unit)
		sa(self, 'tag', tag)
		sa(self, 'code', code)
		sa(self, 'body', body)
		sa(self, 'meta', meta)
		sa(self, 'config', config)
		sa(self, 'confid', confid)


	def __setattr__(self, k, v):
		raise ValueError("T3DocView is read only")


	def __delattr__(self, k):
		raise ValueError("T3DocView is read only")


	def serialize(self) -> dict[str, Any]:
		return {k: getattr(self, k) for k in self.__slots__ if k != '_frozen'}


	@overload
	def get_body(self) -> Optional[dict[str, Any]]:
		...
	@overload
	def get_body(self, *, raise_exc: Literal[True]) -> dict[str, Any]:
		...
	@overload
	def get_body(self, ret_type: Type[TBson]) -> Optional[TBson]:
		...
	@overload
	def get_body(self, ret_type: Type[TBson], *, raise_exc: Literal[True]) -> TBson:
		...
	@overload
	def get_body(self, ret_type: Type[TBson], *, raise_exc: Literal[False]) -> Optional[TBson]:
		...
	def get_body(self, ret_type: Type[TBson] = dict, *, raise_exc: bool = False) -> Optional[TBson]: # type: ignore[assignment]
		"""
		:param raise_exc: raise exception if the body has not the expected type

		reveal_type(t3dv.get_body()) -> Union[builtins.dict[builtins.str, Any], None]
		reveal_type(t3dv.get_body(raise_exc=True)) -> builtins.dict[builtins.str, Any]
		reveal_type(t3dv.get_body(str)) -> Union[builtins.str, None]
		reveal_type(t3dv.get_body(str, raise_exc=True)) -> builtins.str
		"""
		return self.body if isinstance(self.body, ret_type) else None


	@overload
	def get_time_created(self, to_string: Literal[False]) -> Optional[float]:
		...
	@overload
	def get_time_created(self, to_string: Literal[True]) -> Optional[str]:
		...
	def get_time_created(self, to_string: bool = False) -> Optional[Union[float, str]]:

		if to_string:
			return datetime.fromtimestamp(self.meta['ts']).strftime('%d/%m/%Y %H:%M:%S')

		return self.meta['ts']
