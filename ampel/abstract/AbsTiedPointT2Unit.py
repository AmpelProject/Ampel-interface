#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsTiedPointT2Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 16.02.2021
# Last Modified Date: 17.02.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Dict, Union, Optional, Literal, Tuple, Sequence
from ampel.base import abstractmethod
from ampel.type import T2UnitResult
from ampel.abstract.AbsTiedT2Unit import AbsTiedT2Unit
from ampel.content.DataPoint import DataPoint
from ampel.view.T2DocView import T2DocView


class AbsTiedPointT2Unit(AbsTiedT2Unit, abstract=True):
	"""
	A T2 unit bound to a :class:`~ampel.content.DataPoint.DataPoint` as well
	as the results of other T2 units
	"""

	#: Which :class:`~ampel.content.DataPoint.DataPoint` to create
	#: :class:`T2 documents <ampel.content.T2Document.T2Document>` for
	#:
	#: "first"
	#:   first datapoint for a stock
	#: "last"
	#:   most recent datapoint for a stock
	#: "all"
	#:   every datapoint
	#: :class:`tuple`
	#:   :class:`slice` of datapoints
	#:
	#: For example::
	#:   
	#:   {"eligible": (1, -2, 5)}
	#:
	#: will create documents bound to every 5th datapoint starting from the 2nd
	#: and ending with the 3rd-to-last
	#:
	#: If unspecified, a T2 document will be created for each datapoint.
	ingest: Optional[Dict[
		Literal['eligible'],
		Union[
			Literal['first', 'last', 'all'],
			Tuple[int, Optional[int], Optional[int]]
		]
	]]


	@abstractmethod
	def run(self, datapoint: DataPoint, t2_views: Sequence[T2DocView]) -> T2UnitResult:
		"""
		Returned object should contain computed science results to be saved into the DB.

		.. note:: the returned dict must have only string keys and be BSON-encodable
		"""
