#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsT3Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 23.02.2018
# Last Modified Date: 17.06.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Union, TypeVar, ClassVar, Type, Generic, Generator
from ampel.types import UBson
from ampel.view.SnapView import SnapView
from ampel.base.AmpelABC import AmpelABC
from ampel.base.decorator import abstractmethod
from ampel.base.LogicalUnit import LogicalUnit
from ampel.struct.UnitResult import UnitResult
from ampel.struct.JournalAttributes import JournalAttributes

T = TypeVar("T", bound=SnapView)


class AbsT3Unit(Generic[T], AmpelABC, LogicalUnit, abstract=True):
	"""
	Generic abstract class for T3 units.

	:param session_info:
	  (defined in LogicalUnit)
	  a dictionary containing session information, which can be
	  requested in the process configuration. Examples of session information are:
	  
	    - Date and time the current process was last run
	    - Number of alerts processed since then
	  
	  .. note::
	    Custom session information can be added to this dict by implementing a subclass of
	    :class:`~ampel.session.AbsSessionInfo.AbsSessionInfo`
	    and adding the custom unit to the process configuration
	"""

	# avoid introspection at run-time
	_View: ClassVar[Type[T]] = SnapView # type: ignore[assignment]


	@abstractmethod
	def process(self, gen: Generator[T, JournalAttributes, None]) -> Union[UBson, UnitResult]:
		"""
		Implementing T3 units receive SnapView instances (or subclasses of) via this method.
		Use gen.send(JournalAttributes) to customize the journal of the stock document associated with a specific view.
		"""
