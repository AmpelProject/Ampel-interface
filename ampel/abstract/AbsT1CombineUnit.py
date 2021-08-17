#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsT1CombineUnit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 11.10.2019
# Last Modified Date: 14.06.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Union, Iterable, List, Optional
from ampel.types import ChannelId, DataPointId
from ampel.base.AmpelABC import AmpelABC
from ampel.base.decorator import abstractmethod
from ampel.base.LogicalUnit import LogicalUnit
from ampel.content.DataPoint import DataPoint
from ampel.struct.T1CombineResult import T1CombineResult


class AbsT1CombineUnit(AmpelABC, LogicalUnit, abstract=True):
	""" A unit that combines datapoints """

	debug: bool = False
	access: List[Union[int, str]]
	policy: List[Union[int, str]]
	channel: Optional[ChannelId] = None

	@abstractmethod
	def combine(self, datapoints: Iterable[DataPoint]) -> Union[List[DataPointId], T1CombineResult]:
		...
