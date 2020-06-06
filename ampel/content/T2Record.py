#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/content/T2Record.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 13.01.2018
# Last Modified Date: 06.06.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Sequence, Union, Optional, TypedDict
from ampel.type import ChannelId, StockId, DataPointId, Tag
from ampel.content.T2SubRecord import T2SubRecord

T2Links = Union[bytes, DataPointId, StockId]


class T2Record(TypedDict, total=False):

	# Indexed values
	_id: bytes
	stock: Union[StockId, Sequence[StockId]]

	# Compound index
	unit: Union[int, str] # unit id can be hashed for performance reason
	config: int
	link: Union[T2Links, Sequence[T2Links]]

	# Non-indexed values
	tag: Optional[Sequence[Tag]]
	channel: Sequence[ChannelId]
	col: Optional[str]
	run: Union[int, Sequence[int]] # positive, ever increasing integer
	# Usually a T2RunState member but let's not be too restrictive here
	status: int
	body: Optional[Sequence[T2SubRecord]] # value(s) returned by t2 unit execution(s)
