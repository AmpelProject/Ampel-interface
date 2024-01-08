#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/base/AmpelBaseModel.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                30.09.2018
# Last Modified Date:  05.01.2022
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from collections.abc import KeysView
from types import UnionType
from typing import TYPE_CHECKING, Union, get_origin, get_args

from pydantic import BaseModel

if TYPE_CHECKING:
	from typing import Optional, Mapping, Any

	IntStr = int | str
	AbstractSetIntStr = set[str] | set[int] | dict[str, Any] | dict[int, Any]
	DictStrAny = dict[str, Any]
	MappingIntStrAny = Mapping[IntStr, Any]

NoneType = type(None)

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
				and get_origin(v) in (UnionType, Union)
				and NoneType in get_args(v)
			):
				setattr(cls, k, None)
		super().__init_subclass__(*args, **kwargs)


	@classmethod
	def get_model_keys(cls) -> KeysView[str]:
		return cls.model_fields.keys()
	
	# keep a facade of pydantic v1 BaseModel.dict() method
	def dict(
        self,
        *,
        include: "AbstractSetIntStr | None" = None,
        exclude: "AbstractSetIntStr | None" = None,
        by_alias: bool = False,
        skip_defaults: "Optional[bool]" = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> 'DictStrAny':
		return self.model_dump(
			include=include,
			exclude=exclude,
			by_alias=by_alias,
			exclude_unset=exclude_unset,
			exclude_defaults=exclude_defaults or (skip_defaults is True),
			exclude_none=exclude_none
		)
