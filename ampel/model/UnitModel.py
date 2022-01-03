#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/model/UnitModel.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                26.09.2019
# Last Modified Date:  15.09.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from typing import Any, Generic
from ampel.types import T
from ampel.base.AmpelBaseModel import AmpelBaseModel


class UnitModel(Generic[T], AmpelBaseModel):
	"""
	Specification of a processing unit.
	Note: generic parametrization allows to constrain unit ids (ex: UnitModel[Literal[T2SNCosmo]])
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


	def dict(
		self,
		include: None | set[str]=None,
		exclude: None | set[str]={"secrets"},
		exclude_defaults: bool=False,
		exclude_unset: bool=False,
	) -> dict[str, Any]:
		return super().dict(
			include=include,
			exclude=exclude,
			exclude_defaults=exclude_defaults,
			exclude_unset=exclude_unset
		)
