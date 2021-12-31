#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/content/EventDocument.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 04.03.2021
# Last Modified Date: 18.04.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Union, TypedDict, Any, Literal
from collections.abc import Sequence
from ampel.enum.EventCode import EventCode
from ampel.types import ChannelId


class EventDocument(TypedDict, total=False):
	"""
	Specifications for documents saved into the ampel 'event' collection
	"""

	#: Name of the ampel process (may be hashed for performance reasons)
	process: Union[int, str]

	#: process version
	version: int

	#: Ever increasing global and unique run identifier
	run: int

	#: Optional identification of the associated execution layer
	tier: Literal[-1, 0, 1, 2, 3]

	#: clock time duration of the event
	duration: Union[int, float]

	#: Optional channel(s) associated with the underlying process
	channel: Union[ChannelId, Sequence[ChannelId]]

	#: A member of :class:`~ampel.enum.EventCode.EventCode`
	code: EventCode

	#: Optional extras
	extra: dict[str, Any]
