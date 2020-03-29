#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsT0Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 07.10.2019
# Last Modified Date: 14.03.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from ampel.abc import abstractmethod
from ampel.abstract.AbsDataUnit import AbsDataUnit
from ampel.content.DataPoint import DataPoint
from typing import Any, List

class AbsT0Unit(AbsDataUnit, abstract=True):

	@abstractmethod
	def ampelize(self, arg: Any) -> List[DataPoint]:
		...
