#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/base/AmpelBaseModel.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 07.10.2019
# Last Modified Date: 19.11.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from types import MemberDescriptorType
from typing import get_origin, get_args, Union, Dict, Any, ClassVar, Set, Type
from pydantic import BaseModel, validate_model, create_model
from ampel.model.StrictModel import StrictModel

_check_types = True


class AmpelBaseModel:
	"""
	Top level class that uses pydantic's BaseModel to validate data.
	This class supports setting slots values through constructor parameters (they will be type checked as well).

	Type checking can be deactivated globaly through the _check_types varaible, which will speed up instantiation significantly::
	
	  In []: class B(AmpelBaseModel):
	    ...:     a: List[int] = []

	  In []: %timeit B(a=[11])
	  8.08 µs ± 78 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)

	  In []: ampel.base.AmpelBaseModel._check_types=False

	  In []: %timeit B(a=[11])
	  1.46 µs ± 21 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
	"""

	_model: Type[BaseModel]
	_annots: ClassVar[Dict[str, Any]] = {}
	_defaults: ClassVar[Dict[str, Any]] = {}
	_slot_defaults: ClassVar[Dict[str, Any]] = {}
	_aks: ClassVar[Set[str]] = set() # annotation keys
	_sks: ClassVar[Set[str]] = set() # slots keys


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
			if ann := getattr(base, '__annotations__', None):
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
					# if Optional[] with no default
					elif get_origin(v) is Union and NoneType in get_args(v) and k not in joined_defaults: # type: ignore[misc]
						joined_defaults[k] = None
					elif k in cls._slot_defaults:
						joined_defaults[k] = cls._slot_defaults[k]

		if slots := getattr(cls, '__slots__', None):
			joined_sks.update(slots)

		for el in (
			('_annots', joined_ann), ('_defaults', joined_defaults),
			('_aks', joined_aks), ('_sks', joined_sks), ('_model', None)
		):
			setattr(cls, el[0], el[1])


	@classmethod
	def _create_model(cls):
		defs = cls._defaults
		cls._model = create_model(
			cls.__name__,
			__config__ = StrictModel.__config__,
			**{
				k: (v, defs[k] if k in defs else ...)
				for k, v in cls._annots.items()
			} # type: ignore[arg-type]
		)

	@classmethod
	def validate(cls, **kwargs) -> None:
		"""
		Validate kwargs against the fields of cls
		"""
		if cls._model is None:
			cls._create_model()
		values, fields, errors = validate_model(cls._model, kwargs) # type: ignore[arg-type]
		if errors:
			raise errors


	def __init__(self, **kwargs) -> None:

		cls = self.__class__

		if cls._model is None:
			self._create_model()
			# might be needed in the future due to postponed annotations
			# cls._model.update_forward_refs()

		# Check types (default behavior)
		if _check_types:

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

			# Note: coercion could be checked/deactived by a flag as well
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
