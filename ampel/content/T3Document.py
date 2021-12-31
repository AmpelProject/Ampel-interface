#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/content/T3Document.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 23.02.2021
# Last Modified Date: 13.12.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Union, TypedDict, Any, Optional
from collections.abc import Sequence
from ampel.types import ChannelId, StockId, Tag, UBson
from ampel.content.MetaRecord import MetaRecord


class T3Document(TypedDict, total=False):
	"""
	Specifications for tier3 documents stored as BSON structures in the ampel DB
	"""

	#: Database primary id
	_id: Union[str, bytes]

	#: Name of the associated T3 process (may be a hash)
	process: Union[int, str]

	#: T3 unit name
	unit: str

	#: Hash of config (including defaults defined in unit class)
	confid: int

	#: T3 unit config (hash of possibly)
	config: dict[str, Any]

	#: Ever increasing global and unique run identifier
	run: int

	#: visible by any projection (not channel bound)
	tag: Union[Tag, Sequence[Tag]]

	#: Ampel channel(s) associated with this document
	channel: Union[ChannelId, Sequence[ChannelId]]

	#: Note: might contain versions of dependent external services
	#: (not only those used by t3 units but also potentially versions of resources
	#: used by session and/or complement routines)
	meta: MetaRecord

	#: Records session info, if any
	session: Optional[dict[str, Any]]

	#: Stock id of the views provided to unit
	stock: Optional[Sequence[StockId]]

	#: Optional source origin (avoids potential stock collision between different data sources)
	origin: int

	#: Negative values must be member of :class:`~ampel.enum.DocumentCode.DocumentCode`
	code: int

	#: Optional human friendly date time stamp
	datetime: str

	body: UBson
