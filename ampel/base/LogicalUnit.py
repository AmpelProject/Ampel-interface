#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/base/LogicalUnit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 12.10.2019
# Last Modified Date: 22.06.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Tuple, Dict, Any, Optional, ClassVar
from ampel.protocol.LoggerProtocol import LoggerProtocol
from ampel.base.AmpelBaseModel import AmpelBaseModel
from ampel.abstract.Secret import Secret


class LogicalUnit(AmpelBaseModel):
	"""
	Logical as in: performing logic operations of ampel's tier: add, combine, augment, synthetise.
	Base for standardized t0, t1, t2 and t3 units.
	Note that the defined parameters must all be serializable
	"""

	#: Resources requirements as class variable (passed on to and merged with subclasses).
	require: ClassVar[Optional[Tuple[str, ...]]] = None

	#: a dictionary containing session information, which can be requested in process configuration.
	#: Example of session information: date and time the current process was last run
	session_info: Optional[Dict[str, Any]] = None

	#: Private variable potentially set by UnitLoader for provenance purposes. Either:
	#: * 0 if provanance flag is False
	#: * -1 in case model content is not serializable
	#: * any other signed int value
	_trace_id: int = 0

	# Some unit contributors might want to restrict units usage
	# by scoping them to their respective distribution name (str)
	# private: ClassVar[Optional[str]] = None


	@classmethod
	def __init_subclass__(cls, **kwargs) -> None:
		super().__init_subclass__(**kwargs) # type: ignore
		setattr(cls, "resource",
			set(getattr(cls, "resource", None) or []) | {
				el for base in cls.__bases__
				for el in (getattr(base, 'resource', None) or [])
			}
		)


	def __init__(self,
		logger: LoggerProtocol,
		resource: Optional[Dict[str, Any]] = None,
		**kwargs
	) -> None:
		"""
		Note: logical units are initialized (by UnitLoader) as follows:
		* ctor
		* if available, secrets are resolved
		* if defined by sub-class, post_init() is called
		"""

		if logger is None:
			raise ValueError("Parameter logger cannot be None")

		AmpelBaseModel.__init__(self, **kwargs)

		d = self.__dict__
		self._trace_content = {
			k: d[k] for k in sorted(d)
			if not isinstance(d[k], Secret) and
			k not in ("session_info", "logger")
		}

		self.logger = logger

		if resource:
			# self._trace_content['require'] = self.require
			self.resource = resource
