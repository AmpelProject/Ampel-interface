#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsTiedPointT2Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 16.02.2021
# Last Modified Date: 28.09.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Union, Sequence
from ampel.types import UBson
from ampel.struct.UnitResult import UnitResult
from ampel.view.T2DocView import T2DocView
from ampel.content.DataPoint import DataPoint
from ampel.base.decorator import abstractmethod
from ampel.abstract.AbsTiedT2Unit import AbsTiedT2Unit


class AbsTiedPointT2Unit(AbsTiedT2Unit, abstract=True):
	"""
	A T2 unit bound to a :class:`~ampel.content.DataPoint.DataPoint` as well
	as the results of other T2 units

	Note that the implementing class can customize the default ingestion behavior
	by defining the class variable 'eligible'.
	See AbsPointT2Unit and DPSelection docstrings for more info
	"""

	@abstractmethod
	def process(self, datapoint: DataPoint, t2_views: Sequence[T2DocView]) -> Union[UBson, UnitResult]:
		"""
		Returned object should contain computed science results to be saved into the DB.

		.. note:: the returned dict must have only string keys and be BSON-encodable
		"""
