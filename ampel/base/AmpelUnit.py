#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/base/AmpelUnit.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                07.10.2019
# Last Modified Date:  05.01.2022
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

import collections.abc as abc
from types import MemberDescriptorType, GenericAlias, UnionType
import ampel.types as altypes
from ampel.types import Traceless, TRACELESS
from ampel.secret.Secret import Secret
from ampel.base.AmpelBaseModel import AmpelBaseModel
from pydantic import BaseModel, validate_model, create_model
from typing import Any, Type, Union, Annotated, get_origin, get_args, _GenericAlias, _UnionGenericAlias # type: ignore[attr-defined]

ttf = type(Traceless)
NoneType = type(None)


class AmpelUnit:
	"""
	This class supports setting slots values through constructor parameters (they will be type checked as well).
	Type checking can be deactivated globally by setting ampel.types.do_type_check to False
	"""

	_model: Type[BaseModel]
	_annots: dict[str, Any] = {}
	_defaults: dict[str, Any] = {}
	_slot_defaults: dict[str, Any] = {}
	_aks: set[str] = set() # annotation keys
	_sks: set[str] = set() # slots keys


	@classmethod
	def __init_subclass__(cls, *args, **kwargs) -> None:
		"""
		Combines annotations & default values of this class with the one defined in sub-classes.
		Has similarities with the newly introduced typing.get_type_hints() function.
		"""
		super().__init_subclass__(*args, **kwargs) # type: ignore

		joined_ann = {
			k: v for k, v in cls._annots.items()
			if not (k[0] == '_' or 'ClassVar' in str(v))
		}
		joined_defaults = cls._defaults.copy()
		joined_sks = cls._sks.copy()
		joined_aks = cls._aks.copy()

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
					elif get_origin(v) in (Union, UnionType) and NoneType in get_args(v) and k not in joined_defaults: # type: ignore[misc]
						joined_defaults[k] = None
					elif k in cls._slot_defaults:
						joined_defaults[k] = cls._slot_defaults[k]

			# allow subclasses to change default value without supplying a new annotation
			for k, v in getattr(base, '__dict__', {}).items():
				if k in joined_ann and not k in ann:
					joined_defaults[k] = v

		if slots := getattr(cls, '__slots__', None):
			joined_sks.update(slots)

		for el in (
			('_annots', joined_ann), ('_defaults', joined_defaults),
			('_aks', joined_aks), ('_sks', joined_sks), ('_model', None)
		):
			setattr(cls, el[0], el[1])


	@classmethod
	def _create_model(cls, omit_traceless: bool = False) -> Type[BaseModel]:

		defs = cls._defaults
		if omit_traceless:
			ttf = type(Traceless)
			kwargs = {
				k: (v, defs[k] if k in defs else ...)
				for k, v in cls._annots.items()
				if not (type(v) is ttf and v.__metadata__[0] == TRACELESS)
			}
		else:
			kwargs = {
				k: (v, defs[k] if k in defs else ...)
				for k, v in cls._annots.items()
			}

		return create_model(
			cls.__name__,
			__config__ = AmpelBaseModel.__config__,
			**kwargs # type: ignore
		)


	@classmethod
	def validate(cls, value: dict) -> Any:
		""" Validate kwargs values against fields of cls (except traceless) """
		values, fields, errors = validate_model(cls._create_model(True), value)
		if errors:
			raise errors
		return values


	@classmethod
	def validate_all(cls, value: dict) -> Any:
		""" Validate kwargs values against all fields of cls """
		if cls._model is None:
			model = cls._model = cls._create_model()
		else:
			model = cls._model
		values, fields, errors = validate_model(model, value)
		if errors:
			raise errors
		return values


	def __init__(self, **kwargs) -> None:

		cls = self.__class__

		if cls._model is None:
			cls._model = self._create_model()
			# might be needed in the future due to postponed annotations
			# cls._model.update_forward_refs()

		self._exclude_unset = self._defaults.keys() - kwargs.keys()
		vres = validate_model(cls._model, kwargs) # type: ignore[arg-type]

		# pydantic ValidationError
		if e := vres[2]:
			# https://github.com/samuelcolvin/pydantic/issues/784
			print("")
			print("#" * 60)
			print("Offending values:")
			for k, v in kwargs.items():
				print(f"{k}: {v}")
			print("#" * 60)
			raise e

		# Save coerced values
		kwargs.update(vres[0])

		sa = self.__setattr__
		sks = cls._sks
		aks = cls._aks

		for k, v in cls._slot_defaults.items():
			if k not in kwargs:
				sa(k, v)

		# Set kwargs attributes
		for k in kwargs:
			if k in sks or k in aks:
				sa(k, kwargs[k])


	def dict(self, *,
		include: None | set[str] = None,
		exclude: None | set[str] = None,
		exclude_defaults: bool = False,
		exclude_unset: bool = False,
	) -> dict[str, Any]:

		d = self.__dict__
		incl = self._aks if include is None else include
		excl = {
			k for k, v in self._annots.items()
			if type(v) is ttf and v.__metadata__[0] == TRACELESS
		}

		if exclude is not None:
			excl.update(exclude)

		if exclude_unset:
			excl.update(self._exclude_unset)

		if exclude_defaults:
			for k in self._defaults:
				if self.__dict__[k] == self._defaults[k]:
					excl.add(k)

		return {
			k: self._dictify(v)
			for k, v in d.items()
			if k in incl and not (k in excl or isinstance(d[k], Secret))
		}


	def _dictify(self, arg: Any, dict_kwargs={}) -> Any:
		if isinstance(arg, (list, tuple, set)):
			return [self._dictify(el, dict_kwargs) for el in arg]
		elif isinstance(arg, dict):
			return {
				k: self._dictify(v, dict_kwargs)
				for k, v in arg.items()
			}
		elif isinstance(arg, Klass):
			return arg.dict(**dict_kwargs)
		return arg


	@classmethod
	def get_model_keys(cls) -> abc.KeysView[str]:
		return cls._annots.keys()


Klass = AmpelUnit