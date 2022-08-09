#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/content/MetaRecord.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                17.05.2021
# Last Modified Date:  07.10.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from typing import Literal, Any, TypedDict
from collections.abc import Sequence
from ampel.types import ChannelId, Tag
from ampel.content.MetaActivity import MetaActivity


class MetaRecord(TypedDict, total=False):
	""" A record of updates on tier documents """

	#: Run(s) associated with this record
	run: int

	#: UNIX epoch of the activity
	ts: int | float

	#: UNIX epoch after which the activity may be retried
	retry_after: int | float

	#: Tier of the associated process
	tier: Literal[-1, 0, 1, 2, 3]

	#: Channels associated with the activity
	channel: ChannelId | Sequence[ChannelId]

	#: Trace ids associated with the creation / update of this document
	traceid: dict[str, None | int]

	#: hash of potentially underlying job schema
	jobid: None | int

	#: Name of the associated process
	process: int | str

	#: Free-form labels
	tag: Tag | Sequence[Tag]

	#: Status code of the latest associated process
	code: int

	#: Actions performed on the associated document
	activity: Sequence[MetaActivity]

	#: Duration of the process
	duration: int | float

	#: Free-form information
	extra: dict[str, Any]
