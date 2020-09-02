#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/content/DataPoint.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 12.12.2019
# Last Modified Date: 02.09.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Any, Sequence, Union, Optional, Dict, TypedDict
from ampel.type import StockId, DataPointId, ChannelId


class DataPoint(TypedDict, total=False):
	_id: DataPointId
	tag: Sequence[Union[int, str]]
	stock: Optional[Union[StockId, Sequence[StockId]]]
	channel: Optional[Union[ChannelId, Sequence[ChannelId]]]
	excl: Optional[Sequence[ChannelId]]
	extra: Optional[Dict[str, Any]]
	policy: Optional[Dict[str, Any]]
	body: Dict[str, Any]
