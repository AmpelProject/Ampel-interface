#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/abstract/AbsStockT2Unit.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                28.12.2019
# Last Modified Date:  11.06.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from ampel.types import Union, UBson
from ampel.struct.UnitResult import UnitResult
from ampel.content.StockDocument import StockDocument
from ampel.base.AmpelABC import AmpelABC
from ampel.base.decorator import abstractmethod
from ampel.base.LogicalUnit import LogicalUnit


class AbsStockT2Unit(AmpelABC, LogicalUnit, abstract=True):
	"""
	A T2 unit bound to a :class:`~ampel.content.StockDocument.StockDocument`
	"""

	@abstractmethod
	def process(self, stock_doc: StockDocument) -> UBson | UnitResult:
		"""
		Returned object should contain computed science results to be saved into the DB.

		.. note:: the returned dict must have only string keys and be BSON-encodable
		"""
