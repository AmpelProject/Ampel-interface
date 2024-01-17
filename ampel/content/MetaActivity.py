#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/content/MetaActivity.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                07.10.2021
# Last Modified Date:  10.10.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from collections.abc import Sequence
from typing import TypedDict

from ampel.enum.MetaActionCode import MetaActionCode
from ampel.types import ChannelId, DataPointId, Tag


class MetaActivity(TypedDict, total=False):
	""" A record of activity on tier documents """

	#: Action code(s)
	action: MetaActionCode

	#: Free-form labels
	tag: Tag | Sequence[Tag]

	#: references dps exclusion (t1)
	excl: list[DataPointId]

	#: Document code (useful when t1_compute is performed on the fly)
	code: int

	#: Channel(s) associated with action
	channel: ChannelId | Sequence[ChannelId]
