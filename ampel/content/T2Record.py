#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/content/T2Record.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 13.01.2018
# Last Modified Date: 06.06.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Sequence, Union, Optional, TypedDict
from ampel.type import ChannelId, StockId, DataPointId, Tag
from ampel.content.T2SubRecord import T2SubRecord

T2Links = Union[bytes, DataPointId, StockId]


class T2Record(TypedDict, total=False):
	"""
	Specification of a calculation based on a :class:`~ampel.content.StockRecord.StockRecord`,
	:class:`~ampel.content.DataPoint.DataPoint`, or :class:`~ampel.content.Compound.Compound`.
	
	This is a dict containing 1 or more of the following items:
	"""

	# Indexed values
	#: Database key
	_id: bytes
	#: Stock associated with the input data 
	stock: Union[StockId, Sequence[StockId]]

	# Compound index
	#: Name of the unit to be run. This may be hashed for performance reasons.
	unit: Union[int, str]
	#: Configuration hash, if unit defaults were overridden. The underlying
	#: values can be resolved with
	#: :meth:`UnitLoader.get_init_config() <ampel.core.UnitLoader.UnitLoader.get_init_config>`
	config: Optional[int]
	#: References to input data
	link: Union[T2Links, Sequence[T2Links]]

	# Non-indexed values
	tag: Optional[Sequence[Tag]]
	channel: Sequence[ChannelId]
	#: Name of the database collection holding the input data
	col: Optional[str]
	#: Identifier of the process that created this record
	run: Union[int, Sequence[int]]
	#: A member of :class:`~ampel.t2.T2RunState.T2RunState`
	status: int
	#: value(s) returned by T2 unit execution(s)
	body: Optional[Sequence[T2SubRecord]]
