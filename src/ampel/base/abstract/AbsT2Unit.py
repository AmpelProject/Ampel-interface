#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/base/abstract/AbsT2Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 13.12.2017
# Last Modified Date: 04.07.2018
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from ampel.base.abstract.AmpelABC import AmpelABC, abstractmethod
from logging import Logger
from typing import Tuple, Dict, Any, Optional
from ampel.base.LightCurve import LightCurve

class AbsT2Unit(metaclass=AmpelABC):
	"""
	Base class for lightcurve processing
	"""

	#: Named resources required by this unit. See :py:attr:`ampel.base.abstract.AbsAlertFilter.AbsAlertFilter.resources`
	resources : Tuple[str] = tuple()

	@abstractmethod
	def __init__(self, logger : Logger, base_config : Optional[Dict[str,str]] = None):
		"""
		:param logger: logger to use for reporting output
		:param base_config: resources configured for this unit. The keys are
		    the elements of :py:attr:`resources`.
		"""
		pass

	@abstractmethod
	def run(self, light_curve : LightCurve, run_config : Optional[Dict[str,Any]] = None) -> Dict[str,Any]:
		"""
		Process a lightcurve for a single transient
		
		:returns: dictionary of results
		"""
		pass

	# pylint: disable=no-member
	def get_version(self):
		return self.version
