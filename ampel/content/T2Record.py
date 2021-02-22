#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/content/T2Record.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 13.01.2018
# Last Modified Date: 12.02.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Union, TypedDict, Dict, List, Any


class T2Record(TypedDict, total=False):
	"""
	Dict crafted by :class:`~ampel.t2.T2Processor.T2Processor` based on return
	value from t2 base unit, which can be either:

	- a BSON serializable-dict,
	- a :class:`~ampel.struct.T2BroadUnitResult.T2BroadUnitResult`,
	- a standardized status: :class:`~ampel.enum.T2RunState.T2RunState` (negative number).
	- a positive number as unit-specific status

	This is a dict containing 1 or more of the following items:
	"""
	# str is allowed to enable digest based version info
	version: Union[str, float]

	#: UNIX epoch when :meth:`run` was invoked
	ts: Union[float, int]

	#: Duration of :meth:`run`, in seconds
	duration: Union[float, int]

	#: Identifier of the :class:`~ampel.t2.T2Processor.T2Processor` invocation
	#: that created this
	run: int

	#: An integer 'status' can be returned by t2 units instead of a payload dict.
	#: Negative numbers shall be of :class:`~ampel.enum.T2RunState.T2RunState`
	#: Positive numbers are for T2-unit-specific status
	status: int

	#: Human-readable explanation of the reason for a potential error.
	msg: str

	#: True if the t2 result contained a :class:`~ampel.struct.JournalTweak.JournalTweak`
	jup: bool

	#: Payload returned by :meth:`run`.
	result: Union[Dict[str, Any], List[Dict[str, Any]]]
