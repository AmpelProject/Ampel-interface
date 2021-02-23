#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsStockT2Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 28.12.2019
# Last Modified Date: 08.06.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from ampel.type import T2UnitResult
from ampel.base import abstractmethod, AmpelABC, DataUnit
from ampel.content.StockDocument import StockDocument


class AbsStockT2Unit(AmpelABC, DataUnit, abstract=True):
	"""
	A T2 unit bound to a :class:`~ampel.content.StockDocument.StockDocument`
	"""


	@abstractmethod
	def run(self, stock_doc: StockDocument) -> T2UnitResult:
		"""
		Returned object should contain computed science results to be saved into the DB.

		.. note:: the returned dict must have only string keys and be BSON-encodable
		"""
