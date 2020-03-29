#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/content/T2Record.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 13.01.2018
# Last Modified Date: 10.03.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Sequence, Union, Optional, TypedDict, Dict
from ampel.types import ChannelId, StockId

class T2Record(TypedDict, total=False):

	_id: bytes
	unit: Union[int, str] # int to enable future potential hash optimizations
	stock: Union[StockId, Sequence[StockId]]
	link: Union[bytes, Sequence[bytes]]
	tag: Optional[Sequence[Union[int, str]]]
	channel: Sequence[ChannelId]
	col: Optional[str]
	run: Union[int, Sequence[int]]
	status: int
	config: Union[int, Dict]
	result: Optional[Sequence[dict]] # value(s) returned by t2 unit execution(s)
