#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/abstract/AbsT0Unit.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                07.10.2019
# Last Modified Date:  15.05.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from typing import Any
from ampel.types import StockId
from ampel.base.AmpelABC import AmpelABC
from ampel.base.decorator import abstractmethod
from ampel.base.LogicalUnit import LogicalUnit
from ampel.content.DataPoint import DataPoint


class AbsT0Unit(AmpelABC, LogicalUnit, abstract=True):
	"""
	A unit that creates :class:`datapoints <ampel.content.DataPoint.DataPoint>` for Ampel

	Before new datapoint are inserted into the database, they are customized (or 'ampelized' if you will),
	in order to later enable the use of short and flexible queries.
	The cutomizations are light, most of the original information is kept.
	For example, in the case of ZiDataPointShaper:
		* The field candid is renamed in id
		* A new field 'tag' is created
		...
	"""

	@abstractmethod
	def process(self, arg: Any, stock: None | StockId = None) -> list[DataPoint]:
		"""
		Convert an external object to Ampel format
		"""
