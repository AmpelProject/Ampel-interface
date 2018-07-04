#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/base/abstract/AbsAlertShaper.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 24.04.2018
# Last Modified Date: 04.07.2018
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from abc import ABC, abstractmethod

class AbsAlertShaper(ABC):


	@abstractmethod
	def shape(self, dict_instance):
		"""
		Should return a dict containing the following keywords:
		'pps': list of dicts
		'uls': list of dicts
		'ro_pps': tuple of MappingProxyType instances
		'ro_uls': tuple of MappingProxyType instances
		'tran_id': string or int
		'alert_id': long
		"""
		pass
