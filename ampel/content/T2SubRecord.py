#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/content/T2SubRecord.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 13.01.2018
# Last Modified Date: 10.02.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Sequence, Union, Optional, TypedDict, Dict, Any
from ampel.type import ChannelId


class T2SubRecord(TypedDict, total=False):
	"""
	Dict crafted by :class:`~ampel.t2.T2Processor.T2Processor` based on return
	value from t2 base unit, which can be either

	- a BSON serializable-dict,
	- a tuple of dict, :class:`~ampel.struct.JournalExtra.JournalExtra`,
	- or, if an error occurred, a :class:`~ampel.t2.T2RunState.T2RunState`.

	This is a dict containing 1 or more of the following items:
	"""
	# str is allowed to enable digest based version info
	version: Optional[Union[str, float]]
	#: UNIX epoch when :meth:`run` was invoked
	ts: Union[float, int]
	#: Duration of :meth:`run`, in seconds
	duration: Union[float, int]
	#: Identifier of the :class:`~ampel.t2.T2Processor.T2Processor` invocation
	#: that created this
	run: int

	#: Usually not set but required for "tied" t2 units
	channel: Sequence[ChannelId]

	#: An integer 'status' can be returned by t2 units instead of a payload dict.
	#: This will usually be a member of :class:`~ampel.t2.T2RunState.T2RunState`.
	status: Optional[int]

	#: Human-readable explanation of the error reason.
	msg: str

	#: True if the t2 result contained a :class:`~ampel.struct.JournalExtra.JournalExtra`
	jup: bool
	#: Payload returned by :meth:`run`.
	result: Dict[str, Any]
