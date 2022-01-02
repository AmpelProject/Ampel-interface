#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/content/DataPoint.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                12.12.2019
# Last Modified Date:  17.05.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from typing import Any, TypedDict
from collections.abc import Sequence
from ampel.types import StockId, DataPointId, ChannelId
from ampel.content.MetaRecord import MetaRecord


class DataPoint(TypedDict, total=False):
	"""
	A single data point.

	A dict containing 1 or more of the following items:
	"""

	id: DataPointId
	stock: StockId | Sequence[StockId]
	origin: int
	tag: Sequence[int | str]
	channel: Sequence[ChannelId]
	meta: Sequence[MetaRecord]
	excl: Sequence[ChannelId]
	body: dict[str, Any]
