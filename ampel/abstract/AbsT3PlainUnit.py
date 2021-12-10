#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsT3PlainUnit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 08.12.2021
# Last Modified Date: 08.12.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Union, Optional
from ampel.types import UBson
from ampel.view.T3Store import T3Store
from ampel.base.AmpelABC import AmpelABC
from ampel.base.decorator import abstractmethod
from ampel.base.LogicalUnit import LogicalUnit
from ampel.struct.UnitResult import UnitResult


class AbsT3PlainUnit(AmpelABC, LogicalUnit, abstract=True):
	""" Generic abstract class for T3 units receiving only a T3Store via the process method """

	@abstractmethod
	def process(self, t3s: Optional[T3Store] = None) -> Union[UBson, UnitResult]:
		"""
		Optional parameter t3s provides a t3 store containing t3 views.
		The content of the store is dependent on the configuration of the 'supply' option
		of the underlying t3 process config.
		"""
