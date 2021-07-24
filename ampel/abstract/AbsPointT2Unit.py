#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsPointT2Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 28.12.2019
# Last Modified Date: 03.04.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Union, Optional, ClassVar
from ampel.types import UBson
from ampel.struct.UnitResult import UnitResult
from ampel.content.DataPoint import DataPoint
from ampel.base.AmpelABC import AmpelABC
from ampel.base.decorator import abstractmethod
from ampel.base.LogicalUnit import LogicalUnit
from ampel.model.T2IngestOptions import T2IngestOptions


class AbsPointT2Unit(AmpelABC, LogicalUnit, abstract=True):
	"""
	A T2 unit bound to a :class:`~ampel.content.DataPoint.DataPoint`
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
	def process(self, datapoint: DataPoint) -> Union[UBson, UnitResult]:
		"""
		Returned object should contain computed science results to be saved into the DB.

		.. note:: the returned dict must have only string keys and be BSON-encodable
		"""
