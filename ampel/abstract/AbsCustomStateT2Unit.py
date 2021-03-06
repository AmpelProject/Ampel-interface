#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsCustomStateT2Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 28.12.2019
# Last Modified Date: 08.06.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Sequence, Generic
from ampel.type import T, T2UnitResult
from ampel.base import abstractmethod, AmpelABC, DataUnit
from ampel.content.Compound import Compound
from ampel.content.DataPoint import DataPoint


class AbsCustomStateT2Unit(Generic[T], AmpelABC, DataUnit, abstract=True):
	"""
	Generic top level abstract class for t2 units
	Known sub-class: ampel.abstract.AbsLightCurveT2Unit
	"""

	# Note1: we want to enforce the implementation of an abstract *class method*
	# and hence have purposely omitted the first reflective argument
	@staticmethod
	@abstractmethod(force=True)
	def build(compound: Compound, datapoints: Sequence[DataPoint]) -> T:
		...


	@abstractmethod
	def run(self, arg: T) -> T2UnitResult:
		"""
		Returned object should contain computed science results to be saved into the DB.
		Notes: dict must have only string keys and values must be bson encodable
		"""
