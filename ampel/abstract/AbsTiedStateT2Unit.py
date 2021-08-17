#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsTiedStateT2Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 11.03.2020
# Last Modified Date: 03.04.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Sequence, Dict, Any, Union, Optional, Generic
from ampel.types import UBson, T
from ampel.struct.UnitResult import UnitResult
from ampel.view.T2DocView import T2DocView
from ampel.base.decorator import abstractmethod
from ampel.content.T1Document import T1Document
from ampel.content.DataPoint import DataPoint
from ampel.abstract.AbsTiedT2Unit import AbsTiedT2Unit
from ampel.model.StateT2Dependency import StateT2Dependency


class AbsTiedStateT2Unit(Generic[T], AbsTiedT2Unit, abstract=True):
	"""
	A T2 unit bound to a :class:`~ampel.content.T1Document.T1Document` (state of a stock),
	as well as the results of other T2 units
	"""

	t2_dependency: Sequence[StateT2Dependency[T]]

	@staticmethod
	@abstractmethod(force=True)
	def get_link(
		link_override: Dict[str, Any],
		compound: T1Document,
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
	def process(self,
		compound: T1Document,
		datapoints: Sequence[DataPoint],
		t2_views: Sequence[T2DocView]
	) -> Union[UBson, UnitResult]:
		"""
		Returned object should contain computed science results to be saved into the DB.

		.. note:: the returned dict must have only string keys and be BSON-encodable
		"""
