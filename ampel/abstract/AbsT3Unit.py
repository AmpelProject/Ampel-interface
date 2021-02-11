#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsT3Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 23.02.2018
# Last Modified Date: 08.06.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Tuple, Optional, Union, Dict, Any, TypeVar, Generic
from ampel.type import StockId
from ampel.base import abstractmethod, defaultmethod, AmpelABC, DataUnit
from ampel.view.SnapView import SnapView
from ampel.struct.JournalTweak import JournalTweak

T = TypeVar("T", bound=SnapView)


class AbsT3Unit(Generic[T], AmpelABC, DataUnit, abstract=True):
	"""
	General generic abstract class for T3 units.
	Inherit this class if your unit is compatible with multiple type of views,
	that is if you access only SnapView fields or perform dedicated isinstance checks.

	:param context:
	  a dictionary containing context information, which can be
	  requested in the process configuration. Examples of context information are:
	  
	    - Date and time the current process was last run
	    - Number of alerts processed since then
	  
	  .. note::
	    Custom context information can be added to this dict by
	    implementing a subclass of
	    :class:`~ampel.t3.context.AbsT3RunContextAppender.AbsT3RunContextAppender`
	    and adding the custom unit to the process configuration
	"""

	context: Optional[Dict[str, Any]]


	@abstractmethod
	def add(self, views: Tuple[T, ...]) -> Optional[Union[JournalTweak, Dict[StockId, JournalTweak]]]:
		""" Implementing T3 units get SnapView (or subclasses of SnapView) instances via this method """
		...


	@defaultmethod
	def done(self) -> None:
		""" Method called after all data have been processed """
		pass
