#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/content/MetaActivity.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 07.10.2021
# Last Modified Date: 08.10.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Sequence, Union, TypedDict
from ampel.types import ChannelId, Tag
from ampel.enum.MetaActionCode import MetaActionCode


class MetaActivity(TypedDict, total=False):
	""" A record of activity on tier documents """

	#: Action code(s)
	action: MetaActionCode

	#: Free-form labels
	tag: Union[Tag, Sequence[Tag]]

	#: Channel(s) associated with action
	channel: Union[ChannelId, Sequence[ChannelId]]
