#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/abstract/AbsIdMapper.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                12.02.2021
# Last Modified Date:  12.02.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from typing import overload
from ampel.types import StrictIterable, StockId
from ampel.base.AmpelABC import AmpelABC
from ampel.base.decorator import abstractmethod
from ampel.base.AmpelBaseModel import AmpelBaseModel


class AbsIdMapper(AmpelABC, AmpelBaseModel, abstract=True):

	@overload
	@classmethod
	def to_ampel_id(cls, ext_id: str) -> int:
		...

	@overload
	@classmethod
	def to_ampel_id(cls, ext_id: StrictIterable[str]) -> list[int]:
		...

	@classmethod
	@abstractmethod
	def to_ampel_id(cls, ext_id: str | StrictIterable[str]) -> int | list[int]:
		...

	@overload
	@classmethod
	def to_ext_id(cls, ampel_id: StockId) -> str:
		...

	@overload
	@classmethod
	def to_ext_id(cls, ampel_id: StrictIterable[StockId]) -> list[str]:
		...

	@classmethod
	@abstractmethod
	def to_ext_id(cls, ampel_id: StockId | StrictIterable[StockId]) -> str | list[str]:
		...
