#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/content/StockDocument.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 28.12.2019
# Last Modified Date: 05.05.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Any, Union, TypedDict, Literal
from collections.abc import Sequence
from ampel.types import StockId, ChannelId, Tag
from ampel.content.JournalRecord import JournalRecord


class StockDocument(TypedDict, total=False):
	"""
	The stock record ties together data from various sources, selected by
	various channels, but all related to the same underlying object. Each
	channel has a different view of the stock.
	From the perspective of a given channel, the stock is updated
	whenever a linked document (T0, T1, T2) is updated.

	A dict containing 1 or more of the following items:
	"""

	#: The unique id associated with the stock. Integer most of the time
	stock: StockId

	#: Optional source origin (avoids potential stock collision between different data sources)
	origin: int

	#: Optional tag(s)
	tag: Sequence[Tag]

	#: Channels asscoiated with this stock
	channel: Sequence[ChannelId]

	#: Records of activity
	journal: Sequence[JournalRecord]

	#: Creation time (UNIX epoch) in each channel
	ts: dict[ChannelId, dict[Literal['tied', 'upd'], float]]

	#: Last update time for any channel
	updated: Union[int, float]

	#: External name(s) associated with the stock
	name: Sequence[Union[int, str]]

	#: Optional specific content
	body: dict[str, Any]
