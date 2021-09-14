#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/view/T2DocView.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 10.02.2021
# Last Modified Date: 14.09.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from datetime import datetime
from typing import Dict, Optional, Union, Any, Sequence, Literal, overload
from ampel.types import StockId, UBson, T2Link, Tag
from ampel.content.MetaRecord import MetaRecord
from ampel.content.T2Document import T2Document
from ampel.config.AmpelConfig import AmpelConfig

TYPE_POINT_T2 = 0 # linked with datapoints, that is with tier 0
TYPE_STATE_T2 = 1 # linked with compounds, that is with tier 1
TYPE_STOCK_T2 = 3 # linked with stock document


class T2DocView:
	"""
	View of a given T2Document (with unique stock id).
	"""

	__slots__ = 'unit', 'config', 'link', 'stock', 'tag', 'code', 'meta', 'created', 't2_type', 'body', '_frozen'

	stock: Union[StockId, Sequence[StockId]]
	unit: Union[int, str]
	config: Optional[Dict[str, Any]]
	link: T2Link
	tag: Sequence[Tag]
	code: int
	t2_type: int
	created: float
	meta: Sequence[MetaRecord]
	body: Optional[Sequence[UBson]]


	@classmethod # Static ctor
	def of(cls, doc: T2Document, conf: AmpelConfig) -> "T2DocView":
		"""
		We might want to move this method elsewhere in the future
		"""

		t2_unit_info = conf.get(f'unit.{doc["unit"]}', dict)
		if not t2_unit_info:
			raise ValueError(f'Unknown T2 unit {doc["unit"]}')

		if 'AbsStockT2Unit' in t2_unit_info['base']:
			t2_type: int = TYPE_STOCK_T2
		elif 'AbsPointT2Unit' in t2_unit_info['base']:
			t2_type = TYPE_POINT_T2
		else: # quick n dirty
			t2_type = TYPE_STATE_T2

		return cls(
			stock = doc['stock'],
			unit = doc['unit'],
			t2_type = t2_type,
			link = doc['link'],
			tag = doc['tag'],
			code = doc['code'],
			meta = doc['meta'],
			body = doc.get('body'),
			created = doc['_id'].generation_time.timestamp(), # type: ignore
			config = conf.get(f'confid.{doc["config"]}', dict) \
				if doc['config'] else None
		)


	def __init__(self,
		stock: Union[StockId, Sequence[StockId]],
		unit: Union[int, str],
		link: T2Link,
		tag: Sequence[Tag],
		code: int,
		t2_type: int,
		created: float,
		meta: Sequence[MetaRecord],
		config: Optional[Dict[str, Any]] = None,
		body: Optional[Sequence[UBson]] = None,
		freeze: bool = True
	):
		self.stock = stock
		self.unit = unit
		self.link = link
		self.tag = tag
		self.code = code
		self.body = body
		self.meta = meta
		self.config = config
		self.created = created
		self.t2_type = t2_type
		self._frozen = freeze


	def freeze(self):
		if not self._frozen:
			self._frozen = True


	def __setattr__(self, k, v):
		if getattr(self, "_frozen", False):
			raise ValueError("SnapView is read only")
		object.__setattr__(self, k, v)


	def serialize(self) -> Dict[str, Any]:
		return {k: getattr(self, k) for k in self.__slots__ if k != '_frozen'}


	def has_content(self) -> bool:
		return True if self.body else False


	def get_payload(self) -> UBson:
		"""
		:returns: The content of the last array element of body associated with a meta code >= 0.
		"""
		if not self.body:
			return None

		idx = len([el for el in self.meta if el['tier'] == 2 and el['code'] >= 0]) - 1
		return self.body[idx] if idx >= 0 else None


	def is_point_type(self) -> bool:
		return self.t2_type == TYPE_POINT_T2


	def is_stock_type(self) -> bool:
		return self.t2_type == TYPE_STOCK_T2


	def is_state_type(self) -> bool:
		return self.t2_type == TYPE_STATE_T2


	@overload
	def get_time_created(self, to_string: Literal[False]) -> Optional[float]:
		...
	@overload
	def get_time_created(self, to_string: Literal[True]) -> Optional[str]:
		...
	def get_time_created(self, to_string: bool = False) -> Optional[Union[float, str]]:

		if to_string:
			return datetime.fromtimestamp(self.created).strftime('%d/%m/%Y %H:%M:%S')

		return self.created


	@overload
	def get_time_updated(self, to_string: Literal[False]) -> Optional[float]:
		...
	@overload
	def get_time_updated(self, to_string: Literal[True]) -> Optional[str]:
		...
	def get_time_updated(self, to_string: bool = False) -> Optional[Union[float, str]]:

		if not self.has_content():
			return None

		ts = self.meta[-1]['ts']
		if to_string:
			dt = datetime.fromtimestamp(ts)
			return dt.strftime('%d/%m/%Y %H:%M:%S')

		return ts
