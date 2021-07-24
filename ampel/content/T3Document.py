#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/content/T3Document.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 23.02.2021
# Last Modified Date: 18.04.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from bson import ObjectId
from typing import Sequence, Union, TypedDict
from ampel.types import ChannelId, StockId, Tag, UBson
from ampel.content.MetaRecord import MetaRecord


class T3Document(TypedDict, total=False):
	"""
	Specifications for tier3 documents stored as BSON structures in the ampel DB
	"""

	#: Database primary id (contains time of creation)
	_id: ObjectId

	#: Name of the associated T3 process (may be a hash)
	process: Union[int, str]

	#: T3 unit name
	unit: str

	#: T3 unit config (hashed)
	config: int

	#: Ever increasing global and unique run identifier
	run: int

	channel: Union[ChannelId, Sequence[ChannelId]]

	#: Note: might contain versions of dependent external services
	#: (not only those used by t3 units but also potentially versions of resources
	#: used by session and/or complement routines)
	meta: MetaRecord

	#: Stock id of the views provided to unit
	stock: Sequence[StockId]

	#: Optional source origin (avoids potential stock collision between different data sources)
	origin: int

	tag: Sequence[Tag]

	#: Negative values must be member of :class:`~ampel.enum.DocumentCode.DocumentCode`
	code: int

	body: UBson
