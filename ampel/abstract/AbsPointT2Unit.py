#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsPointT2Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 28.12.2019
# Last Modified Date: 08.06.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Optional, Union, Literal, Tuple, Dict
from ampel.type import T2UnitResult
from ampel.base import AmpelABC, DataUnit, abstractmethod
from ampel.content.DataPoint import DataPoint


class AbsPointT2Unit(AmpelABC, DataUnit, abstract=True):
	"""
	Top level abstract class for t2 units bound to datapoint(s)

	The parameter ingest (used by the ingester) supports the key/value 'eligible'.
	If customized, the alert ingester will not create a T2 document for each datapoint
	of a given transient, but only for the one fulfilling the selection criteria below:
	
	- Either the "first" or the current "last" one
	- The one selected by the function "slice" whose 3 integer arguments are to be provided
	"""

	# See EligibleModel docstring for more info
	ingest: Optional[Dict[
		Literal['eligible'],
		Union[
			Literal['first', 'last', 'all'],
			Tuple[int, Optional[int], Optional[int]]
		]
	]]


	@abstractmethod
	def run(self, datapoint: DataPoint) -> T2UnitResult:
		"""
		Returned object should contain computed science results to be saved into the DB.
		Notes: dict must have only string keys and values must be bson encodable
		"""
