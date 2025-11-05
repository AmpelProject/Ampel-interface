#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/abstract/AbsT4Unit.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                03.04.2023
# Last Modified Date:  01.11.2025
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from ampel.types import UBson
from ampel.base.decorator import abstractmethod
from ampel.base.LogicalUnit import LogicalUnit
from ampel.struct.UnitResult import UnitResult


class AbsT4Unit(LogicalUnit, abstract=True):
	""" Abstract class for logical T4 units """

	@abstractmethod
	def do(self) -> UBson | UnitResult:
		...
