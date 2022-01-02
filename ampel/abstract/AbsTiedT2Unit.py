#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/abstract/AbsTiedT2Unit.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                06.02.2021
# Last Modified Date:  31.05.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from typing import Sequence
from ampel.model.UnitModel import UnitModel
from ampel.base.AmpelABC import AmpelABC
from ampel.base.LogicalUnit import LogicalUnit


class AbsTiedT2Unit(AmpelABC, LogicalUnit, abstract=True):
	"""
	A T2 unit that depends on the results of other T2 units.
	"""

	#: Dependencies configuration for the underlying tied t2 unit
	#: Sub-class can add unit id constraints by parametrizing UnitModel
	t2_dependency: Sequence[UnitModel]

	def __init__(self, **kwargs):
		"""
		Dependency errors should not happen with config built by ampel (ConfigBuilder)
		but might happen in developers notebook
		"""

		if isinstance(kwargs.get("t2_dependency"), dict):
			kwargs["t2_dependency"] = [kwargs["t2_dependency"]]

		super().__init__(**kwargs)
