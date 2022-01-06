#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/base/AlternativeAmpelBaseModel.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                07.10.2019
# Last Modified Date:  30.12.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from __future__ import annotations
import collections.abc as abc
from ujson import loads, dumps # type: ignore
from typeguard import check_type # type: ignore
from types import MemberDescriptorType, GenericAlias, UnionType
import ampel.types as altypes
from ampel.types import Traceless, TRACELESS
from ampel.secret.Secret import Secret
from typing import Any, Type, Union, Annotated, get_origin, get_args, _GenericAlias, _UnionGenericAlias # type: ignore[attr-defined]

ttf = type(Traceless)
NoneType = type(None)


class AlternativeAmpelBaseModel:
	"""
	Prototype class, not in used.
	This class supports setting slots values through constructor parameters (they will be type checked as well).
	Type checking can be deactivated globally by setting ampel.types.do_type_check to False
	"""

	_annots: dict[str, Any] = {}
	_defaults: dict[str, Any] = {}
	_slot_defaults: dict[str, Any] = {}
	_aks: set[str] = set() # annotation keys
	_sks: set[str] = set() # slots keys
	_debug: int = 0


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

		# Coercion (models, secrets) and type checking if ampel.types.do_type_check is True
		for k, v in joined_defaults.items():
			joined_defaults[k] = cls.get_value(k, joined_ann[k], v)

		if slots := getattr(cls, '__slots__', None):
			joined_sks.update(slots)

		for el in (
			('_annots', joined_ann), ('_defaults', joined_defaults),
			('_aks', joined_aks), ('_sks', joined_sks), ('_model', None)
		):
			setattr(cls, el[0], el[1])


	@classmethod
	def validate(cls, value: dict, _omit_traceless: bool = True) -> Any:
		""" Validate kwargs values against the fields of cls """

		defs = cls._defaults
		for k, v in cls._annots.items():
			if type(v) is ttf and v.__metadata__[0] == TRACELESS:
				continue
			if k in value:
				if cls._has_nested_model(v):
					v = cls._modelify(k, v, value[k])[1]
				if isinstance(v, type) and issubclass(v, Klass):
					v.validate(value[k], _omit_traceless=_omit_traceless)
				else:
					check_type(k, value[k], v)
			elif k in defs:
				continue
			else:
				raise ValueError(f"Parameter required: {k}")

		for k in value.keys():
			if k not in cls._annots:
				raise ValueError(f"Unknown parameter {k}")


	@classmethod
	def _spawn_model(cls, model: "type[AlternativeAmpelBaseModel]", value: dict) -> "AlternativeAmpelBaseModel":

		args = {
			k: model._spawn_model(model, v) if (
				k in cls._annots and
				isinstance(cls._annots[k], type) and
				issubclass(cls._annots[k], cls)
			) else v
			for k, v in value.items()
		}

		if cls._debug > 0:
			print(f"Spawning {model.__name__} with: {args}")

		try:
			ret = model(**args)
		except Exception as e:
			if cls._debug > 0:
				print(f"{model.__name__} instantiation failed")
				print("##", repr(e))
				import traceback
				print(traceback.format_exc())
			raise e

		if cls._debug > 0:
			print(f"{model.__name__} spawned")

		return ret


	@classmethod
	def _has_nested_model(cls, annot: type) -> bool:

		if cls._debug > 1:
			print("Checking " + str(annot).replace('collections.abc.', '') + " for nested models")

		if isinstance(annot, _GenericAlias) and hasattr(annot, 'mro') and issubclass(get_origin(annot), Secret): # type: ignore
			return True

		for i, el in enumerate(get_args(annot)):

			if cls._debug > 1:
				print(f"get_args element {i}: ", el)

			if isinstance(el, (GenericAlias, _GenericAlias, _UnionGenericAlias, UnionType)):
				o = get_origin(el)
				if (isinstance(o, type) and issubclass(o, Klass)) or cls._has_nested_model(el):
					return True

			if isinstance(el, type) and issubclass(el, Klass):
				return True

		return False


	@classmethod
	def _modelify(cls, key: str, annot: type, arg: Any) -> tuple[Exception | bool, Any]:

		oa = get_origin(annot)

		if cls._debug:
			print(f"● Potentially spawning model for {cls.__name__}.{key}")
			print("Annotation: ", annot)
			if oa:
				print("Origin", oa)
			print("Value:", arg)

		if oa is Union or oa is UnionType:
			if cls._debug:
				print("Origin is Union")
			es: list[Exception] = []
			for a in get_args(annot):
				try:
					if cls._debug > 1:
						print("Considering union member: ", a)
					modified, ret = cls._modelify(key, a, arg)
					if modified is True:
						if cls._debug > 1:
							print("Model spawned by union member: ", a)
						return True, ret
					elif isinstance(modified, Exception):
						es.append(modified)
				except Exception as e:
					es.append(e)
			if es and cls._has_nested_model(annot):
				raise TypeError(
					f"Type of {cls.__name__}.{key} must be one of {str(annot).replace('typing.', '')}:\n" +
					f"Value: {arg}\nAssociated errors:\n• " +
					"\n• ".join([str(e) for e in es])
				)
			return False, arg

		elif oa is Annotated:
			return cls._modelify(key, get_args(annot)[0], arg)
				
		elif oa is dict and isinstance(arg, dict):
			if cls._debug:
				print("Origin is dict")
			modified = False
			ret = {}
			for k, v in arg.items():
				x, ret[k] = cls._modelify(f"{key}.{k}", get_args(annot)[1], v)
				if x is True:
					modified = True
			return modified, ret

		elif oa in (list, tuple, abc.Sequence) and isinstance(arg, (list, tuple)):
			if cls._debug:
				print("Origin is sequence")
			ret = []
			modified = False
			for i, el in enumerate(arg):
				x, y = cls._modelify(f"{key}[{i}]", get_args(annot)[0], el)
				ret.append(y)
				if x is True:
					modified = True
			return modified, ret

		elif oa is None and isinstance(arg, dict) and isinstance(annot, type) and issubclass(annot, AlternativeAmpelBaseModel):
			try:
				return True, cls._spawn_model(annot, arg)
			except Exception as e:
				return e, arg

		elif isinstance(oa, type) and issubclass(oa, Klass) and isinstance(arg, dict):
			try:
				return True, cls._spawn_model(oa, arg)
			except Exception as e:
				return e, arg

		else:
			if cls._debug > 1:
				print("Value left as is")

		return False, arg


	@classmethod
	def get_value(cls, k: str, a: type, v: Any) -> Any:

		es = None
		ao = get_origin(a)
		if a in (bool, int, str, float):
			pass
		elif cls._has_nested_model(a):
			if cls._debug > 1:
				print(f"{cls.__name__}.{k} has nested model")
			es, v = cls._modelify(k, a, v)
		elif ao in (Union, UnionType):
			if cls._debug > 1:
				print(f"{cls.__name__}.{k} has Union type")
			es, v = cls._modelify(k, a, v)
		elif ao is Annotated:
			return cls.get_value(k, get_args(a)[0], v)
		elif isinstance(a, type) and issubclass(a, Klass) and isinstance(v, dict):
			v = cls._spawn_model(a, v)
		elif isinstance(a, type) and issubclass(a, Secret):
			v = a(**v)
		else:
			if cls._debug > 1:
				print(f"{cls.__name__}.{k} has no nested model")

		if ao is Annotated:
			return cls.get_value(k, get_args(a)[0], v)

		if altypes.do_type_check:
			"""
			from typingx import isinstancex
			if cls._debug > 1:
				print(f"○ Type checking {cls.__name__}.{k}\n  Annotated type: {a}\n  Value: {v}")
			if isinstancex(v, a):
				if cls._debug > 1:
						print("✓ OK")
			else:
				msg = f"{cls.__name__}: invalid type for field '{k}'\n  Type: {a}\n  Value: {v}"
				if isinstance(es, list):
					msg += "Related errors:\n" + "\n".join([str(e) for e in es])
				raise TypeError(msg) from None
			"""
			try:
				if cls._debug > 1:
					print(f"○ Type checking {cls.__name__}.{k}\n  Annotated type: {a}\n  Value: {v}")
				check_type(k, v, a)
				if cls._debug > 1:
					print("✓ OK")
			except Exception as e:
				msg = f"{str(e)}\nField: {cls.__name__}.{k}\nType: {a}\nValue: {v}"
				if isinstance(es, list):
					msg += "Related errors:\n" + "\n".join([str(e) for e in es])
				raise TypeError(msg) from None

		return v


	def __init__(self, **kwargs) -> None:

		cls = self.__class__
		sa = self.__setattr__
		defs = cls._defaults
		self._exclude_unset: set[str] = set()

		if cls._debug > 1:
			print(f"{cls.__name__}.__init__(...)")

		for k, a in cls._annots.items():

			if cls._debug > 1:
				print(f"□ {cls.__name__}.{k}: {a}")

			es = None

			# Should be first
			if k in kwargs:
				v = cls.get_value(k, a, kwargs[k])
			elif k in defs:
				self._exclude_unset.add(k)
				if isinstance(defs[k], (list, dict)):
					v = loads(dumps(defs[k]))
				elif Klass in defs[k].__class__.__mro__:
					v = defs[k].__class__(**loads(dumps(defs[k].dict())))
				else:
					v = defs[k]
			elif k in cls._slot_defaults:
				self._exclude_unset.add(k)
				if isinstance(cls._slot_defaults[k], (list, dict)):
					v = loads(dumps(cls._slot_defaults[k]))
				elif Klass in cls._slot_defaults[k].__class__.__mro__:
					v = cls._slot_defaults[k].__class__(**loads(dumps(cls._slot_defaults[k].dict())))
				else:
					v = cls._slot_defaults[k]
			else:
				raise ValueError(f"{cls.__name__}: a value is required for parameter '{k}'")

			if cls._debug > 1:
				print(f"Setting {cls.__name__}.{k} value: {v}")

			sa(k, v)

		for k in kwargs.keys():
			if k not in cls._annots:
				raise ValueError(f"{cls.__name__}: unknown parameter {k}")

		if cls._debug > 1:
			print(f"End of {cls.__name__}.__init__(...)")


	def dict(self,
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
				if k in self.__dict__:
					if self.__dict__[k] == self._defaults[k]:
						excl.add(k)
				else:
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


Klass = AlternativeAmpelBaseModel
