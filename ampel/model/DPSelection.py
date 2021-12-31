#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/model/DPSelection.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 10.03.2020
# Last Modified Date: 28.09.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Union, Optional, Literal
from collections.abc import Callable
from ampel.model.UnitModel import UnitModel
from ampel.model.StrictModel import StrictModel
from ampel.base.AuxUnitRegister import AuxUnitRegister
from ampel.abstract.AbsApplicable import AbsApplicable


class DPSelection(StrictModel):

	#: Aux unit name used to filter datapoints.
	# (Unit must define method apply(self, arg: Any) -> Any)
	filter: Optional[Union[UnitModel, str]]

	#: Dict key used for sorting
	#: Use 'id' to sort dps based on key 'id' at root level,
	#: anything else will target a field (by name) in 'body'
	sort: Optional[str]

	#: How to slice the datapoint array.
	#: If a list is provided, it must have a length of 3
	select: Union[
		None,
		Literal['first'],
		Literal['last'],
		tuple[Optional[int], Optional[int], Optional[int]]
	] = None


	def __init__(self, **kwargs):

		if 'select' in kwargs and isinstance(kwargs['select'], list) and len(kwargs['select']) == 3:
			kwargs['select'] = tuple(kwargs['select'])

		super().__init__(**kwargs)

		if self.sort and not self.select:
			raise ValueError("Options 'sort' requires option 'select'")


	def tools(self) -> tuple[Optional[AbsApplicable], Optional[Callable[[list], list]], slice]:

		so = None
		sl = None

		f = AuxUnitRegister.new_unit(
			self.filter if isinstance(self.filter, UnitModel) else UnitModel(unit=self.filter),
			sub_type = AbsApplicable
		) if self.filter else None

		if self.sort:
			if self.sort == 'id':
				lbd = lambda k: k['id']
			else:
				lbd = lambda k: k['body'][self.sort]
			so = lambda l: sorted(l, key=lbd)

		if self.select is None:
			sl = slice(None)
		elif self.select == "all":
			sl = slice(None)
		elif self.select == "first":
			sl = slice(1)
		elif self.select == "last":
			sl = slice(-1, -2, -1)
		elif isinstance(self.select, (list, tuple)) and len(self.select) == 3:
			sl = slice(*self.select)
		else:
			raise ValueError(
				f"Unsupported value provided as slice parameter : {self.select}"
			)

		return f, so, sl
