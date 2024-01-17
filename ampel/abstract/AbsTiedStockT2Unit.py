#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/abstract/AbsTiedStockT2Unit.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                17.02.2021
# Last Modified Date:  03.04.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from collections.abc import Sequence

from ampel.abstract.AbsTiedT2Unit import AbsTiedT2Unit
from ampel.base.decorator import abstractmethod
from ampel.content.StockDocument import StockDocument
from ampel.struct.UnitResult import UnitResult
from ampel.types import UBson
from ampel.view.T2DocView import T2DocView


class AbsTiedStockT2Unit(AbsTiedT2Unit, abstract=True):
	""" Later """

	@abstractmethod
	def process(self, stock: StockDocument, t2_view: Sequence[T2DocView]) -> UBson | UnitResult:
		"""
		Returned object should contain computed science results to be saved into the DB.

		.. note:: the returned dict must have only string keys and be BSON-encodable
		"""
