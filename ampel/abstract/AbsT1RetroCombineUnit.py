#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/abstract/AbsT1RetroCombineUnit.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                17.06.2021
# Last Modified Date:  17.06.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from collections.abc import Iterable, Sequence

from ampel.base.AmpelABC import AmpelABC
from ampel.base.decorator import abstractmethod
from ampel.base.LogicalUnit import LogicalUnit
from ampel.content.DataPoint import DataPoint
from ampel.struct.T1CombineResult import T1CombineResult
from ampel.types import ChannelId, DataPointId


class AbsT1RetroCombineUnit(AmpelABC, LogicalUnit, abstract=True):
	""" A unit that combines datapoints """

	debug: bool = False
	access: list[int | str]
	policy: list[int | str]
	channel: None | ChannelId = None

	@abstractmethod
	def combine(self, datapoints: Iterable[DataPoint]) -> Sequence[Sequence[DataPointId]] | Sequence[T1CombineResult]:
		...
