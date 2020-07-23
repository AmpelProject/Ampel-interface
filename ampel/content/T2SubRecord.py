#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/content/T2SubRecord.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 13.01.2018
# Last Modified Date: 08.06.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Sequence, Union, Optional, TypedDict, Dict, Any
from ampel.type import ChannelId


class T2SubRecord(TypedDict, total=False):
	"""
	Dict crafted by T2Processor based on return value from t2 base unit
	(which can be either a T2RunState in case of errors or a T2UnitResult dict)
	"""
	# str is allowed to enable digest based version info
	version: Optional[Union[str, float]]
	ts: Union[float, int]
	duration: Union[float, int]
	run: int

	# Usually not set but required for "tied" t2 units
	channel: Union[ChannelId, Sequence[ChannelId]]

	# An integer 'error' can be returned by t2 units instead of a payload dict
	# Usually a T2RunState member but let's not be too restrictive here
	error: int
	msg: str

	# Whether the t2 result contained a journal update
	jup: bool
	result: Dict[str, Any]
