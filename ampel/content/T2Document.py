#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/content/T2Document.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 13.01.2018
# Last Modified Date: 23.03.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import TypedDict, Union, Optional, Sequence
from ampel.types import UBson, ChannelId, StockId, Tag, UnitId, T2Link
from ampel.content.MetaRecord import MetaRecord


class T2Document(TypedDict, total=False):
	"""
	Specifications for tier2 documents stored as BSON structures in the ampel DB.
	Calculations of the associated t2 unit is performed based on ampel data referenced by the attribute 'link'.
	Linked input data type can be either :class:`~ampel.content.StockDocument.StockDocument`,
	:class:`~ampel.content.DataPoint.DataPoint`, or :class:`~ampel.content.T1Document.T1Document`.
	"""

	#: Stock id associated with the data
	stock: Union[StockId, Sequence[StockId]]

	#: Optional source origin (avoids potential stock collision between different data sources)
	origin: int

	#: Name of the unit to be run. This may be hashed for performance reasons.
	unit: UnitId

	#: Configuration hash, if unit defaults were overridden. The underlying values can be resolved with
	#: :meth:`UnitLoader.get_init_config() <ampel.core.UnitLoader.UnitLoader.get_init_config>`
	config: Optional[int]

	#: References to input data
	link: T2Link

	tag: Sequence[Tag]
	channel: Sequence[ChannelId]

	#: Records of activity on this document
	meta: Sequence[MetaRecord]

	#: Name of the database collection holding the input data
	#: (enables efficient DB queries at T3 level)
	col: str

	#: Ever increasing global and unique run identifier
	run: Union[int, Sequence[int]]

	#: DocumentCode.NEW for new T2 document, DocumentCode.OK if computation was successful
	code: int

	#: value(s) returned by T2 unit execution(s)
	body: Sequence[UBson]
