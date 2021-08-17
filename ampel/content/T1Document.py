#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/content/T1Document.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : Unspecified
# Last Modified Date: 17.05.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Sequence, Literal, Union, TypedDict
from ampel.types import UBson, StockId, DataPointId, ChannelId, Tag, UnitId
from ampel.content.MetaRecord import MetaRecord


class T1Document(TypedDict, total=False):
	"""
	A symbolic collection of :class:`~ampel.content.DataPoint.DataPoint`,
	representing the state of a stock at a given point in time as viewed
	through one or more channels.

	Dict containing 1 or more of the following items:
	"""

	#: Name of AbsT1ComputeUnit potentially associated with this doc
	unit: UnitId

	#: Optional hashed config of t1 unit
	config: int

	#: stock(s) this doc is associated to
	stock: Union[StockId, Sequence[StockId]]

	#: Optional instrument/source identifier
	origin: int

	#: Result of AbsT1CombineUnit units
	dps: Sequence[DataPointId]

	#: intger hash hash of dps (referenced by stated T2 units)
	link: int

	#: channel(s) associated with this doc
	channel: Sequence[ChannelId]

	#: DocumentCode.NEW for T1 units requiring computation, DocumentCode.OK otherwise
	code: int

	#: Set by ingesters (ex: ZTF_PUB)
	tag: Sequence[Tag]

	#: References among other things the id of process invocation that created this doc
	meta: Sequence[MetaRecord]

	#: Ampel tier of the process that created this doc (-1 is ops)
	tier: Literal[-1, 0, 1, 3]

	#: Potential result of AbsT1ComputeUnit subclasses
	body: Sequence[UBson]
