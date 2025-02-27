#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/base/AuxUnitRegister.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                17.02.2021
# Last Modified Date:  08.11.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from importlib import import_module
from typing import Any, ClassVar, overload

from ampel.base.AmpelUnit import AmpelUnit
from ampel.config.AmpelConfig import AmpelConfig
from ampel.model.UnitModel import UnitModel
from ampel.types import T, check_class


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
	def new_unit(cls, model: UnitModel, *, sub_type: None = ..., **kwargs) -> AmpelUnit:
		...

	@classmethod
	def new_unit(cls, model: UnitModel, *, sub_type: None | type[T] = None, **kwargs) -> T | AmpelUnit:
		"""	:raises: ValueError is model.config is not of type None | dict """

		Klass = cls.get_aux_class(klass=model.unit, sub_type=sub_type)

		if model.config:
			if isinstance(model.config, dict):
				init_kwargs = model.config | kwargs
			else:
				raise ValueError("Auxiliary units cannot use config aliases")
		else:
			init_kwargs = kwargs

		unit = Klass(**init_kwargs)
		if hasattr(unit, "post_init"):
			unit.post_init()

		return unit


	@overload
	@classmethod
	def get_aux_class(cls, klass: str, *, sub_type: type[T]) -> type[T]:
		...

	@overload
	@classmethod
	def get_aux_class(cls, klass: str, *, sub_type: None = ...) -> type[AmpelUnit]:
		...

	@classmethod
	def get_aux_class(cls, klass: str, *, sub_type: None | type[T] = None) -> type[T | AmpelUnit]:
		""" :raises: ValueError if unit is unknown """

		if klass in cls._dyn:
			ret = cls._dyn[klass]
		elif klass in cls._defs:
			fqn = cls._defs[klass]['fqn']
			ret = getattr(import_module(fqn), klass)
		else:
			if not cls._defs:
				raise ValueError(
					f"Unknown auxiliary unit {klass}:"
					f"- make sure a context is loaded (requirement)\n"
				)
			raise ValueError(
				f"Unknown auxiliary unit {klass}:\n"
				f"- check your ampel conf to see if the unit is properly registered"
			)

		if sub_type:
			check_class(ret, sub_type)

		return ret
