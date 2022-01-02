#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/content/EventDocument.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                04.03.2021
# Last Modified Date:  18.04.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from typing import TypedDict, Any, Literal
from collections.abc import Sequence
from ampel.enum.EventCode import EventCode
from ampel.types import ChannelId


class EventDocument(TypedDict, total=False):
	"""
	Specifications for documents saved into the ampel 'event' collection
	"""

	#: Name of the ampel process (may be hashed for performance reasons)
	process: int | str

	#: process version
	version: int

	#: Ever increasing global and unique run identifier
	run: int

	#: Optional identification of the associated execution layer
	tier: Literal[-1, 0, 1, 2, 3]

	#: clock time duration of the event
	duration: int | float

	#: Optional channel(s) associated with the underlying process
	channel: ChannelId | Sequence[ChannelId]

	#: A member of :class:`~ampel.enum.EventCode.EventCode`
	code: EventCode

	#: Optional extras
	extra: dict[str, Any]
