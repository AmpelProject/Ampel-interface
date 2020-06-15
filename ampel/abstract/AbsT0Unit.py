#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsT0Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 07.10.2019
# Last Modified Date: 15.06.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Any, List
from ampel.base import abstractmethod, AmpelABC, DataUnit
from ampel.content.DataPoint import DataPoint


class AbsT0Unit(AmpelABC, DataUnit, abstract=True):

	@abstractmethod
	def ampelize(self, arg: Any) -> List[DataPoint]:
		...
