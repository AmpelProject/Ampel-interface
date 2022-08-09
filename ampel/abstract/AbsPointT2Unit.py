#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/abstract/AbsPointT2Unit.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                28.12.2019
# Last Modified Date:  28.09.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from ampel.types import UBson
from ampel.struct.UnitResult import UnitResult
from ampel.content.DataPoint import DataPoint
from ampel.base.AmpelABC import AmpelABC
from ampel.base.decorator import abstractmethod
from ampel.base.LogicalUnit import LogicalUnit


class AbsPointT2Unit(AmpelABC, LogicalUnit, abstract=True):
	"""
	A T2 unit bound to a :class:`~ampel.content.DataPoint.DataPoint`

	Note that the implementing class can customize the default ingestion behavior
	(which :class:`~ampel.content.DataPoint.DataPoint` to create
	:class:`T2 documents <ampel.content.T2Document.T2Document>` for)
	by defining the class variable 'eligible'
	
	Example::
	  ingest: ClassVar[DPSelection] = DPSelection(select=(1, -2, 5))
	
	will create documents bound to every 5th datapoint starting from the 2nd
	and ending with the 3rd-to-last

	Example::
	   ingest: ClassVar[DPSelection] = DPSelection(filter=UnitModel(unit='SimpleTagFilter', config={'require': ['ZTF_DP']}), sort='jd', select='first'}

	will create documents bound to the first datapoint with tag 'ZTF_DP', in order of body.jd.
	
	select options:
	  - "first": first datapoint for a stock
	  - "last": most recent datapoint for a stock
	  - "all": every datapoint (default)
	  - :class:`tuple`: :class:`slice` of datapoints
	-> see DPSelection docstring for info regarding 'filter' and 'sort'.

	If 'eligible' is not specified, default ingestion will occur:
	a T2 document will be created for each datapoint
	"""

	@abstractmethod
	def process(self, datapoint: DataPoint) -> UBson | UnitResult:
		"""
		Returned object should contain computed science results to be saved into the DB.

		.. note:: the returned dict must have only string keys and be BSON-encodable
		"""
