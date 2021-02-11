#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsTiedStateT2Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 11.03.2020
# Last Modified Date: 11.02.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Sequence, Dict, Any, Union, Optional
from ampel.base import abstractmethod
from ampel.type import T2UnitResult
from ampel.abstract.AbsTiedT2Unit import AbsTiedT2Unit
from ampel.content.DataPoint import DataPoint
from ampel.content.Compound import Compound
from ampel.view.T2DocView import T2DocView


class AbsTiedStateT2Unit(AbsTiedT2Unit, abstract=True):
	"""
	Abstract class for state T2 units depending on other T2 units.
	Run method features the additional parameter 't2_records' which should contain
	prerequisite T2 results (`T2Records <ampel.content.T2Record.T2Record>`)
	"""

	@staticmethod
	@abstractmethod(force=True)
	def get_link(
		link_override: Dict[str, Any],
		compound: Compound,
		datapoints: Sequence[DataPoint]
	) -> Optional[Union[int, bytes]]:
		"""
		Method used by T2Processor if 't2_dependency' is specified in the t2 config dict
		and if 'link_override' is defined in there.

		T2Processor needs to retrieve the T2Records of units tied with this unit.
		If unspecified in config, t2 dependencies are resolved - for each unit defined in get_tied_unit_names() -
		using the db match query: {unit: <unit_name>, config: None, link: <same link as root doc>}.

		This behavior is overridable/customizable by adding the keyword 't2_dependency' to the t2 config dict.
		The value of t2_dependency should be of type Union[T2Dependency, List[T2Dependency]].
		The parameter 'link_override' in T2Dependency allows to link this state T2 with a different value
		than the one registered as 'link' in the T2Record (which is the _id of a compound document for state t2s).

		This method thus enables to tie a state T2 with the result of a point t2
		(the returned link could be the id of the first datapoint contained in the compound)

		:returns: the value of 'link' (tied t2 document) to be matched
		"""

	@abstractmethod
	def run(self,
		compound: Compound,
		datapoints: Sequence[DataPoint],
		t2_records: Sequence[T2DocView]
	) -> T2UnitResult:
		"""
		Returned object should contain computed science results to be saved into the DB.
		Notes: dict must have only string keys and values must be bson encodable
		"""
