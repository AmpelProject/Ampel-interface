#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/enum/MetaActionCode.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 01.09.2021
# Last Modified Date: 05.09.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from enum import IntFlag

# flake8: noqa (E221)
class MetaActionCode(IntFlag):
	"""
	Potential code of field 'action' from :class:`~ampel.content.MetaRecord.MetaRecord` (62 different possible values)
	"""

	UNIT                      = 1
	CLI                       = 2
	EXTRA_META                = 4
	EXTRA_JOURNAL             = 8
	SET_CODE                  = 16
	ADD_TAG                   = 32
	PULL_TAG                  = 64
	ADD_CHANNEL               = 128
	PULL_CHANNEL              = 1<<8
	ADD_BODY                  = 1<<9
	PULL_BODY                 = 1<<10
	RESET_BODY                = 1<<11
	BUMP_STOCK_UPD            = 1<<12
