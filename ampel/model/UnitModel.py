#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/model/UnitModel.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                26.09.2019
# Last Modified Date:  15.09.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from collections.abc import Callable
from typing import Any, ClassVar, Generic, TypeVar

from pydantic import model_validator

from ampel.base.AmpelBaseModel import AmpelBaseModel

T = TypeVar("T", bound=str)



class UnitModel(AmpelBaseModel, Generic[T]):
	"""
	Specification of a processing unit.
	Note: generic parametrization allows to constrain unit ids (ex: UnitModel[Literal['T2SNCosmo']])
	"""

	#: Name of ampel unit class
	unit: T

	#: - None: no config (use class defaults)
	#: - dict: config 'as is'
	#: - str: a corresponding alias key in the AmpelConfig must match the provided string
	#: - int: used internally for T2 units, a corresponding int key (AmpelConfig, base key 'confid') must match the provided integer
	config: None | int | str | dict[str, Any] = None

	secrets: None | dict[str, Any] = None

	#: Values to override in the config
	override: None | dict[str, Any] = None

	# A shim to allow a validator to be configured dynamically
	# (pydantic.ModelMetaClass picks up validators at class definition time)
	@model_validator(mode="after")
	def post_validate(self) -> "UnitModel":
		if self.post_validate_hook:
			return self.post_validate_hook(self)
		return self

	post_validate_hook: ClassVar[None | Callable[["UnitModel"], "UnitModel"]] = None
