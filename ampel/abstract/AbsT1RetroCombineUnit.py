#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsT1RetroCombineUnit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 17.06.2021
# Last Modified Date: 17.06.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Union
from collections.abc import Iterable
from ampel.types import ChannelId, DataPointId
from ampel.base.AmpelABC import AmpelABC
from ampel.base.decorator import abstractmethod
from ampel.base.LogicalUnit import LogicalUnit
from ampel.content.DataPoint import DataPoint
from ampel.struct.T1CombineResult import T1CombineResult


class AbsT1RetroCombineUnit(AmpelABC, LogicalUnit, abstract=True):
	""" A unit that combines datapoints """

	debug: bool = False
	channel: ChannelId
	access: list[Union[int, str]]
	policy: list[Union[int, str]]

	@abstractmethod
	def combine(self, datapoints: Iterable[DataPoint]) -> Union[list[list[DataPointId]], list[T1CombineResult]]:
		...
