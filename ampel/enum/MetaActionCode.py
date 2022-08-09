#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/enum/MetaActionCode.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                01.09.2021
# Last Modified Date:  10.10.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from enum import IntFlag

# flake8: noqa (E221)
class MetaActionCode(IntFlag):
	"""
	Potential code for 'action' field from :class:`~ampel.content.MetaActivity.MetaActivity`
	"""

	UNIT                      = 1
	CLI                       = 2
	EXTRA_META                = 4
	EXTRA_JOURNAL             = 8
	SET_CODE                  = 16
	SET_UNIT_CODE             = 32
	ADD_INGEST_TAG            = 64
	ADD_UNIT_TAG              = 128
	ADD_WORKER_TAG            = 1<<8
	ADD_OTHER_TAG             = 1<<9
	PULL_TAG                  = 1<<10
	ADD_CHANNEL               = 1<<11
	PULL_CHANNEL              = 1<<12
	ADD_BODY                  = 1<<13
	PULL_BODY                 = 1<<14
	RESET_BODY                = 1<<15
	ADD_T1_EXCL               = 1<<16
	BUMP_STOCK_UPD            = 1<<17
