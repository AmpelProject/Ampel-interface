#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/abstract/AbsStateT2Unit.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                28.12.2019
# Last Modified Date:  30.05.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from collections.abc import Iterable

from ampel.base.AmpelABC import AmpelABC
from ampel.base.decorator import abstractmethod
from ampel.base.LogicalUnit import LogicalUnit
from ampel.content.DataPoint import DataPoint
from ampel.content.T1Document import T1Document
from ampel.struct.UnitResult import UnitResult
from ampel.types import UBson


class AbsStateT2Unit(AmpelABC, LogicalUnit, abstract=True):
	"""
	A T2 unit bound to a :class:`~ampel.content.T1Document.T1Document` (state of a stock)
	"""

	@abstractmethod
	def process(self, compound: T1Document, datapoints: Iterable[DataPoint]) -> UBson | UnitResult:
		"""
		Returned object should contain computed science results to be saved into the DB.

		.. note:: the returned dict must have only string keys and be BSON-encodable
		"""
