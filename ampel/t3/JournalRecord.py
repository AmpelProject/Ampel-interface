#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/t3/JournalRecord.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 12.12.2019
# Last Modified Date: 14.02.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from dataclasses import dataclass
from typing import Sequence, Union, Optional, Literal, Any, Dict
from ampel.types import ChannelId

@dataclass(frozen=True)
class JournalRecord:

	tier: Literal[0, 1, 2, 3]
	dt: float
	channels: Union[ChannelId, Sequence[ChannelId]]
	tags: Optional[Sequence[Union[int, str]]] = None
	unit: Optional[Union[int, str]] = None
	extra: Optional[Dict[str, Any]] = None
