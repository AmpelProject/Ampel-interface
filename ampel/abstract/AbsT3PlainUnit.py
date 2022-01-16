#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/abstract/AbsT3PlainUnit.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                08.12.2021
# Last Modified Date:  12.12.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from ampel.types import UBson
from ampel.view.T3Store import T3Store
from ampel.base.AmpelABC import AmpelABC
from ampel.base.decorator import abstractmethod
from ampel.base.LogicalUnit import LogicalUnit
from ampel.struct.UnitResult import UnitResult


class AbsT3PlainUnit(AmpelABC, LogicalUnit, abstract=True):
	""" Generic abstract class for T3 units receiving only a T3Store via the process method """

	@abstractmethod
	def process(self, t3s: T3Store) -> UBson | UnitResult:
		"""
		The content of the t3 store is dependent on:
		- the configuration of the 'include' option of the underlying t3 process
		- previously run t3 units if the option 'propagate' is activated
		"""
