#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/enum/EventCode.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                04.03.2021
# Last Modified Date:  25.07.2022
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from enum import IntEnum

# flake8: noqa (E221)
class EventCode(IntEnum):
	"""
	Potential state of :class:`~ampel.content.EventDocument.EventDocument`
	"""

	OK                        = 0
	RUNNING                   = 1
	UNSPECIFIED               = 2
	PRE_CHECK_EXIT            = 3
	ABORTED                   = 4

	ERROR                     = -1
	EXCEPTION                 = -2
