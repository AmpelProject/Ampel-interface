#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/base/AuxUnitRegister.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 17.02.2021
# Last Modified Date: 05.08.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from importlib import import_module
from typing import Dict, Type, Any, Union, Optional, ClassVar, overload # type: ignore[attr-defined]
from ampel.types import T, check_class
from ampel.model.UnitModel import UnitModel
from ampel.base.AmpelBaseModel import AmpelBaseModel


class AuxUnitRegister:

	# References unit definitions of auxiliary units
	# allows units to load aux units by themselve or
	# aux units to load other aux units
	_defs: ClassVar[Dict[str, Any]] = {}
	_dyn: ClassVar[Dict[str, Any]] = {}

	@classmethod
	def initialize(cls, defs: Dict[str, Any]) -> None:
		cls._defs = defs

	@overload
	@classmethod
	def new_unit(cls, model: UnitModel, *, sub_type: Type[T], **kwargs) -> T:
		...
	@overload
	@classmethod
	def new_unit(cls, model: UnitModel, *, sub_type: None = ..., **kwargs) -> AmpelBaseModel:
		...

	@classmethod
	def new_unit(cls,
		model: UnitModel, *, sub_type: Optional[Type[T]] = None, **kwargs
	) -> Union[T, AmpelBaseModel]:
		"""	:raises: ValueError is model.config is not of type Optional[dict] """

		if model.unit in cls._dyn:
			Klass = cls._dyn[model.unit]
		else:
			Klass = cls.get_aux_class(klass=model.unit, sub_type=sub_type)

		if model.config:
			if isinstance(model.config, dict):
				return Klass(**(model.config | kwargs)) # type: ignore[call-arg]
			raise ValueError("Auxiliary units cannot use config aliases")

		return Klass(**kwargs) # type: ignore[call-arg]


	@overload
	@classmethod
	def get_aux_class(cls, klass: str, *, sub_type: Type[T]) -> Type[T]:
		...

	@overload
	@classmethod
	def get_aux_class(cls, klass: str, *, sub_type: None = ...) -> Type[AmpelBaseModel]:
		...

	@classmethod
	def get_aux_class(cls, klass: str, *, sub_type: Optional[Type[T]] = None) -> Union[Type[T], Type[AmpelBaseModel]]:
		""" :raises: ValueError if unit is unknown """

		if klass not in cls._defs:
			if not cls._defs:
				raise ValueError(
					f"Unknown auxiliary unit {klass}:"
					f"- make sure a context is loaded (requirement)\n"
				)
			else:
				raise ValueError(
					f"Unknown auxiliary unit {klass}:\n"
					f"- check your ampel conf to see if the unit is properly registered"
				)

		fqn = cls._defs[klass]['fqn']
		ret = getattr(import_module(fqn), klass)

		if sub_type:
			check_class(ret, sub_type)

		return ret
