#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsPointT2Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 28.12.2019
# Last Modified Date: 17.02.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Optional, Union, Literal, Tuple, Dict, ClassVar
from ampel.abc import abstractmethod, defaultmethod
from ampel.abstract.AbsDataUnit import AbsDataUnit
from ampel.t2.T2Result import T2Result
from ampel.content.DataPoint import DataPoint


class AbsPointT2Unit(AbsDataUnit, abstract=True):
	"""
	Top level abstract class for t2 units bound to datapoint(s)

	The parameter ingest (used by the ingester) supports the key/value 'eligible'.
	If customized, the alert ingester will not create a T2 document for each datapoint
	of a given transient, but only for the one fulfilling the selection criteria below:
	- Either the "first" or the current "last" one
	- The one selected by the function "slice" whose 3 integer arguments are to be provided
	"""

	# See EligibleModel docstring for more info
	ingest: ClassVar[Optional[Dict[
		Literal['eligible'],
		Union[
			Literal['first', 'last'],
			Tuple[int, Optional[int], Optional[int]]
		]
	]]]


	@defaultmethod(check_super_call=True)
	def __init__(self, **kwargs) -> None:
		AbsDataUnit.__init__(self, **kwargs)
		self.post_init()


	def post_init(self) -> None:
		pass


	@abstractmethod
	def run(self, datapoint: DataPoint) -> T2Result:
		"""
		Returned T2Result dataclass should contain computed science results to be saved into the DB.
		Notes: dict must have only string keys and values must be bson encodable
		"""
