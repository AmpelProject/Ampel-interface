#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsTiedStateT2Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 11.03.2020
# Last Modified Date: 11.03.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Union, Iterable, Sequence
from ampel.abc import abstractmethod
from ampel.abstract.AbsStateT2Unit import AbsStateT2Unit
from ampel.content.Compound import Compound
from ampel.content.DataPoint import DataPoint
from ampel.content.T2Record import T2Record
from ampel.t2.T2Result import T2Result


class AbsTiedStateT2Unit(AbsStateT2Unit, abstract=True):
	"""
	Generic top level abstract class for t2 units
	Known sub-class: AbsTiedLightCurveT2
	"""

	dependency: Union[str, Sequence[str]]

	@abstractmethod
	def run(self, # type: ignore
		compound: Compound,
		datapoints: Iterable[DataPoint],
		t2_records: Sequence[T2Record]
	) -> T2Result:
		"""
		Returned T2Result dataclass should contain computed science results to be saved into the DB.
		Notes: dict must have only string keys and values must be bson encodable
		"""
