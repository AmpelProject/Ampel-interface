#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/base/abstract/AbsAlertFilter.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 14.12.2017
# Last Modified Date: 04.07.2018
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from ampel.base.abstract.AmpelABC import AmpelABC, abstractmethod

class AbsAlertFilter(metaclass=AmpelABC):


	@abstractmethod
	def __init__(self, on_match_t2_units, base_config=None, run_config=None, logger=None):
		pass

	@abstractmethod
	def apply(self, ampel_alert):
		pass

	# pylint: disable=no-member
	def get_version(self):
		return self.version
