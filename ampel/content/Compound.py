#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/content/Compound.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : Unspecified
# Last Modified Date: 04.03.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Sequence, Optional, Literal, TypedDict, Union
from ampel.type import StockId, ChannelId, DataPointId

class CompoundElement(TypedDict, total=False):
	id: DataPointId
	tag: Optional[Sequence[Union[int, str]]]
	excl: Optional[Union[int, str]] # exclusion reason

class Compound(TypedDict, total=False):

	_id: bytes
	tag: Optional[Sequence[Union[int, str]]]
	stock: Union[StockId, Sequence[StockId]]
	channel: Union[ChannelId, Sequence[ChannelId]]
	data: Sequence[Union[DataPointId, CompoundElement]]
	tier: Literal[0, 1, 2, 3]
	run: Union[int, Sequence[int]]
	added: float
	len: int
