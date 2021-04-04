#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/enum/EventCode.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 04.03.2021
# Last Modified Date: 04.03.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from enum import IntEnum

# flake8: noqa (E221)
class EventCode(IntEnum):
	"""
	Potential state of :class:`~ampel.content.EventDocument.EventDocument`
	"""

	OK                        = 0
	ERROR                     = -1
	EXCEPTION                 = -2
