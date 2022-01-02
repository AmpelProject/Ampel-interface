#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/content/LogDocument.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                14.02.2020
# Last Modified Date:  16.03.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

import sys
if sys.version_info.minor > 8:
	from typing import TypedDict
else:
	from typing_extensions import TypedDict
from typing import Any
from collections.abc import Sequence
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
	r: int | Sequence[int]

	#: msg
	m: str | Sequence[str] | ChannelLogEntry

	#: stock
	s: StockId | Sequence[StockId]

	#: channel
	c: ChannelId | Sequence[ChannelId]

	#: extra
	e: dict[str, Any]
