#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsT1ComputeUnit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 13.05.2021
# Last Modified Date: 13.05.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import List, Union, Tuple
from ampel.types import UBson, StockId
from ampel.base.AmpelABC import AmpelABC
from ampel.base.decorator import abstractmethod
from ampel.base.LogicalUnit import LogicalUnit
from ampel.content.DataPoint import DataPoint
from ampel.struct.UnitResult import UnitResult
	

class AbsT1ComputeUnit(AmpelABC, LogicalUnit, abstract=True):

	@abstractmethod
	def compute(self, datapoints: List[DataPoint]) -> Tuple[Union[UBson, UnitResult], StockId]:
		...
