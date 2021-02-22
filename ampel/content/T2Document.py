#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/content/T2Document.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 13.01.2018
# Last Modified Date: 11.02.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Sequence, Union, Optional, TypedDict
from bson import ObjectId
from ampel.type import ChannelId, StockId, DataPointId, Tag
from ampel.content.T2Record import T2Record

T2Link = Union[bytes, DataPointId, StockId]


class T2Document(TypedDict, total=False):
	"""
	Specifications for tier2 documents stored as BSON structures in the ampel DB.
	Calculations of the associated t2 unit is performed based on ampel data referenced by the attribute 'link'.
	Linked input data type can be either :class:`~ampel.content.StockDocument.StockDocument`,
	:class:`~ampel.content.DataPoint.DataPoint`, or :class:`~ampel.content.Compound.Compound`.
	"""

	#: Database primary id
	_id: ObjectId

	#: Stock id associated with the data
	#: (multiple stock ids disabled for simplicity for now)
	stock: StockId

	#: Name of the unit to be run. This may be hashed for performance reasons.
	unit: Union[int, str]

	#: Configuration hash, if unit defaults were overridden. The underlying values can be resolved with
	#: :meth:`UnitLoader.get_init_config() <ampel.core.UnitLoader.UnitLoader.get_init_config>`
	config: Optional[int]

	#: References to input data
	link: Union[T2Link, Sequence[T2Link]]

	tag: Sequence[Tag]
	channel: Sequence[ChannelId]

	#: Name of the database collection holding the input data
	#: (enables efficient T3 DB queries)
	col: str

	#: Identifier of the process that created this record
	run: Union[int, Sequence[int]]

	#: A member of :class:`~ampel.enum.T2RunState.T2RunState`
	status: int

	#: value(s) returned by T2 unit execution(s)
	body: Sequence[T2Record]
