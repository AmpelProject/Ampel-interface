#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/base/AmpelBaseModel.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                30.09.2018
# Last Modified Date:  05.11.2025
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from types import UnionType
from typing import TYPE_CHECKING, Any, Union, get_args, get_origin

# NB: ModelMetaClass squirrels away generic args in its own
# __pydantic_model_args__ attribute, so we can't use typing.get_args() here
from pydantic import BaseModel
from pydantic._internal._generics import get_args as _internal_get_args
from pydantic._internal._generics import get_origin as _internal_get_origin

if TYPE_CHECKING:
	from pydantic.main import IncEx

NoneType = type(None)


class AmpelBaseModel(BaseModel):
	"""
	Base model for Ampel data structures with strict validation and flexible defaults.

	This underlying Pydantic BaseModel:
	- Forbids extra fields by default (`extra = "forbid"`), ensuring strict schema adherence.
	- Allows arbitrary types (e.g., custom classes) without requiring explicit validation.
	- Populates fields by name even when aliases are defined (`populate_by_name = True`).
	- Validates default values at model creation (`validate_default = True`).

	Additional features:
	- Automatically assigns `None` as the default for fields annotated with `Optional[...]` or
	 `Union[..., None]` if no default is explicitly provided in the class body.
	- Provides utility methods for introspecting generic model parameters:
		- `get_model_args()`: returns the type arguments used in a generic subclass.
		- `get_model_origin()`: returns the original generic base class.
		- `get_model_keys()`: returns the set of declared field names.

	Compatibility:
	- Overrides the deprecated `BaseModel.dict()` method to maintain compatibility with legacy code,
	  internally delegating to `model_dump()` with support for filtering options.
	"""

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
	def get_model_args(cls) -> tuple[type, ...]:
		return _internal_get_args(cls)

	@classmethod
	def get_model_origin(cls) -> None | type:
		return _internal_get_origin(cls)

	@classmethod
	def get_model_keys(cls) -> set[str]:
		return set(cls.model_fields.keys())
	
	# keep our own implementation of the (deprecated) BaseModel.dict() for
	# future compatibility
	def dict(self, *,
		include: "IncEx | None" = None,
		exclude: "IncEx | None" = None,
		by_alias: bool = False,
		exclude_unset: bool = False,
		exclude_defaults: bool = False,
		exclude_none: bool = False,
		warnings: bool = True,
	) -> dict[str, Any]:
		return self.model_dump(
			include=include,
			exclude=exclude,
			by_alias=by_alias,
			exclude_unset=exclude_unset,
			exclude_defaults=exclude_defaults,
			exclude_none=exclude_none,
			warnings=warnings,
		)
