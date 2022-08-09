#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/base/AmpelGenericModel.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                30.09.2018
# Last Modified Date:  05.01.2022
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from collections.abc import KeysView
from pydantic import BaseConfig, Extra
from pydantic.generics import GenericModel

class AmpelGenericModel(GenericModel):
	""" Raises validation errors if extra fields are present """

	class Config(BaseConfig):
		arbitrary_types_allowed = True
		allow_population_by_field_name = True
		validate_all = True
		extra = Extra.forbid

	def __init__(self, **kwargs) -> None:
		self.__config__.extra = Extra.forbid
		try:
			super().__init__(**kwargs)
		except Exception as e:
			raise TypeError(e)
		self.__config__.extra = Extra.allow

	@classmethod
	def get_model_keys(cls) -> KeysView[str]:
		return cls.__fields__.keys()
