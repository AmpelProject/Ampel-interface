#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/base/AmpelBaseModel.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                07.10.2019
# Last Modified Date:  30.12.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from __future__ import annotations
from ujson import loads, dumps # type: ignore[import]
import collections.abc as abc
from typeguard import check_type
from types import MemberDescriptorType, GenericAlias, UnionType
from ampel.types import Traceless, TRACELESS
from ampel.secret.Secret import Secret
from typing import Any, Type, Union, Annotated, get_origin, get_args, _GenericAlias, _UnionGenericAlias # type: ignore[attr-defined]

do_type_check = True
ttf = type(Traceless)


class AmpelBaseModel:
	"""
	This class supports setting slots values through constructor parameters (they will be type checked as well).

	Type checking can be deactivated globaly through the _check_types varaible, which will speed up instantiation significantly::
	
	  In []: class B(AmpelBaseModel):
	    ...:     a: list[int] = []

	  In []: %timeit B(a=[11])
	  8.08 µs ± 78 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)

	  In []: ampel.base.AmpelBaseModel._check_types=False

	  In []: %timeit B(a=[11])
	  1.46 µs ± 21 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
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
				NoneType = type(None)
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
	def validate(cls, value: dict, _omit_traceless: bool = True) -> Any:
		""" Validate kwargs values against the fields of cls """

		defs = cls._defaults
		ttf = type(Traceless)
		for k, v in cls._annots.items():
			if type(v) is ttf and v.__metadata__[0] == TRACELESS:
				continue
			if k in value:
				if cls._has_nested_model(v):
					v = cls._modelify(k, value[k], v)[1]
				if isinstance(v, type) and issubclass(v, Klass):
					v.validate(value[k], _omit_traceless=_omit_traceless)
				else:
					check_type(k, value[k], v)
				#raise ValueError(f"Wrong type for parameter '{k}'. Expected: {v}, Provided: {type(value[k])}")
			elif k in defs:
				continue
			else:
				raise ValueError(f"Parameter required: {k}")

		for k in value.keys():
			if k not in cls._annots:
				raise ValueError(f"Unknown parameter {k}")


	@classmethod
	def _spawn_model(cls, model: "type[AmpelBaseModel]", value: dict) -> "AmpelBaseModel":
		return model(
			**{
				k: model._spawn_model(model, v)
				if (k in cls._annots and isinstance(cls._annots[k], type) and issubclass(cls._annots[k], cls)) else v
				for k, v in value.items()
			}
		)


	@classmethod
	def _has_nested_model(cls, annot: type) -> bool:

		if isinstance(annot, _GenericAlias) and hasattr(annot, 'mro') and issubclass(get_origin(annot), Secret): # type: ignore
			return True

		for el in get_args(annot):

			if cls._debug > 1:
				print("el", el, get_origin(el))

			if isinstance(el, (GenericAlias, _GenericAlias, _UnionGenericAlias, UnionType)):
				o = get_origin(el)
				if (isinstance(o, type) and issubclass(o, Klass)) or cls._has_nested_model(el):
					return True

			if isinstance(el, type) and issubclass(el, Klass):
				return True

		return False


	@classmethod
	def _modelify(cls, key: str, arg: Any, annot: type) -> tuple[Exception | bool, Any]:

		oa = get_origin(annot)

		if cls._debug:
			print(f"⬤  Modelify {cls.__name__}")
			print("Annot: ", annot)
			print("Arg:", arg)
			print("Origin", oa)

		if oa is Union or oa is UnionType:
			if cls._debug:
				print("Origin is Union")
			es: list[Exception] = []
			for a in get_args(annot):
				try:
					if cls._debug > 1:
						print("Considering union member: ", a)
					modified, ret = cls._modelify(key, arg, a)
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
			return cls._modelify(key, arg, get_args(annot)[0])
				
		elif oa is dict and isinstance(arg, dict):
			if cls._debug:
				print("Origin is dict")
			modified = False
			vtype = get_args(annot)[1]
			ret = {}
			for k, v in arg.items():
				x, ret[k] = cls._modelify(f"{key}.{k}", v, vtype)
				if x is True:
					modified = True
			return modified, ret

		elif oa in (list, tuple, abc.Sequence) and isinstance(arg, (list, tuple)):
			if cls._debug:
				print("Origin is sequence")
			vtype = get_args(annot)[0]
			ret = []
			modified = False
			for i, el in enumerate(arg):
				x, y = cls._modelify(f"{key}[{i}]", el, vtype)
				ret.append(y)
				if x:
					modified = True
			return modified, ret

		elif oa is None and isinstance(arg, dict) and isinstance(annot, type) and issubclass(annot, AmpelBaseModel):
			if cls._debug:
				print("Spawning ", annot)
			try:
				ret = cls._spawn_model(annot, arg)
				if cls._debug > 0:
					print(f"{annot.__name__} spawned")
				return True, ret
			except Exception as e:
				if cls._debug > 0:
					print(f"{annot.__name__} instantiation failed")
					if cls._debug > 1:
						print(e)
				return e, arg

		elif isinstance(oa, type) and issubclass(oa, Klass) and isinstance(arg, dict):
			if cls._debug:
				print("Spawning ", oa)
			try:
				ret = cls._spawn_model(oa, arg)
				if cls._debug > 0:
					print(f"{oa.__name__} spawned")
				return True, ret
			except Exception as e:
				if cls._debug > 0:
					print(f"{oa.__name__} instantiation failed")
					if cls._debug > 1:
						print(e)
				return e, arg

		else:
			if cls._debug > 1:
				print("No action performed")

		return False, arg


	def __init__(self, **kwargs) -> None:

		if self.__class__._debug > 1:
			print(f"{self.__class__.__name__}.__init__(...)")

		self._exclude_unset: set[str] = set()

		cls = self.__class__
		sa = self.__setattr__
		defs = cls._defaults

		for k in cls._annots:
			if k in kwargs:
				v = cls._annots[k]
				if cls._has_nested_model(v):
					if self.__class__._debug > 1:
						print(f"{cls.__name__}.{k} has nested model")
					es, kwargs[k] = self._modelify(k, kwargs[k], v)
				elif isinstance(v, type) and issubclass(v, Klass) and isinstance(kwargs[k], dict):
					kwargs[k] = self._spawn_model(v, kwargs[k])
				elif isinstance(v, type) and issubclass(v, Secret):
					kwargs[k] = v(**kwargs[k])
				else:
					if self.__class__._debug > 1:
						print(f"{cls.__name__}.{k} has no nested model")

				if do_type_check:
					try:
						check_type(k, kwargs[k], v)
					except Exception as e:
						msg = f"{str(e)}\nField: {cls.__name__}.{k}\nType: {v}\nValue: {kwargs[k]}"
						if isinstance(es, list):
							msg += "Related errors:\n" + "\n".join([str(e) for e in es])
						raise TypeError(msg) from None
				sa(k, kwargs[k])
			elif k in defs:
				self._exclude_unset.add(k)
				if isinstance(defs[k], (list, dict)):
					sa(k, loads(dumps(defs[k])))
				elif Klass in defs[k].__class__.__mro__:
					sa(k, defs[k].__class__(**loads(dumps(defs[k].dict()))))
				else:
					sa(k, defs[k])
			elif k in cls._slot_defaults:
				self._exclude_unset.add(k)
				#sa(k, loads(dumps(cls._slot_defaults[k])))
				sa(k, cls._slot_defaults[k])
			else:
				raise ValueError(f"{self.__class__.__name__}: a value for parameter '{k}' is required")

		for k in kwargs.keys():
			if k not in cls._annots:
				raise ValueError(f"{self.__class__.__name__}: unknown parameter {k}")

		if self.__class__._debug > 1:
			print(f"End of {self.__class__.__name__}.__init__(...)")


	def dict(
		self,
		include: None | set[str]=None,
		exclude: None | set[str]=None,
		exclude_defaults: bool=False,
		exclude_unset: bool=False,
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


Klass = AmpelBaseModel
