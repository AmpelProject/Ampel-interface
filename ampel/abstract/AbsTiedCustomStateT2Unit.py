#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/abstract/AbsTiedCustomStateT2Unit.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                03.04.2020
# Last Modified Date:  28.09.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from typing import Generic, TypeVar
from collections.abc import Iterable, Sequence
from ampel.types import T, UBson
from ampel.struct.UnitResult import UnitResult
from ampel.view.T2DocView import T2DocView
from ampel.content.DataPoint import DataPoint
from ampel.base.decorator import abstractmethod
from ampel.content.T1Document import T1Document
from ampel.abstract.AbsTiedT2Unit import AbsTiedT2Unit
from ampel.model.StateT2Dependency import StateT2Dependency

U = TypeVar("U")


class AbsTiedCustomStateT2Unit(Generic[T, U], AbsTiedT2Unit, abstract=True):
	"""
	A T2 unit bound to a custom type *constructed* from a :class:`compound <ampel.content.T1Document.T1Document>`,
	as well as the results of other T2 units.

	Known subclass: :class:`~ampel.abstract.AbsTiedLightCurveT2Unit.AbsTiedLightCurveT2Unit`
	"""

	t2_dependency: Sequence[StateT2Dependency[U]]
	

	# Note: we want to enforce the implementation of an abstract *class method*
	# and hence have purposely omitted the first reflective argument
	@staticmethod
	@abstractmethod(force=True)
	def build(compound: T1Document, datapoints: Iterable[DataPoint]) -> T:
		"""
		Create the parametrized type using compound and datapoints.
		For example, AbsTiedCustomStateT2Unit[LightCurve] would return a
		:class:`~ampel.view.LightCurve.LightCurve` instance.
		"""
		...

	@abstractmethod
	def process(self, arg: T, t2_views: Sequence[T2DocView]) -> UBson | UnitResult:
		"""
		Returned object should contain computed science results to be saved into the DB.

		.. note:: the returned dict must have only string keys and be BSON-encodable
		"""
