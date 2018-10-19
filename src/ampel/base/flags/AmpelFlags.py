#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/base/flags/AmpelFlags.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 13.06.2018
# Last Modified Date: 04.07.2018
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from enum import IntFlag

class AmpelFlags(IntFlag):
	"""
	General Ampel flags
	"""
	INST_ZTF                 = 1 # 2**0
	SRC_IPAC                 = 2
	SRC_AMPEL                = 4
	RESERVED1                = 8
	RESERVED2                = 16
	RESERVED3                = 32
	RESERVED4                = 64
	RESERVED5                = 126
	RESERVED6                = 256
	RESERVED7                = 512
	RESERVED8                = 1024
	RESERVED9                = 2048
	RESERVED10               = 4096
	RESERVED11               = 8192
	RESERVED12               = 16384
	RESERVED13               = 32768 # 2**15
