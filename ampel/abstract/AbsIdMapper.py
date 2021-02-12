#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsIdMapper.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 12.02.2021
# Last Modified Date: 12.02.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import List, Union, overload
from ampel.type import StrictIterable, StockId
from ampel.base import abstractmethod, AmpelBaseModel
from ampel.base.AmpelABC import AmpelABC


class AbsIdMapper(AmpelABC, AmpelBaseModel, abstract=True):

	@overload
	@classmethod
	def to_ampel_id(cls, ext_id: str) -> int:
		...

	@overload
	@classmethod
	def to_ampel_id(cls, ext_id: StrictIterable[str]) -> List[int]:
		...

	@classmethod
	@abstractmethod
	def to_ampel_id(cls, ext_id: Union[str, StrictIterable[str]]) -> Union[int, List[int]]:
		...

	@overload
	@classmethod
	def to_ext_id(cls, ampel_id: StockId) -> str:
		...

	@overload
	@classmethod
	def to_ext_id(cls, ampel_id: StrictIterable[StockId]) -> List[str]:
		...

	@classmethod
	@abstractmethod
	def to_ext_id(cls, ampel_id: Union[StockId, StrictIterable[StockId]]) -> Union[str, List[str]]:
		...
