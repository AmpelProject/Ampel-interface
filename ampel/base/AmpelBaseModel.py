#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/base/AmpelBaseModel.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                30.09.2018
# Last Modified Date:  05.01.2022
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from collections.abc import KeysView
# from pydantic.v1 import BaseModel, BaseConfig, Extra
from pydantic import BaseModel, BaseConfig, Extra

class AmpelBaseModel(BaseModel):
	""" Raises validation errors if extra fields are present """

	model_config = {
		"arbitrary_types_allowed": True,
		"populate_by_name": True,
		"validate_default": True,
		"extra": "forbid"
	}

	def __init__(self, **kwargs) -> None:
		self.model_config["extra"] = "forbid"
		try:
			super().__init__(**kwargs)
		except Exception as e:
			raise TypeError(e) from None
		self.model_config["extra"] = "allow"


	@classmethod
	def get_model_keys(cls) -> KeysView[str]:
		return cls.model_fields.keys()
