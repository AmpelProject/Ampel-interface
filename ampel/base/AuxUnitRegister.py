#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/base/AuxUnitRegister.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 17.02.2021
# Last Modified Date: 17.02.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from importlib import import_module
from typing import Dict, Type, Any, Union, Optional, ClassVar, overload # type: ignore[attr-defined]
from ampel.type import T, check_class
from ampel.model.UnitModel import UnitModel
from ampel.base.AmpelBaseModel import AmpelBaseModel


class AuxUnitRegister:

	# References unit definitions of auxiliary units
	# allows units to load aux units by themselve or
	# aux units to load other aux units
	_defs: ClassVar[Dict[str, Any]] = {}

	@classmethod
	def initialize(cls, defs: Dict[str, Any]) -> None:
		cls._defs = defs

	@overload
	@classmethod
	def new_unit(cls, unit_model: UnitModel, *, sub_type: Type[T], **kwargs) -> T:
		...
	@overload
	@classmethod
	def new_unit(cls, unit_model: UnitModel, *, sub_type: None = ..., **kwargs) -> AmpelBaseModel:
		...

	@classmethod
	def new_unit(cls,
		unit_model: UnitModel, *, sub_type: Optional[Type[T]] = None, **kwargs
	) -> Union[T, AmpelBaseModel]:
		"""	:raises: ValueError is unit_model.config is not of type Optional[dict] """

		Klass = cls.get_aux_class(klass=unit_model.unit, sub_type=sub_type)
		if unit_model.config:
			if isinstance(unit_model.config, dict):
				return Klass(**{**unit_model.config, **kwargs}) # type: ignore[call-arg]
			raise ValueError("Auxiliary units cannot use config aliases")
		return Klass(**kwargs) # type: ignore[call-arg]


	@overload
	@classmethod
	def get_aux_class(cls, klass: Union[str, Type], *, sub_type: Type[T]) -> Type[T]:
		...

	@overload
	@classmethod
	def get_aux_class(cls, klass: Union[str, Type], *, sub_type: None = ...) -> Type[AmpelBaseModel]:
		...

	@classmethod
	def get_aux_class(cls, klass: Union[str, Type], *, sub_type: Optional[Type[T]] = None) -> Union[Type[T], Type[AmpelBaseModel]]:
		""" :raises: ValueError if unit is unknown """

		if isinstance(klass, str):
			if klass not in cls._defs:
				raise ValueError(f"Unknown auxiliary unit {klass}")

			fqn = cls._defs[klass]['fqn']
			# we 'redefine' klass and mypy doesn't like that, hence the ignores below
			klass = getattr(import_module(fqn), fqn.split('.')[-1])

		if sub_type:
			check_class(klass, sub_type) # type: ignore[arg-type]

		return klass # type: ignore[return-value]
