#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/base/LogicalUnit.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                12.10.2019
# Last Modified Date:  09.01.2022
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from typing import Any, ClassVar
from ampel.types import Traceless
from ampel.base.AmpelUnit import AmpelUnit
from ampel.protocol.LoggerProtocol import LoggerProtocol


class LogicalUnit(AmpelUnit):
	"""
	Logical as in: performing logic operations of ampel's tier: add, combine, augment, synthetise.
	Base for standardized t0, t1, t2 and t3 units.
	Note:
	- the defined parameters must be serializable
	- logical units are initialized (by UnitLoader) as follows:
	* ctor
	* if available, secrets are resolved
	* if defined by sub-class, post_init() is called
	"""

	logger: Traceless[LoggerProtocol]

	#: Resources requirements as class variable (passed on to and merged with subclasses).
	require: ClassVar[None | tuple[str, ...]] = None

	resource: Traceless[None | dict[str, Any]] = None

	#: Private variable potentially set by UnitLoader for provenance purposes. Either:
	#: * None if provanance flag is False
	#: * 0 in case model content is not serializable
	#: * any other signed int value
	_trace_id: None | int = None

	# Some unit contributors might want to restrict units usage
	# by scoping them to their respective distribution name (str)
	# private: ClassVar[None | str] = None


	@classmethod
	def __init_subclass__(cls, **kwargs) -> None:
		super().__init_subclass__(**kwargs) # type: ignore
		setattr(cls, "require",
			set(getattr(cls, "require", None) or []) | {
				el for base in cls.__bases__
				for el in (getattr(base, 'require', None) or [])
			}
		)
