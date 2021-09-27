#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/model/DPSelection.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 10.03.2020
# Last Modified Date: 28.09.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Union, Optional, Literal, Tuple
from ampel.model.StrictModel import StrictModel

class DPSelection(StrictModel):

	#: Aux unit name used to filter datapoints.
	# (Unit must define method apply(self, arg: Any) -> Any)
	filter: Optional[str]

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
		Tuple[Optional[int], Optional[int], Optional[int]]
	]

	def __init__(self, **kwargs):

		if 'select' in kwargs and isinstance(kwargs['select'], list) and len(kwargs['select']) == 3:
			kwargs['select'] = tuple(kwargs['select'])

		super().__init__(**kwargs)

		if self.sort and not self.select:
			raise ValueError("Options 'sort' requires option 'select'")
