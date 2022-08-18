#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/enum/DocumentCode.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                14.12.2017
# Last Modified Date:  17.05.2022
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from enum import IntEnum

# flake8: noqa (E221)
class DocumentCode(IntEnum):
	"""
	Potential code of:
		- :class:`~ampel.content.T1Document.T1Document`
		- :class:`~ampel.content.T2Document.T2Document`
		- :class:`~ampel.content.T3Document.T3Document`

	Negative code values are reserved for the ampel system
	(typically set by ingesters or processors).
	They hint that the associated ampel document is either in an
	erroneous state or not yet processed (pending state).

	Database queries can thus use {'code': {'$gte': 0}}
	to ensure the retrieval of valid processed data only.

	Codes are not combinable (IntEnum != IntFlag) meaning
	using DocumentCode.T2_UNKNOWN_CONFIG|DocumentCode.ERROR is not allowed.
	"""

	# General
	OK                        = 0
	NEW                       = -1
	ERROR                     = -2
	INTERNAL_ERROR            = -3
	EXCEPTION                 = -4
	RUNNING                   = -5
	RERUN_REQUESTED           = -6
	TOO_MANY_TRIALS           = -7

	# T1
	T1_NEW_PRIO               = -1000  # For now, std ingesters do not support this
	T1_UNKNOWN_CONFIG         = -1001

	# T2
	T2_NEW_PRIO               = -2000  # For now, std ingesters do not support this
	T2_PENDING_DEPENDENCY     = -2001
	T2_QUEUED                 = -2002
	T2_EXPORTED               = -2003
	T2_UNKNOWN_LINK           = -2004 # might be an ingester bugs, or uncommitted updates
	T2_UNKNOWN_CONFIG         = -2005
	T2_MISSING_DEPENDENCY     = -2006 # misconfiguration, or uncommitted updates
	T2_UNEXPECTED_DEPENDENCY  = -2007
	T2_MISSING_INFO           = -2008 # ingester bugs, or uncommitted updates
	T2_OUTDATED_CODE          = -2009

	# T3
	T3_CONTEXT_ERROR          = -3000 # error occured in context stage
	T3_SELECT_ERROR           = -3001 # error occured in select stage
	T3_LOAD_ERROR             = -3002 # error occured in load stage
	T3_COMPLEMENT_ERROR       = -3003 # error occured in complement stage
	T3_RUN_ERROR              = -3004 # error occured in run stage
