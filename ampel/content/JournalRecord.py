#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/content/JournalRecord.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 12.12.2019
# Last Modified Date: 08.06.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Sequence, Union, Literal, Any, Dict, TypedDict, List
from ampel.type import ChannelId, Tag

class JournalRecord(TypedDict, total=False):
	"""
	A record of activity on a stock.

	.. seealso:: :class:`~ampel.struct.JournalTweak.JournalTweak`

	This is a dict containing 1 or more of the following items:
	"""
	#: Tier of the associated process
	tier: Literal[0, 1, 2, 3]
	#: UNIX epoch of the activity
	ts: Union[int, float]
	#: Channels associated with the activity
	channel: Union[ChannelId, Sequence[ChannelId]]
	#: Name of the associated process
	process: Union[int, str]
	#: Free-form labels
	tag: Union[Tag, Sequence[Tag]]
	#: Status code of the associated process
	status: int
	#: id of the unit associated with this record
	unit: Union[int, str]
	#: id of the document associated with the invocation
	doc: Union[int, bytes]
	#: run(s) associated with this record
	run: Union[int, List[int]]
	#: Free-form information
	extra: Dict[str, Any]
