#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/model/operator/FlatAnyOf.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 15.10.2018
# Last Modified Date: 18.03.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

import collections
from typing import List, Generic
from pydantic import validator
from pydantic.generics import GenericModel
from ampel.types import T

class FlatAnyOf(GenericModel, Generic[T]):
	"""
	Similar to AnyOf except that it does not allow embedded AllOf elements
	"""
	any_of: List[T]

	@validator('any_of', pre=True)
	def cast_to_list(cls, v):
		if not isinstance(v, collections.abc.Sequence):
			return [v]
		return v
