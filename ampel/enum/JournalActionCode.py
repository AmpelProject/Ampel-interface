#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/enum/JournalActionCode.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 01.09.2021
# Last Modified Date: 05.09.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from enum import IntFlag

# flake8: noqa (E221)
class JournalActionCode(IntFlag):
	"""
	Potential code of field 'action' from :class:`~ampel.content.JournalRecord.JournalRecord` (62 different possible values)
	"""

	# T0
	T0_ADD_CHANNEL            = 1
	T0_PULL_CHANNEL           = 2
	T0_ADD_TAG                = 4
	T0_PULL_TAG               = 8
	T0_ADD_EXCL               = 64
	T0_PULL_EXCL              = 128

	# T1
	T1_ADD_CHANNEL            = 1<<8
	T1_PULL_CHANNEL           = 1<<9
	T1_ADD_BODY               = 1<<10
	T1_ADD_TAG                = 1<<11
	T1_PULL_TAG               = 1<<12
	T1_SET_CODE               = 1<<13
	T1_EXTRA_META             = 1<<14
	T1_EXTRA_JOURNAL          = 1<<15

	# T2
	T2_ADD_CHANNEL            = 1<<16
	T2_PULL_CHANNEL           = 1<<17
	T2_ADD_BODY               = 1<<18
	T2_ADD_TAG                = 1<<19
	T2_PULL_TAG               = 1<<20
	T2_SET_CODE               = 1<<21
	T2_EXTRA_JOURNAL          = 1<<22
	T2_EXPORT_DOC             = 1<<23
	T2_IMPORT_RESULT          = 1<<24

	# T3
	T3_ADD_DOC                = 1<<25

	# STOCK
	STOCK_ADD_CHANNEL         = 1<<26
	STOCK_PULL_CHANNEL        = 1<<27
	STOCK_BUMP_UPD            = 1<<28
	STOCK_ADD_TAG             = 1<<29
	STOCK_PULL_TAG            = 1<<30
	STOCK_ADD_NAME            = 1<<31
	STOCK_PULL_NAME           = 1<<32
	STOCK_SET_BODY            = 1<<33

	# CLI / OPS
	STOCK_RESET_BODY          = 1<<34
	T1_RESET_CODE             = 1<<35
	T1_RESET_BODY             = 1<<36
	T2_RESET_CODE             = 1<<37
	T2_RESET_BODY             = 1<<38
