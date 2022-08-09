#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/abstract/AbsT1ComputeUnit.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                13.05.2021
# Last Modified Date:  13.05.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from typing import Tuple
from ampel.types import UBson, StockId
from ampel.base.AmpelABC import AmpelABC
from ampel.base.decorator import abstractmethod
from ampel.base.LogicalUnit import LogicalUnit
from ampel.content.DataPoint import DataPoint
from ampel.struct.UnitResult import UnitResult
	

class AbsT1ComputeUnit(AmpelABC, LogicalUnit, abstract=True):

	@abstractmethod
	def compute(self, datapoints: list[DataPoint]) -> tuple[UBson | UnitResult, StockId]:
		...
