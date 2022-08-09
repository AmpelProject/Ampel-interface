#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/abstract/AbsT1CombineUnit.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                11.10.2019
# Last Modified Date:  14.06.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from collections.abc import Iterable, Sequence
from ampel.types import ChannelId, DataPointId
from ampel.base.AmpelABC import AmpelABC
from ampel.base.decorator import abstractmethod
from ampel.base.LogicalUnit import LogicalUnit
from ampel.content.DataPoint import DataPoint
from ampel.struct.T1CombineResult import T1CombineResult


class AbsT1CombineUnit(AmpelABC, LogicalUnit, abstract=True):
	""" A unit that combines datapoints """

	debug: bool = False
	access: Sequence[int | str]
	policy: Sequence[int | str]
	channel: None | ChannelId = None

	@abstractmethod
	def combine(self, datapoints: Iterable[DataPoint]) -> list[DataPointId] | T1CombineResult:
		...
