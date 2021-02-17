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
	Status values between 0 and -1000 are reserved for the ampel system.
	(Typically set by ingesters or T2Processor)

	Potential state of:
		- :class:`~ampel.content.T2Document.T2Document`
		- :class:`~ampel.content.T2Record.T2Record`
	"""

	COMPLETED                 = 0
	NEW                       = -1
	NEW_PRIO                  = -2  # For now, std ingesters do not support this
	RUNNING                   = -3
	PENDING_DEPENDENCY        = -4
	EXCEPTION                 = -5
	QUEUED                    = -6
	EXPORTED                  = -7
	TOO_MANY_TRIALS           = -8

	# Might be due to ingester bugs
	UNKNOWN_LINK              = -9
	UNKNOWN_CONFIG            = -10
	MISSING_DEPENDENCY        = -11
	BAD_DEPENDENCY_CONFIG     = -12

	# Copied from T2RunState
	# -> python does not support enum inheritance
	ERROR                     = -1000
	MISSING_INFO              = -1001
	UNEXPECTED_DEPENDENCY     = -1002
	RERUN_REQUESTED           = -1003
	OUTDATED_CODE             = -1004
