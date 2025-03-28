#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/content/StockDocument.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                28.12.2019
# Last Modified Date:  05.05.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from collections.abc import Sequence
from typing import Any, Literal

from typing_extensions import TypedDict

from ampel.content.JournalRecord import JournalRecord
from ampel.types import ChannelId, StockId, Tag


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
	updated: int | float

	#: External name(s) associated with the stock
	name: Sequence[int | str]

	#: Optional specific content
	body: dict[str, Any]
