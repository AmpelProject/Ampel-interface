#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsTiedStockT2Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 17.02.2021
# Last Modified Date: 17.02.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Sequence
from ampel.base import abstractmethod
from ampel.type import T2UnitResult
from ampel.abstract.AbsTiedT2Unit import AbsTiedT2Unit
from ampel.content.StockDocument import StockDocument
from ampel.view.T2DocView import T2DocView


class AbsTiedStockT2Unit(AbsTiedT2Unit, abstract=True):
	""" Later """

	@abstractmethod
	def run(self, stock: StockDocument, t2_view: Sequence[T2DocView]) -> T2UnitResult:
		"""
		Returned object should contain computed science results to be saved into the DB.
		Notes: dict must have only string keys and values must be bson encodable
		"""
