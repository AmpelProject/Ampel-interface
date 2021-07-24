#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/content/LogDocument.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 14.02.2020
# Last Modified Date: 16.03.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

import sys
if sys.version_info.minor > 8:
	from typing import TypedDict
else:
	from typing_extensions import TypedDict
from typing import Sequence, Union, Any, Dict
from ampel.types import ChannelId, StockId


class ChannelLogEntry(TypedDict):
	"""
	Abbreviations:
	s: stock, a: alert, f: flag, r: run, m: msg, c: channel

	Used to save multiple channel specific messages into a single LogDocument
	Example of a LogDocument embedding two ChannelLogEntry entries: {
		"_id" : ObjectId("5be4aa6254048041edbac352"),
		"s" : NumberLong(1810101032122523),
		"a" : NumberLong(404105201415015004),
		"f" : 572784643,
		"r" : 509,
		"m" : [
			{"c" : "NO_FILTER", "m": "Alert accepted"},
			{"c" : "HU_RANDOM", "m": "Alert accepted"},
		]
	}
	"""
	#: channel
	c: ChannelId

	#: msg
	m: str


class LogDocument(TypedDict, total=False):
	"""
	Abbreviations:
	s: stock, a: alert, f: flag, r: run, m: msg, c: channel

	Example: {
		"_id" : ObjectId("5be4aa6254048041edbac353"),
		"s" : NumberLong(1810101032122523),
		"a" : NumberLong(404105201415015004),
		"f" : 572784643,
		"r" : 509,
		"c" : "NO_FILTER",
		"m" : "Alert accepted"
	}
	"""

	#: database key
	_id: bytes

	#: flag
	f: int

	#: run id
	r: Union[int, Sequence[int]]

	#: msg
	m: Union[str, Sequence[str], ChannelLogEntry]

	#: stock
	s: Union[StockId, Sequence[StockId]]

	#: channel
	c: Union[ChannelId, Sequence[ChannelId]]

	#: extra
	e: Dict[str, Any]
