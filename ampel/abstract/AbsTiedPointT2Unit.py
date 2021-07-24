#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsTiedPointT2Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 16.02.2021
# Last Modified Date: 30.05.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Union, Optional, Sequence, ClassVar
from ampel.types import UBson
from ampel.struct.UnitResult import UnitResult
from ampel.view.T2DocView import T2DocView
from ampel.content.DataPoint import DataPoint
from ampel.base.decorator import abstractmethod
from ampel.abstract.AbsTiedT2Unit import AbsTiedT2Unit
from ampel.model.T2IngestOptions import T2IngestOptions


class AbsTiedPointT2Unit(AbsTiedT2Unit, abstract=True):
	"""
	A T2 unit bound to a :class:`~ampel.content.DataPoint.DataPoint` as well
	as the results of other T2 units
	"""

	# See T2IngestOptions docstring for more info
	#: Which :class:`~ampel.content.DataPoint.DataPoint` to create
	#: :class:`T2 documents <ampel.content.T2Document.T2Document>` for
	#:
	#: Example::
	#:    {'filter': 'PPSFilter', 'sort': 'jd', 'select': 'first'}
	#:
	#: "first"
	#:   first datapoint for a stock
	#: "last"
	#:   most recent datapoint for a stock
	#: "all"
	#:   every datapoint (default)
	#: :class:`tuple`
	#:   :class:`slice` of datapoints
	#:
	#: Example::
	#:
	#:   {"select": (1, -2, 5)}
	#:
	#: will create documents bound to every 5th datapoint starting from the 2nd
	#: and ending with the 3rd-to-last
	#:
	#: If unspecified, a T2 document will be created for each datapoint.
	ingest: ClassVar[Optional[T2IngestOptions]] = None


	@abstractmethod
	def process(self, datapoint: DataPoint, t2_views: Sequence[T2DocView]) -> Union[UBson, UnitResult]:
		"""
		Returned object should contain computed science results to be saved into the DB.

		.. note:: the returned dict must have only string keys and be BSON-encodable
		"""
