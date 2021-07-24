#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/content/DataPoint.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 12.12.2019
# Last Modified Date: 17.05.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Any, TypedDict, Sequence, Union, Dict
from ampel.types import StockId, DataPointId, ChannelId
from ampel.content.MetaRecord import MetaRecord


class DataPoint(TypedDict, total=False):
	"""
	A single data point.

	A dict containing 1 or more of the following items:
	"""

	id: DataPointId
	stock: Union[StockId, Sequence[StockId]]
	origin: int
	tag: Sequence[Union[int, str]]
	channel: Sequence[ChannelId]
	meta: Sequence[MetaRecord]
	excl: Sequence[ChannelId]
	body: Dict[str, Any]
