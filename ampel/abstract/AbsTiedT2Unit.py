#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsTiedT2Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 06.02.2021
# Last Modified Date: 17.02.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import List, Sequence, Union, Optional
from ampel.base import abstractmethod, AmpelABC, DataUnit, BadConfig
from ampel.model.UnitModel import UnitModel


class AbsTiedT2Unit(AmpelABC, DataUnit, abstract=True):
	"""
	Top level abstract class for T2 units depending on other T2 units.
	"""

	t2_dependency: Union[UnitModel, Sequence[UnitModel]]

	def __init__(self, **kwargs):
		"""
		Dependency errors should not happen with config built by ampel (ConfigBuilder)
		but can happen in developers notebook
		"""
		if not kwargs.get("t2_dependency"):
			if self.get_tied_unit_names() is None:
				raise BadConfig(f"t2_dependency is mandatory since tied unit {self.__class__.__name__} sets no defaults")
			kwargs["t2_dependency"] = [UnitModel(unit=el) for el in self.get_tied_unit_names()]
			super().__init__(**kwargs)
		else:
			super().__init__(**kwargs)
			v = self.t2_dependency
			for t2_dep in ([v] if isinstance(v, UnitModel) else v):
				if t2_dep.unit not in self.get_tied_unit_names():
					raise BadConfig(f"Unit %s is not compatible with tied unit {self.__class__.__name__}" % t2_dep.unit)


	@abstractmethod
	@classmethod
	def get_tied_unit_names(cls) -> Optional[List[str]]:
		"""
		If None, all unit names are accepted.
		ex: return ["T2CatalogMatch"]
		"""
