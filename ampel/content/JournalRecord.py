#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/content/JournalRecord.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 12.12.2019
# Last Modified Date: 08.06.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Sequence, Union, Optional, Literal, Any, Dict, TypedDict, List
from ampel.type import ChannelId, Tag

class JournalRecord(TypedDict, total=False):

	tier: Literal[0, 1, 2, 3]
	ts: Union[int, float]
	channel: Union[ChannelId, Sequence[ChannelId]]
	process: Union[int, str]
	tag: Optional[Union[Tag, Sequence[Tag]]]
	status: Optional[int]
	unit: Optional[Union[int, str]]
	doc: Optional[Union[int, bytes]]
	run: Union[int, List[int]]
	extra: Optional[Dict[str, Any]]
