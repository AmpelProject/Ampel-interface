#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/utils/Freeze.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 10.12.2019
# Last Modified Date: 12.02.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Dict, Any
from pydantic import BaseModel
from ampel.view.ReadOnlyDict import ReadOnlyDict


class Freeze:


	@classmethod
	def recursive_lock(cls, model: BaseModel) -> None:
		"""
		Locks a pydantic model instance
		"""
		model.Config.allow_mutation = False
		for key in model.fields.keys():
			value = getattr(model, key)
			if isinstance(value, BaseModel):
				cls.recursive_lock(value)


	@classmethod
	def recursive_freeze(cls, arg: Any) -> Any:
		"""
		Return an immutable shallow copy
		:param arg:
			dict: ReadOnlyDict is returned
			list: tuple is returned
			set: frozenset is returned
			otherwise: arg is returned 'as is'
		"""
		if isinstance(arg, dict):
			return ReadOnlyDict(
				{
					cls.recursive_freeze(k): cls.recursive_freeze(v)
					for k,v in arg.items()
				}
			)

		if isinstance(arg, list):
			return tuple(
				map(cls.recursive_freeze, arg)
			)

		if isinstance(arg, set):
			return frozenset(arg)

		return arg


	@classmethod
	def recursive_unfreeze(cls, arg: ReadOnlyDict) -> Dict:
		"""
		Inverse of recursive_freeze
		"""
		if isinstance(arg, ReadOnlyDict):
			return dict(
				{
					cls.recursive_unfreeze(k): cls.recursive_unfreeze(v)
					for k,v in arg.items()
				}
			)

		if isinstance(arg, tuple):
			return list(
				map(cls.recursive_unfreeze, arg)
			)

		if isinstance(arg, frozenset):
			return set(arg)

		return arg
