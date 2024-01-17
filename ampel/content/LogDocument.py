#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/content/LogDocument.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                14.02.2020
# Last Modified Date:  15.12.2022
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from collections.abc import Sequence
from typing import Any, TypedDict

from typing_extensions import Required

from ampel.types import ChannelId, StockId


class ChannelLogEntry(TypedDict):
	"""
	Abbreviations:
	s: stock, a: alert, f: flag, r: run, m: msg, c: channel

	Used to save multiple channel specific messages into a single LogDocument
	Example of a LogDocument embedding two ChannelLogEntry entries: {
		"_id" : ObjectId("5be4aa6254048041edbac352"),
		"s" : 1810101032122523,
		"a" : 404105201415015004,
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
	f: Required[int]

	#: run id
	r: Required[int | Sequence[int]]

	#: msg
	m: str | Sequence[str] | ChannelLogEntry

	#: stock
	s: StockId | Sequence[StockId]

	#: channel
	c: ChannelId | Sequence[ChannelId]

	#: unit
	u: str

	#: extra
	x: dict[str, Any]

	#: file:line_number (set DBLoggingHanlder.log_provenance to True)
	p: tuple[str, int]
