#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsTiedStateT2Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 11.03.2020
# Last Modified Date: 08.06.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Union, Iterable, Sequence, TypedDict, Optional, Dict, Any
from ampel.type import T2UnitResult
from ampel.base import abstractmethod, AmpelABC, DataUnit
from ampel.content.Compound import Compound
from ampel.content.DataPoint import DataPoint
from ampel.content.T2Record import T2Record


class Dependency(TypedDict):
	#: T2 unit
	unit: str
	#: Parameters, if any
	config: Optional[Dict[str, Any]]


class AbsTiedStateT2Unit(AmpelABC, DataUnit, abstract=True):
	"""
	Generic abstract class for T2 units that depend on other T2 units.
	"""

	#: Prerequisite T2 calculations. Their output `T2Records <ampel.content.T2Record.T2Record>`_ will be supplied as arguments to :meth:`run`.
	dependency: Optional[Union[Dependency, Sequence[Dependency]]]

	@abstractmethod
	def run(self, # type: ignore
		compound: Compound,
		datapoints: Iterable[DataPoint],
		t2_records: Sequence[T2Record]
	) -> T2UnitResult:
		"""
		Returned object should contain computed science results to be saved into the DB.
		Notes: dict must have only string keys and values must be bson encodable
		"""
