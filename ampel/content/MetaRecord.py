#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/content/MetaRecord.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 17.05.2021
# Last Modified Date: 07.10.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Optional, Union, Literal, Any, TypedDict
from collections.abc import Sequence
from ampel.types import ChannelId, Tag
from ampel.content.MetaActivity import MetaActivity


class MetaRecord(TypedDict, total=False):
	""" A record of updates on tier documents """

	#: Run(s) associated with this record
	run: int

	#: UNIX epoch of the activity
	ts: Union[int, float]

	#: UNIX epoch after which the activity may be retried
	retry_after: Union[int, float]

	#: Tier of the associated process
	tier: Literal[-1, 0, 1, 2, 3]

	#: Channels associated with the activity
	channel: Union[ChannelId, Sequence[ChannelId]]

	#: Trace ids associated with the creation / update of this document
	traceid: dict[str, Optional[int]]

	#: Name of the associated process
	process: Union[int, str]

	#: Free-form labels
	tag: Union[Tag, Sequence[Tag]]

	#: Status code of the latest associated process
	code: int

	#: Actions performed on the associated document
	activity: Sequence[MetaActivity]

	#: Duration of the process
	duration: Union[int, float]

	#: Free-form information
	extra: dict[str, Any]
