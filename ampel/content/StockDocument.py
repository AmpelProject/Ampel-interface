#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/content/StockDocument.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 28.12.2019
# Last Modified Date: 21.02.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Any, Sequence, Union, Optional, Dict, TypedDict
from ampel.type import StockId, ChannelId
from ampel.content.JournalRecord import JournalRecord


class StockDocument(TypedDict):
	"""
	An object being observed.

	The stock record ties together data from various sources, selected by
	various channels, but all related to the same underlying object. Each
	channel has a different view of the stock. From the perspective of a given
	channel, the stock is created the first time one of its datapoints is
	selected by the channel. Likewise, it is modified whenever a new datapoint
	is selected by the channel.

	This is a dict containing 1 or more of the following items:
	"""
	_id: StockId
	tag: Optional[Sequence[Union[int, str]]]
	#: Channels that have selected datapoints for this stock
	channel: Optional[Sequence[ChannelId]]
	#: Records of activity on the stock
	journal: Sequence[JournalRecord]
	#: Names associated with the stock
	name: Optional[Sequence[Union[int, str]]]
	#: Last modification time (UNIX epoch) in each channel
	modified: Dict[str, Any]
	#: Creation time (UNIX epoch) in each channel
	created: Dict[str, Any]
