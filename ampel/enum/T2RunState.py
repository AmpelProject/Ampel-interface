#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/enum/T2RunState.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 14.12.2017
# Last Modified Date: 11.02.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from enum import IntEnum

# flake8: noqa (E221)
class T2RunState(IntEnum):
	"""
	Status values usable by T2 units (along with any positive value)
	Potential state of:
	
	- :class:`~ampel.content.T2Document.T2Document`
	- :class:`~ampel.content.T2Record.T2Record`
	"""

	COMPLETED                 = 0
	# First 1000 negative values are system reserved
	ERROR                     = -1000
	MISSING_INFO              = -1001
	UNEXPECTED_DEPENDENCY     = -1002
	RERUN_REQUESTED           = -1003
	OUTDATED_CODE             = -1004
