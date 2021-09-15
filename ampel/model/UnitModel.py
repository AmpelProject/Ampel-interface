#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/model/UnitModel.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 26.09.2019
# Last Modified Date: 15.09.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Dict, Optional, Any, Union, Generic
from ampel.types import T
from ampel.model.StrictGenericModel import StrictGenericModel


class UnitModel(StrictGenericModel, Generic[T]):
	"""
	Specification of a processing unit.
	Note: generic parametrization allows to constrain unit ids (ex: UnitModel[Literal[T2SNCosmo]])
	"""

	#: Name of ampel unit class
	unit: T

	#: - None: no config (use class defaults)
	#: - dict: config 'as is'
	#: - str: a corresponding alias key in the AmpelConfig must match the provided string
	#: - int: used internally for T2 units, a corresponding int key (AmpelConfig, base key 'confid') must match the provided integer
	config: Union[None, int, str, Dict[str, Any]]

	secrets: Union[None, Dict[str, Any]]

	#: Values to override in the config
	override: Optional[Dict[str, Any]]


	def dict(self, **kwargs):
		ret = super().dict(**kwargs)
		if 'secrets' in ret:
			del ret['secrets']
		return ret
