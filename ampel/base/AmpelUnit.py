#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/base/AmpelUnit.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                07.10.2019
# Last Modified Date:  09.01.2022
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from functools import partial
from types import MemberDescriptorType, UnionType
from typing import TYPE_CHECKING, Any, ClassVar, Union, get_args, get_origin

from pydantic import BaseModel, ValidationError, create_model

from ampel.base.AmpelBaseModel import AmpelBaseModel
from ampel.secret.Secret import Secret
from ampel.types import TRACELESS, Traceless

ttf = type(Traceless)
NoneType = type(None)

if TYPE_CHECKING:
	from ampel.base.AmpelBaseModel import IncEx

class AmpelUnit:
	"""
	This class supports setting slots values through constructor parameters (they will be type checked as well).
	Type checking can be deactivated globally by setting ampel.types.do_type_check to False
	"""

	_model: type[BaseModel]
	_annots: ClassVar[dict[str, Any]] = {}
	_defaults: ClassVar[dict[str, Any]] = {}
	_slot_defaults: ClassVar[dict[str, Any]] = {}
	_aks: ClassVar[set[str]] = set() # annotation keys
	_sks: ClassVar[set[str]] = set() # slots keys
	_exclude_unset: set[str]


	@classmethod
	def __init_subclass__(cls, *args, **kwargs) -> None:
		"""
		Combines annotations & default values of this class with the one defined in sub-classes.
		Has similarities with the newly introduced typing.get_type_hints() function.
		"""
		super().__init_subclass__(*args, **kwargs)

		joined_ann = {
			k: v for k, v in cls._annots.items()
			if not (k[0] == '_' or 'ClassVar' in str(v))
		}
		joined_defaults = cls._defaults.copy()
		joined_sks = cls._sks.copy()
		joined_aks = cls._aks.copy()
		# Needed for when sub-classes inherit both AmpelUnit and AmpelBaseModel/BaseModel
		field_keys: dict[str, Any] = getattr(cls, 'model_fields', dict())

		for base in reversed(cls.mro()):
			if ann := getattr(base, '__annotations__', {}):
				defs = getattr(base, '__dict__', {})
				for k, v in ann.items():
					if k == '__slots__' or k[0] == '_' or 'ClassVar' in str(v):
						continue

					joined_ann[k] = v # update merged annotations
					joined_aks.add(k) # update set of known attribute names

					if k in defs:
						if type(defs[k]) is MemberDescriptorType: # is a slot
							if k in cls._slot_defaults:
								joined_defaults[k] = cls._slot_defaults[k]
							continue
						joined_defaults[k] = base.__dict__[k]
					# if None |  with no default
					elif get_origin(v) in (Union, UnionType) and NoneType in get_args(v) and k not in joined_defaults:
						joined_defaults[k] = None
					elif k in cls._slot_defaults:
						joined_defaults[k] = cls._slot_defaults[k]
					elif k in field_keys:
						fields = cls.model_fields # type: ignore[attr-defined]
						if fields[k].is_required() is False:
							joined_defaults[k] = fields[k].default


			# allow subclasses to change default value without supplying a new annotation
			for k, v in getattr(base, '__dict__', {}).items():
				if k in joined_ann and k not in ann:
					joined_defaults[k] = v

			# if we inherit from AmpelBaseModel, add model_fields from base class
			if field_keys:
				field_keys.update(getattr(base, 'model_fields', dict()))

		if slots := getattr(cls, '__slots__', None):
			joined_sks.update(slots)

		for el in (
			('_annots', joined_ann), ('_defaults', joined_defaults),
			('_aks', joined_aks), ('_sks', joined_sks), ('_model', None)
		):
			setattr(cls, el[0], el[1])


	@classmethod
	def _create_model(cls, omit_traceless: bool = False) -> type[BaseModel]:

		defs = cls._defaults
		if hasattr(cls, 'model_fields'):
			cls.model_fields.clear()

		if omit_traceless:
			ttf = type(Traceless)
			kwargs = {
				k: (v, defs.get(k, ...))
				for k, v in cls._annots.items()
				if not (type(v) is ttf and v.__metadata__[0] == TRACELESS)
			}
		else:
			kwargs = {
				k: (v, defs.get(k, ...))
				for k, v in cls._annots.items()
			}

		return create_model(
			cls.__name__,
			__base__ = AmpelBaseModel,
			**kwargs # type: ignore[call-overload]
		)


	@classmethod
	def validate(cls, value: dict) -> Any:
		""" Validate kwargs values against fields of cls (except traceless) """
		try:
			values = cls._create_model(True).model_validate(value)
		except ValidationError as e:
			raise TypeError(e) from None
		return values.model_dump()


	@classmethod
	def validate_all(cls, value: dict) -> Any:
		""" Validate kwargs values against all fields of cls """
		if cls._model is None:
			model = cls._model = cls._create_model()
		else:
			model = cls._model
		try:
			values = model.model_validate(value)
		except ValidationError as e:
			raise TypeError(e) from None
		return values.model_dump()

	
	def __init__(self, **kwargs) -> None:

		cls = self.__class__

		if cls._model is None:
			cls._model = self._create_model()
			# might be needed in the future due to postponed annotations
			# cls._model.update_forward_refs()

		try:
			values = cls._model.model_validate(kwargs)
		except ValidationError as e:
			# https://github.com/samuelcolvin/pydantic/issues/784
			print("") # noqa: T201
			if kwargs:
				print("#" * 60) # noqa: T201
				print("Offending values:") # noqa: T201
				for k, v in kwargs.items():
					print(f"{k}: {v}") # noqa: T201
				print("#" * 60) # noqa: T201
			raise TypeError(e) from None

		# Save coerced values
		unset = self._defaults.keys() - kwargs.keys()
		kwargs.update({k: getattr(values, k) for k in cls._model.model_fields})

		if isinstance(self, BaseModel):
			super().__init__(**kwargs)
		else:
			super().__init__()

		sa = partial(object.__setattr__, self)
		sks = cls._sks
		aks = cls._aks

		sa("_exclude_unset", unset)

		# Set kwargs attributes
		for k, v in kwargs.items():
			if k in sks or k in aks:
				sa(k, v)


	def _get_trace_content(self) -> dict[str, Any]:

		a = self._annots
		return {
			k: self._dictify(getattr(self, k))
			for k in sorted(self._annots)
			if not (
				(type(a[k]) is ttf and a[k].__metadata__[0] == TRACELESS) or
				isinstance(a[k], Secret)
			)
		}

	def dict(
		self,
		*,
		include: "IncEx | None" = None,
		exclude: "IncEx | None" = None,
		by_alias: bool = False,
		exclude_unset: bool = False,
		exclude_defaults: bool = False,
		exclude_none: bool = False,
		warnings: bool = True,
	) -> dict[str, Any]:

		if hasattr(self, "__slots__"):
			d = self.__dict__ | {k: getattr(self, k) for k in self.__slots__}
		else:
			d = self.__dict__

		incl = self._aks if include is None else include
		excl = {
			k for k, v in self._annots.items()
			if type(v) is ttf and v.__metadata__[0] == TRACELESS
		}

		if exclude is not None:
			excl.update(v if isinstance(v, str) else str(v) for v in exclude)

		if exclude_unset:
			excl.update(self._exclude_unset)

		if exclude_defaults:
			for k in self._defaults:
				if d[k] == self._defaults[k]:
					excl.add(k)

		return {
			k: self._dictify(v)
			for k, v in d.items()
			if k in incl and not (k in excl or isinstance(d[k], Secret))
		}


	def _dictify(self, arg: Any, dict_kwargs={}) -> Any: # noqa: B006
		if isinstance(arg, list | tuple | set):
			return [self._dictify(el, dict_kwargs) for el in arg]
		if isinstance(arg, dict):
			return {
				k: self._dictify(v, dict_kwargs)
				for k, v in arg.items()
			}
		if isinstance(arg, Klass | BaseModel):
			return arg.dict(**dict_kwargs)
		return arg


	@classmethod
	def get_model_keys(cls) -> set[str]:
		return set(cls._annots.keys())


Klass = AmpelUnit
