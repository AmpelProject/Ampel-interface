#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/content/StockRecord.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 28.12.2019
# Last Modified Date: 01.03.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Any, Sequence, Union, Optional, Dict, TypedDict
from ampel.type import StockId, ChannelId


class StockRecord(TypedDict):

	_id: StockId
	tag: Optional[Sequence[Union[int, str]]]
	channel: Optional[Sequence[ChannelId]]
	journal: Sequence[Dict[str, Any]]
	name: Optional[Sequence[Union[int, str]]]
	modified: Dict[str, Any]
	created: Dict[str, Any]
