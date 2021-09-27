#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/model/T2IngestOptions.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 10.03.2020
# Last Modified Date: 11.05.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Union, Optional, Literal, List, TypedDict
from ampel.abstract.AbsApplicable import AbsApplicable

class T2IngestOptions(TypedDict, total=False):
	"""
	:param filter: filter datapoints
	:param sort: sort datapoints.
		'id' uses the datapoint 'id' at root level.
		Anything else will target a field (by name) in 'body'
	:param select: how to slice the datapoint array.
		If a list is provided, it must have a length of 3
	"""
	filter: Optional[Union[str, AbsApplicable]]
	sort: Optional[Union[Literal['id'], str]]
	select: Optional[Union[Literal['first', 'last'], List[Optional[int]]]]
