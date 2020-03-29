#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsStateT2Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 28.12.2019
# Last Modified Date: 11.02.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Iterable
from ampel.abc import abstractmethod, defaultmethod
from ampel.abstract.AbsDataUnit import AbsDataUnit
from ampel.content.Compound import Compound
from ampel.content.DataPoint import DataPoint
from ampel.t2.T2Result import T2Result


class AbsStateT2Unit(AbsDataUnit, abstract=True):
	"""
	Generic top level abstract class for t2 units
	Known sub-class: AbsLightCurveT2Unit
	"""

	@defaultmethod(check_super_call=True)
	def __init__(self, **kwargs) -> None:
		AbsDataUnit.__init__(self, **kwargs)
		self.post_init()


	def post_init(self) -> None:
		pass


	@abstractmethod
	def run(self, compound: Compound, datapoints: Iterable[DataPoint]) -> T2Result:
		"""
		Returned T2Result dataclass should contain computed science results to be saved into the DB.
		Notes: dict must have only string keys and values must be bson encodable
		"""
