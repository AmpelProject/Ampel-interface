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


	@classmethod
	@abstractmethod
	def get_tied_unit_names(cls) -> Optional[List[str]]:
		"""
		If None, all unit names are accepted.
		ex: return ["T2CatalogMatch"]
		"""

	def get_t2_dependencies(self) -> Sequence[UnitModel]:
		"""
		Get the dependencies of this instance, raising an exception if the
		configured values are incompatible with the expectations from :func:`get_tied_unit_names`.
	
		Examples::
		  
		  In []:
		  ...: import logging
		  ...: class A(AbsTiedT2Unit):
		  ...:     @classmethod
		  ...:     def get_tied_unit_names(cls):
		  ...:         return ['T2Unit1']

		  In []: a = A(logger=logging.getLogger(), t2_dependency={"unit": "T2Unit1", "config": 123})
		  In []: a.get_t2_dependencies()
		  Out[]: [UnitModel(unit='T2Unit1, config=123, override=None)]

		  In []: a = A(logger=logging.getLogger(), t2_dependency={"unit": "T2Unit2", "config": 123})
		  BadConfig: Unit T2Unit2 is not compatible with tied unit A

		::
		  
		  In []:
		  ...: class B(AbsTiedT2Unit):
		  ...:     t2_dependency: Sequence[StateT2Dependency]
		  ...:     @classmethod
		  ...:     def get_tied_unit_names(cls):
		  ...:         return ['T2Unit1', 'T2Unit2']
  
		  In []: b = B(logger=logging.getLogger(), t2_dependency=[{"unit": "T2Unit1", "config": 123}])
		  In []: b.get_t2_dependencies()
		  Out[]:
		  [StateT2Dependency(unit='T2Unit1', config=123, override=None, link_override=None),
		  UnitModel(unit='T2Unit2', config=None, override=None)]
		"""

		# No config, use defaults
		if self.t2_dependency is None:
			return [UnitModel(unit=el) for el in self.get_tied_unit_names()]

		# For mypy which otherwise complains later
		tied_unit_names = self.get_tied_unit_names()

		# Cast to sequence if need be
		t2_deps = [self.t2_dependency] if isinstance(self.t2_dependency, UnitModel) else self.t2_dependency

		# No restriction (meaning underlying t2 is capable of dealing with all kind of T2DocViews) - use config
		if tied_unit_names is None:
			return t2_deps

		ret = []

		# Check config using defined restrictions and potentialy complete
		for tied_unit_name in tied_unit_names:

			# Customization means also, that we can request multiple t2 views
			# of the same t2 unit with different config
			custom_dependencies = [el for el in t2_deps if el.unit == tied_unit_name]

			if not custom_dependencies:
				ret.append(UnitModel(unit=tied_unit_name))
				continue

			ret.extend(custom_dependencies)

		return ret
