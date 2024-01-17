#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/content/EventDocument.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                04.03.2021
# Last Modified Date:  15.01.2023
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from collections.abc import Sequence
from typing import Any, Literal, TypedDict

from typing_extensions import Required

from ampel.enum.EventCode import EventCode
from ampel.types import ChannelId


class EventDocument(TypedDict, total=False):
	"""
	Specifications for documents saved into the ampel 'event' collection
	"""

	#: Name of the ampel process (may be hashed for performance reasons)
	process: Required[int | str]

	#: Task number (job system)
	task: int

	#: Process version
	version: int

	#: Ever increasing global and unique run identifier
	run: Required[int]

	#: Hash of potentially underlying job schema
	jobid: None | int

	#: Identification of the associated execution layer (-1: ops)
	tier: Literal[-1, 0, 1, 2, 3]

	#: Clock time event duration
	duration: int | float

	#: channel(s) associated with the underlying process
	channel: ChannelId | Sequence[ChannelId]

	#: A member of :class:`~ampel.enum.EventCode.EventCode`
	code: Required[EventCode]

	#: Optional extras
	extra: dict[str, Any]
