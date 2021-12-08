#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsT3StageUnit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 23.02.2018
# Last Modified Date: 01.12.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Union, TypeVar, ClassVar, Type, Generic, Generator, Optional
from ampel.types import UBson, T3Send
from ampel.view.SnapView import SnapView
from ampel.view.T3Store import T3Store
from ampel.base.AmpelABC import AmpelABC
from ampel.base.decorator import abstractmethod
from ampel.base.LogicalUnit import LogicalUnit
from ampel.struct.UnitResult import UnitResult

T = TypeVar("T", bound=SnapView)


class AbsT3StageUnit(Generic[T], AmpelABC, LogicalUnit, abstract=True):
	""" Generic abstract class for T3 units receiving a SnapView generator """

	# avoid introspection at run-time
	_View: ClassVar[Type[T]] = SnapView # type: ignore[assignment]

	@abstractmethod
	def process(self,
		gen: Generator[T, T3Send, None],
		t3s: Optional[T3Store] = None
	) -> Union[UBson, UnitResult]:
		"""
		T3 units receive SnapView instances (or subclasses of) via a generator.
		The method gen.send(...) applies a modification to the last view yielded by the generator
		unless a stock id is provided via a tuple.
		Use gen.send(JournalAttributes) to customize the journal of the stock document associated with the view.
		Use gen.send(StockAttributes) to customize the stock tags or name (or journal) associated with the view.
		Use gen.send((StockId, JournalAttributes)) to customize the journal for a view other than the most recent,
		e.g. when processing in batches.
		Optional parameter t3s provides a t3 store containing t3 views.
		The content of the store is dependent on the configuration of the 'supply' option
		of the underlying t3 process config.
		"""
