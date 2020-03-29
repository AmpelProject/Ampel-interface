#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsStockT2Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 28.12.2019
# Last Modified Date: 17.02.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from ampel.abc import abstractmethod, defaultmethod
from ampel.abstract.AbsDataUnit import AbsDataUnit
from ampel.content.StockRecord import StockRecord
from ampel.t2.T2Result import T2Result


class AbsStockT2Unit(AbsDataUnit, abstract=True):
	"""
	Top level abstract class for t2 units bound to transient doc
	"""

	@defaultmethod(check_super_call=True)
	def __init__(self, **kwargs) -> None:
		AbsDataUnit.__init__(self, **kwargs)
		self.post_init()


	def post_init(self) -> None:
		pass


	@abstractmethod
	def run(self, stock_record: StockRecord) -> T2Result:
		"""
		Returned T2Result dataclass should contain computed science results to be saved into the DB.
		Note: dict must have only string keys
		"""
