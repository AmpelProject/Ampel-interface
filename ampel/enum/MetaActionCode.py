#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/enum/MetaActionCode.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 01.09.2021
# Last Modified Date: 01.10.2021
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
	ADD_INGEST_TAG            = 64
	ADD_UNIT_TAG              = 128
	ADD_OTHER_TAG             = 1<<8
	PULL_TAG                  = 1<<9
	ADD_CHANNEL               = 1<<10
	PULL_CHANNEL              = 1<<11
	ADD_BODY                  = 1<<12
	PULL_BODY                 = 1<<13
	RESET_BODY                = 1<<14
	BUMP_STOCK_UPD            = 1<<15
