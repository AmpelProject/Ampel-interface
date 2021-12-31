#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/protocol/AmpelAlertProtocol.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 24.11.2021
# Last Modified Date: 24.11.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Optional, Union, Any, Protocol
from collections.abc import Sequence
from ampel.types import StockId, Tag


class AmpelAlertProtocol(Protocol):

	@property
	def id(self) -> int:
		...

	@property
	def stock(self) -> StockId:
		...

	@property
	def tag(self) -> Union[None, Tag, list[Tag]]:
		...

	@property
	def extra(self) -> Optional[dict[str, Any]]:
		...

	@property
	def datapoints(self) -> Sequence[dict[str, Any]]:
		...

	def get_values(self,
		key: str, filters: Optional[Sequence[dict[str, Any]]] = None
	) -> list[Any]:
		...

	def get_tuples(self,
		key1: str, key2: str,
		filters: Optional[Sequence[dict[str, Any]]] = None
	) -> list[tuple[Any, Any]]:
		...

	def get_ntuples(self,
		params: list[str], filters: Optional[Sequence[dict[str, Any]]] = None
	) -> list[tuple]:
		...

	# Unsure whether this belongs here
	def is_new(self) -> bool:
		...

	def dict(self) -> dict[str, Any]:
		...
