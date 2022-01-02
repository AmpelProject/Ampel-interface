#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/abstract/AbsCustomStateT2Unit.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                28.12.2019
# Last Modified Date:  03.04.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from typing import Generic
from collections.abc import Iterable
from ampel.types import T, UBson
from ampel.struct.UnitResult import UnitResult
from ampel.content.T1Document import T1Document
from ampel.content.DataPoint import DataPoint
from ampel.base.AmpelABC import AmpelABC
from ampel.base.decorator import abstractmethod
from ampel.base.LogicalUnit import LogicalUnit


class AbsCustomStateT2Unit(Generic[T], AmpelABC, LogicalUnit, abstract=True):
	"""
	A T2 unit bound to a custom type *constructed* from a :class:`compound <ampel.content.T1Document.T1Document>`

	Known subclass: :class:`~ampel.abstract.AbsLightCurveT2Unit.AbsLightCurveT2Unit`
	"""

	# We want to enforce the implementation of an abstract *class method*
	# and hence have purposely omitted the first reflective argument
	@staticmethod
	@abstractmethod(force=True)
	def build(compound: T1Document, datapoints: Iterable[DataPoint]) -> T:
		"""
		Create the parametrized type using compound and datapoints.
		For example, AbsCustomStateT2Unit[LightCurve] would return a
		:class:`~ampel.view.LightCurve.LightCurve` instance.
		"""
		...


	@abstractmethod
	def process(self, arg: T) -> UBson | UnitResult:
		"""
		Returned object should contain computed science results to be saved into the DB.

		.. note:: the returned dict must have only string keys and be BSON-encodable
		"""
