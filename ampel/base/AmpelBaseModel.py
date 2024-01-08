#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/base/AmpelBaseModel.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                30.09.2018
# Last Modified Date:  05.01.2022
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from collections.abc import KeysView
from pydantic import BaseModel


class AmpelBaseModel(BaseModel):
	""" Raises validation errors if extra fields are present """

	model_config = {
		"arbitrary_types_allowed": True,
		"populate_by_name": True,
		"validate_default": True,
		"extra": "forbid"
	}

	@classmethod
	def __init_subclass__(cls, *args, **kwargs) -> None:
		for k, v in cls.__annotations__.items():
			# add implicit None default to unions containing None
			if (
				k not in cls.__dict__
				and get_origin(v) is UnionType
				and NoneType in get_args(v)
			):
				setattr(cls, k, None)
		super().__init_subclass__(*args, **kwargs)


	@classmethod
	def get_model_keys(cls) -> KeysView[str]:
		return cls.model_fields.keys()
