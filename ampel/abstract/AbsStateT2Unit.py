#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsStateT2Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 28.12.2019
# Last Modified Date: 09.02.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Iterable
from ampel.base import abstractmethod, AmpelABC, DataUnit
from ampel.type import T2UnitResult
from ampel.content.Compound import Compound
from ampel.content.DataPoint import DataPoint


class AbsStateT2Unit(AmpelABC, DataUnit, abstract=True):
	"""
	A T2 unit bound to a :class:`~ampel.content.Compound.Compound` (state of a stock)
	"""

	@abstractmethod
	def run(self, compound: Compound, datapoints: Iterable[DataPoint]) -> T2UnitResult:
		"""
		Returned object should contain computed science results to be saved into the DB.

		.. note:: the returned dict must have only string keys and be BSON-encodable
		"""
