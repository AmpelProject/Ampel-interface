#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsT3Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 23.02.2018
# Last Modified Date: 17.02.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Sequence, Tuple, Optional, Dict, Any
from ampel.abc import abstractmethod, defaultmethod
from ampel.abstract.AbsDataUnit import AbsDataUnit
from ampel.view.SnapView import SnapView
from ampel.dataclass.JournalUpdate import JournalUpdate


class AbsT3Unit(AbsDataUnit, abstract=True):

	@defaultmethod
	def post_init(self, context: Optional[Dict[str, Any]]) -> None:
		"""
		Method called after contructor call by parent processor class

		:param context: a dictionary containing context information,
		which can be requested in the process configuration.
		Examples of context information are:
		- Date and time the current process was last run
		- Number of alerts processed since then

		Note: custom context information can be added to this dict by
		implementing a class inheriting AbsT3ContextAppender (in ampel.abstract)
		and by requesting the custom unit in the process configuration
		"""
		pass


	@abstractmethod
	def add(self, views: Tuple[SnapView, ...]) -> Sequence[JournalUpdate]:
		""" Implementing T3 units get SnapViews via this this method """


	@defaultmethod
	def done(self) -> None:
		""" Method called after all data have been processed """
		pass
