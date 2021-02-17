#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsTiedPointT2Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 16.02.2021
# Last Modified Date: 17.02.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Dict, Union, Optional, Literal, Tuple, Sequence
from ampel.base import abstractmethod
from ampel.type import T2UnitResult
from ampel.abstract.AbsTiedT2Unit import AbsTiedT2Unit
from ampel.content.DataPoint import DataPoint
from ampel.view.T2DocView import T2DocView


class AbsTiedPointT2Unit(AbsTiedT2Unit, abstract=True):
	"""
	Later
	"""

	# See EligibleModel docstring for more info
	ingest: Optional[Dict[
		Literal['eligible'],
		Union[
			Literal['first', 'last', 'all'],
			Tuple[int, Optional[int], Optional[int]]
		]
	]]


	@abstractmethod
	def run(self, datapoint: DataPoint, t2_views: Sequence[T2DocView]) -> T2UnitResult:
		"""
		Returned object should contain computed science results to be saved into the DB.
		Notes: dict must have only string keys and values must be bson encodable
		"""
