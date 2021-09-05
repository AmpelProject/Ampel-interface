#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/content/MetaRecord.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 17.05.2021
# Last Modified Date: 05.09.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Sequence, Union, Literal, Any, Dict, TypedDict
from ampel.types import ChannelId, Tag


class MetaRecord(TypedDict, total=False):
	"""
	A record of activity on tier documents.
	Very similar to JournalRecord for now
	"""

	#: Run(s) associated with this record
	run: int

	#: UNIX epoch of the activity
	ts: Union[int, float]

	#: Tier of the associated process
	tier: Literal[-1, 0, 1, 2, 3]

	#: Channels associated with the activity
	channel: Union[ChannelId, Sequence[ChannelId]]

	#: Trace ids associated with the creation / update of this document
	traceid: Dict[str, int]

	#: Name of the associated process
	process: Union[int, str]

	#: Free-form labels
	tag: Union[Tag, Sequence[Tag]]

	#: Status code of the associated process
	code: int

	#: Action code(s) built from :class:`~ampel.enum.MetaActionCode.MetaActionCode`
	action: int

	#: Duration of the process
	duration: Union[int, float]

	#: Free-form information
	extra: Dict[str, Any]
