#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/content/Compound.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : Unspecified
# Last Modified Date: 13.02.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Sequence, Literal, TypedDict, Union
from ampel.type import StockId, ChannelId, DataPointId

class CompoundElement(TypedDict, total=False):
	"""
	Annotated reference to a :class:`~ampel.content.DataPoint.DataPoint`

	This is a dict containing 1 or more of the following items:
	"""
	id: DataPointId
	tag: Sequence[Union[int, str]]
	excl: Union[int, str] #: exclusion reason

class Compound(TypedDict, total=False):
	"""
	A symbolic collection of :class:`~ampel.content.DataPoint.DataPoint`,
	representing the state of a stock at a given point in time as viewed
	through one or more channels.

	This is a dict containing 1 or more of the following items:
	"""
	#: unique identifier (database key)
	_id: bytes
	tag: Sequence[Union[int, str]]
	#: stock that datapoints belong to
	stock: Union[StockId, Sequence[StockId]]
	#: channel(s) that selected the datapoints
	channel: Union[ChannelId, Sequence[ChannelId]]
	#: references to datapoints
	body: Sequence[Union[DataPointId, CompoundElement]]
	#: tier of process that created this
	tier: Literal[0, 1, 2, 3]
	#: id of process invocation that created this
	run: Union[int, Sequence[int]]
	#: UNIX epoch when this was created
	added: float
	#: number of referenced datapoints
	len: int
