#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/content/DataPoint.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 12.12.2019
# Last Modified Date: 13.02.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Any, Sequence, Union, Dict, TypedDict
from ampel.type import StockId, DataPointId, ChannelId

class DataPoint(TypedDict, total=False):
	"""
	A single data point.

	This is a dict containing 1 or more of the following items:
	"""
	_id: DataPointId
	tag: Sequence[Union[int, str]]
	stock: Union[StockId, Sequence[StockId]]
	channel: Union[ChannelId, Sequence[ChannelId]]
	excl: Sequence[ChannelId]
	extra: Dict[str, Any]
	policy: Dict[str, Any]
	body: Dict[str, Any]
