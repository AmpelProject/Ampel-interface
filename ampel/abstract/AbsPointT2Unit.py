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
	A T2 unit bound to a :class:`~ampel.content.DataPoint.DataPoint`
	"""

	# See EligibleModel docstring for more info
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
	def run(self, datapoint: DataPoint) -> T2UnitResult:
		"""
		Returned object should contain computed science results to be saved into the DB.

		.. note:: the returned dict must have only string keys and be BSON-encodable
		"""
