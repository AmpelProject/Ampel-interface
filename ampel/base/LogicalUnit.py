#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/base/LogicalUnit.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                12.10.2019
# Last Modified Date:  05.11.2025
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from typing import Any, ClassVar

from ampel.base.AmpelABC import AmpelABC
from ampel.base.AmpelUnit import AmpelUnit
from ampel.protocol.LoggerProtocol import LoggerProtocol
from ampel.types import Traceless


class LogicalUnit(AmpelABC, AmpelUnit, abstract=True):
	"""
	Base class for standardized Ampel units that perform logical operations within a specific processing tier.

	LogicalUnit represents the lower-level worker units in the Ampel framework, responsible for implementing
	tier-specific logic such as adding, combining, augmenting, or synthesizing data. These units are tightly
	coupled to the structure of their respective tier (T0, T1, T2, T3) and are expected to conform to an
	interface contract defined by abstract base classes (e.g., AbsT0Unit, AbsPointT2Unit, ...).

	LogicalUnits enforce:
	- Standardized input/output signatures via tier-specific abstract interfaces
	- Serializable configuration parameters for reproducibility and traceability
	- A consistent initialization managed by UnitLoader:
	  * Constructor invocation with potential secret resolution
	  * Attachment of run-time resources
	  * Post-initialization via `post_init()` if defined

	Subclasses of this class are both structurally validated and behaviorally constrained.
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
		super().__init_subclass__(**kwargs)
		cls.require = tuple(
			set(getattr(cls, "require", None) or []) | {
				el for base in cls.__bases__
				for el in (getattr(base, "require", None) or [])
			}
		)
