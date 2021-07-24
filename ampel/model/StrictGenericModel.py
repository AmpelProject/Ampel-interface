#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/model/StrictGenericModel.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 28.06.2021
# Last Modified Date: 28.06.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from pydantic import BaseModel, BaseConfig, Extra
from pydantic.generics import GenericModel
from ampel.config.AmpelConfig import AmpelConfig


class StrictGenericModel(GenericModel):

	class Config(BaseConfig):
		arbitrary_types_allowed = True
		allow_population_by_field_name = True
		validate_all = True
		extra = Extra.forbid

	def __init__(self, **kwargs) -> None:
		""" Raises validation errors if extra fields are present """

		if AmpelConfig._check_types:
			self.__config__.extra = Extra.forbid
			BaseModel.__init__(self, **kwargs)
			self.__config__.extra = Extra.allow
		else:
			m = BaseModel.construct(**kwargs)
			object.__setattr__(self, '__dict__', m.__dict__)
			object.__setattr__(self, '__fields_set__', m.__fields_set__)
