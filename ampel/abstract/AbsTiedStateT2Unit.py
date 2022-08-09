#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/abstract/AbsTiedStateT2Unit.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                11.03.2020
# Last Modified Date:  28.09.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from typing import Generic
from collections.abc import Sequence
from ampel.types import UBson, T
from ampel.struct.UnitResult import UnitResult
from ampel.view.T2DocView import T2DocView
from ampel.base.decorator import abstractmethod
from ampel.content.T1Document import T1Document
from ampel.content.DataPoint import DataPoint
from ampel.abstract.AbsTiedT2Unit import AbsTiedT2Unit
from ampel.model.StateT2Dependency import StateT2Dependency


class AbsTiedStateT2Unit(Generic[T], AbsTiedT2Unit, abstract=True):
	"""
	A T2 unit bound to a :class:`~ampel.content.T1Document.T1Document` (state of a stock),
	as well as the results of other T2 units
	"""

	t2_dependency: Sequence[StateT2Dependency[T]]

	@abstractmethod
	def process(self,
		compound: T1Document,
		datapoints: Sequence[DataPoint],
		t2_views: Sequence[T2DocView]
	) -> UBson | UnitResult:
		"""
		Returned object should contain computed science results to be saved into the DB.

		.. note:: the returned dict must have only string keys and be BSON-encodable
		"""
