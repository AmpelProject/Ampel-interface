#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/base/LogicalUnit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 12.10.2019
# Last Modified Date: 13.12.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Any, Optional, ClassVar
from ampel.types import Traceless, TRACELESS
from ampel.protocol.LoggerProtocol import LoggerProtocol
from ampel.base.AmpelBaseModel import AmpelBaseModel
from ampel.secret.Secret import Secret

ttf = type(Traceless)


class LogicalUnit(AmpelBaseModel):
	"""
	Logical as in: performing logic operations of ampel's tier: add, combine, augment, synthetise.
	Base for standardized t0, t1, t2 and t3 units.
	Note that the defined parameters must all be serializable
	"""

	logger: Traceless[LoggerProtocol]

	#: Resources requirements as class variable (passed on to and merged with subclasses).
	require: ClassVar[Optional[tuple[str, ...]]] = None

	resource: Traceless[Optional[dict[str, Any]]] = None

	#: Private variable potentially set by UnitLoader for provenance purposes. Either:
	#: * None if provanance flag is False
	#: * 0 in case model content is not serializable
	#: * any other signed int value
	_trace_id: Optional[int] = None

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


	def __init__(self, **kwargs) -> None:
		"""
		Note: logical units are initialized (by UnitLoader) as follows:
		* ctor
		* if available, secrets are resolved
		* if defined by sub-class, post_init() is called
		"""

		AmpelBaseModel.__init__(self, **kwargs)

		d = self.__dict__
		excl = {
			k for k, v in self._annots.items()
			if type(v) is ttf and v.__metadata__[0] == TRACELESS
		}

		self._trace_content = {
			k: d[k]
			for k in sorted(d)
			if k not in excl and not isinstance(d[k], Secret)
		}
