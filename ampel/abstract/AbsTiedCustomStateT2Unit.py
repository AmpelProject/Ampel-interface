#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsTiedCustomStateT2Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 03.04.2020
# Last Modified Date: 08.06.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Iterable, Generic, Union, Sequence, Optional
from ampel.type import T, T2UnitResult
from ampel.base import abstractmethod, AmpelABC, DataUnit
from ampel.abstract.AbsTiedStateT2Unit import Dependency
from ampel.content.Compound import Compound
from ampel.content.DataPoint import DataPoint
from ampel.content.T2Record import T2Record


class AbsTiedCustomStateT2Unit(Generic[T], AmpelABC, DataUnit, abstract=True):
	"""
	Generic abstract class for state T2 units that depend on other T2 units.
	
	Known sub-classes: :class:`~ampel.abstract.AbsTiedLightCurveT2Unit.AbsTiedLightCurveT2Unit`
	"""

	#: Prerequisite T2s. Their output `T2Records <ampel.content.T2Record.T2Record>`_ will be supplied as arguments to :meth:`run`.
	dependency: Optional[Union[Dependency, Sequence[Dependency]]]

	# Note1: we want to enforce the implementation of an abstract *class method*
	# and hence have purposely omitted the first reflective argument
	@staticmethod
	@abstractmethod(force=True)
	def build(compound: Compound, datapoints: Iterable[DataPoint]) -> T:
		"""Build state type from compound and the datapoints it references"""
		...


	@abstractmethod
	def run(self, arg: T, t2_records: Sequence[T2Record]) -> T2UnitResult:
		"""
		Returned object should contain computed science results to be saved into the DB.
		Notes: dict must have only string keys and values must be bson encodable
		"""
