#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/content/JournalRecord.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 12.12.2019
# Last Modified Date: 05.09.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Sequence, Union, Literal, Any, Dict, TypedDict
from ampel.types import ChannelId, Tag


class JournalRecord(TypedDict, total=False):
	"""
	A record of activity on a stock document.

	.. seealso:: :class:`~ampel.struct.JournalAttributes.JournalAttributes`
	"""

	#: Tier of the associated process
	tier: Literal[-1, 0, 1, 2, 3]

	#: UNIX epoch of the activity
	ts: Union[int, float]

	#: Channels associated with the activity
	channel: Union[ChannelId, Sequence[ChannelId]]

	#: Name of the associated process
	process: Union[int, str]

	#: Free-form labels
	tag: Union[Tag, Sequence[Tag]]

	#: Run(s) associated with this record
	run: int

	#: Status code of the associated process
	code: int

	#: Action code(s) built from :class:`~ampel.enum.JournalActionCode.JournalActionCode`
	action: int

	#: Duration of the process
	duration: Union[int, float]

	#: Trace ids
	traceid: Dict[str, int]

	#: id of the unit associated with this record
	unit: Union[int, str]

	#: id of the document associated with the invocation
	doc: Union[int, bytes]

	#: Free-form information
	extra: Dict[str, Any]
