#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/base/abstract/AbsAlertFilter.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 14.12.2017
# Last Modified Date: 04.07.2018
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from ampel.base.abstract.AmpelABC import AmpelABC, abstractmethod
from ampel.base.AmpelAlert import AmpelAlert
from logging import Logger
from typing import Tuple, Set, Dict, Any, Optional

class AbsAlertFilter(metaclass=AmpelABC):
	"""
	Base class for T0 units
	"""

	#: Named resources required by this unit. This should be overridden by
	#: subclasses to register dependencies on local resources, e.g. URLs of
	#: catalog database servers
	resources : Tuple[str] = tuple()

	@abstractmethod
	def __init__(self, on_match_t2_units : Set[str],
	    base_config : Optional[Dict[str,str]] = None,
	    run_config : Optional[Dict[str,Any]] = None,
	    logger : Optional[Logger] = None):
		"""
		
		:param on_match_t2_units: names of T2 units to run on candidates that
		    pass this filter
		:param base_config: resources configured for this unit. The keys are
		    the elements of :py:attr:`resources`.
		:param run_config: unit-specific settings
		:param logger: logger to use for reporting output
		"""
		pass

	@abstractmethod
	def apply(self, ampel_alert : AmpelAlert) -> Optional[Set[str]]:
		"""
		Filter the candidate. Return `None` to drop the candidate, or the set
		of T2 units to run to accept it.
		
		:param ampel_alert: candidate photopoint
		"""
		pass

	# pylint: disable=no-member
	def get_version(self):
		return self.version
