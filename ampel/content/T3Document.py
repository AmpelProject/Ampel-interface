#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/content/T3Document.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                23.02.2021
# Last Modified Date:  25.06.2022
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from typing import TypedDict, Any
from typing_extensions import Required
from collections.abc import Sequence
from ampel.types import ChannelId, StockId, Tag, UBson, UnitId
from ampel.content.MetaRecord import MetaRecord


class T3Document(TypedDict, total=False):
	"""
	Specifications for tier3 documents stored as BSON structures in the ampel DB
	"""

	#: Database primary id
	_id: str | bytes

	#: Name of the associated T3 process (may be a hash)
	process: int | str

	#: T3 unit name
	unit: Required[UnitId]

	#: Hash of config (including defaults defined in unit class)
	confid: Required[int]

	#: Resolved T3 unit config for convenience
	config: dict[str, Any]

	#: visible by any projection (not channel bound)
	tag: Tag | Sequence[Tag]

	#: Ampel channel(s) associated with this document
	channel: ChannelId | Sequence[ChannelId]

	#: Note: might contain versions of dependent external services
	#: (not only those used by t3 units but also potentially versions of resources
	#: used by session and/or complement routines)
	meta: Required[MetaRecord]

	#: Records session info, if any
	session: None | dict[str, Any]

	#: Stock id of the views provided to unit
	stock: None | Sequence[StockId]

	#: Optional source origin (avoids potential stock collision between different data sources)
	origin: int

	#: Negative values must be member of :class:`~ampel.enum.DocumentCode.DocumentCode`
	code: Required[int]

	#: Optional human friendly date time stamp
	datetime: str

	#: Optional in t1 and t3 docs, mandatory in t0 and t2 docs
	body: UBson
