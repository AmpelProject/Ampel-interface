#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/protocol/AmpelAlertProtocol.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                24.11.2021
# Last Modified Date:  24.11.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from typing import Any, Protocol, runtime_checkable
from collections.abc import Sequence
from ampel.types import StockId, Tag

@runtime_checkable
class AmpelAlertProtocol(Protocol):

	@property
	def id(self) -> int:
		...

	@property
	def stock(self) -> StockId:
		...

	@property
	def tag(self) -> None | Tag | list[Tag]:
		...

	@property
	def extra(self) -> None | dict[str, Any]:
		...

	@property
	def datapoints(self) -> Sequence[dict[str, Any]]:
		...

	def get_values(self,
		key: str, filters: None | Sequence[dict[str, Any]] = None
	) -> list[Any]:
		...

	def get_tuples(self,
		key1: str, key2: str,
		filters: None | Sequence[dict[str, Any]] = None
	) -> list[tuple[Any, Any]]:
		...

	def get_ntuples(self,
		params: list[str], filters: None | Sequence[dict[str, Any]] = None
	) -> list[tuple]:
		...

	# Unsure whether this belongs here
	def is_new(self) -> bool:
		...

	def dict(self) -> dict[str, Any]:
		...
