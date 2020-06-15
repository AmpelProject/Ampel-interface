#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsT1Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 11.10.2019
# Last Modified Date: 18.03.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Sequence, Generic, TypeVar, ClassVar, Type, Iterable
from ampel.base import abstractmethod, AmpelABC, DataUnit
from ampel.type import StockId, ChannelId
from ampel.content.DataPoint import DataPoint
from ampel.ingest.CompoundBluePrint import CompoundBluePrint

T = TypeVar("T", bound=CompoundBluePrint)

class AbsT1Unit(Generic[T], AmpelABC, DataUnit, abstract=True):

	BluePrintClass: ClassVar[Type] = CompoundBluePrint

	@abstractmethod
	def combine(self,
		stock_id: StockId,
		datapoints: Sequence[DataPoint],
		channels: Iterable[ChannelId]
	) -> T:
		...
