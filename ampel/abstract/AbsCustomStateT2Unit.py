#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsT2CustomUnit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 28.12.2019
# Last Modified Date: 11.02.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Iterable, Generic

from ampel.types import T
from ampel.abc import abstractmethod
from ampel.abstract.AbsDataUnit import AbsDataUnit
from ampel.content.Compound import Compound
from ampel.content.DataPoint import DataPoint
from ampel.t2.T2Result import T2Result


class AbsCustomStateT2Unit(Generic[T], AbsDataUnit, abstract=True):
	"""
	Generic top level abstract class for t2 units
	Known sub-class: ampel.abstract.AbsLightCurveT2Unit
	"""

	# Note1: we want to enforce the implementation of an abstract *class method*
	# and hence have purposely omitted the first reflective argument
	# Note2: method "of" returns a subclass of AbsT2MetaModel (ex: a LightCurve instance)
	# and we use "forward reference" type hints to avoid issues
	@staticmethod
	@abstractmethod(force=True)
	def of(compound: Compound, datapoints: Iterable[DataPoint]) -> T:
		...


	@abstractmethod
	def run(self, arg: T) -> T2Result:
		"""
		Returned T2Result dataclass should contain computed science results to be saved into the DB.
		Notes: dict must have only string keys and values must be bson encodable
		"""
