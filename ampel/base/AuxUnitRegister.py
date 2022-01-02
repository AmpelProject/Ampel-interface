#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/base/AuxUnitRegister.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                17.02.2021
# Last Modified Date:  08.11.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from importlib import import_module
from typing import Any, ClassVar, overload # type: ignore[attr-defined]
from ampel.types import T, check_class
from ampel.model.UnitModel import UnitModel
from ampel.base.AmpelBaseModel import AmpelBaseModel
from ampel.config.AmpelConfig import AmpelConfig


class AuxUnitRegister:

	# References unit definitions of auxiliary units
	# allows units to load aux units by themselve or
	# aux units to load other aux units
	_defs: ClassVar[dict[str, Any]] = {}
	_dyn: ClassVar[dict[str, Any]] = {}

	@classmethod
	def initialize(cls, config: AmpelConfig) -> None:
		cls._defs = {
			k: v for k, v in config.get("unit", ret_type=dict, raise_exc=True).items()
			if 'ContextUnit' not in v.get('base', []) and 'LogicalUnit' not in v.get('base', [])
		}

	@overload
	@classmethod
	def new_unit(cls, model: UnitModel, *, sub_type: type[T], **kwargs) -> T:
		...
	@overload
	@classmethod
	def new_unit(cls, model: UnitModel, *, sub_type: None = ..., **kwargs) -> AmpelBaseModel:
		...

	@classmethod
	def new_unit(cls,
		model: UnitModel, *, sub_type: None | type[T] = None, **kwargs
	) -> T | AmpelBaseModel:
		"""	:raises: ValueError is model.config is not of type None | dict """

		if model.unit in cls._dyn:
			Klass = cls._dyn[model.unit]
		else:
			Klass = cls.get_aux_class(klass=model.unit, sub_type=sub_type)

		if model.config:
			if isinstance(model.config, dict):
				return Klass(**(model.config | kwargs)) # type: ignore[call-arg]
			raise ValueError("Auxiliary units cannot use config aliases")

		unit = Klass(**kwargs) # type: ignore[call-arg]
		if hasattr(unit, "post_init"):
			unit.post_init() # type: ignore[union-attr]

		return unit


	@overload
	@classmethod
	def get_aux_class(cls, klass: str, *, sub_type: type[T]) -> type[T]:
		...

	@overload
	@classmethod
	def get_aux_class(cls, klass: str, *, sub_type: None = ...) -> type[AmpelBaseModel]:
		...

	@classmethod
	def get_aux_class(cls, klass: str, *, sub_type: None | type[T] = None) -> type[T] | type[AmpelBaseModel]:
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
