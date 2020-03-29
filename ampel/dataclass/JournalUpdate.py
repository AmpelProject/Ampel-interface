#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/dataclass/JournalUpdate.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 15.10.2018
# Last Modified Date: 14.02.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Any, Dict, List, Union
from pydantic.dataclasses import dataclass
from ampel.types import ChannelId


@dataclass(frozen=True)
class JournalUpdate:
	id: Union[ChannelId, List[ChannelId]]
	content: Dict[str, Any]
	ext: bool = False
