#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/content/LogDocument.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 14.02.2020
# Last Modified Date: 01.03.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Sequence, Union, Optional, Any, Dict, TypedDict
from ampel.type import ChannelId, StockId

class LogDocument(TypedDict, total=False):
	"""
	A message produced by an Ampel unit during processing.

	This is a dict containing 1 or more of the following items:
	"""
	#: database key
	_id: bytes
	flag: int
	run: Union[int, Sequence[int]]
	msg: Optional[Union[str, Sequence[str]]]
	stock: Optional[Union[StockId, Sequence[StockId]]]
	channel: Optional[Union[ChannelId, Sequence[ChannelId]]]
	extra: Optional[Dict[str, Any]]
