#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/enum/T2SysRunState.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 14.12.2017
# Last Modified Date: 11.02.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from enum import IntEnum
from ampel.enum.T2RunState import T2RunState

# flake8: noqa (E221)
class T2SysRunState(IntEnum): # cannot subclass T2RunState unfortunately
	"""
	Status values reserved for the ampel system.
	Typically set by ingesters or T2Processor.

	Potential state of:
		- :class:`~ampel.content.T2Document.T2Document`
		- :class:`~ampel.content.T2Record.T2Record`
	"""

	COMPLETED            = 0
	ERROR                = -1
	UNIT_RUN_AGAIN       = -2
	SYS_RUN_AGAIN        = -3
	TO_RUN               = -4
	TO_RUN_PRIO          = -5
	QUEUED               = -6
	RUNNING              = -7
	EXPORTED             = -8
	EXCEPTION            = -9
	TOO_MANY_TRIALS      = -10
	UNKNOWN_LINK         = -11
	UNKNOWN_CONFIG       = -12
	MISSING_DEPENDENCY   = -13
	MISSING_INFO         = -14
