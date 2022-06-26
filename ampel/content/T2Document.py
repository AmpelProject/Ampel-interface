#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/content/T2Document.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                13.01.2018
# Last Modified Date:  25.06.2022
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from typing import TypedDict
from typing_extensions import Required
from collections.abc import Sequence
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
	stock: Required[StockId | Sequence[StockId]]

	#: Optional source origin (avoids potential stock collision between different data sources)
	origin: int

	#: Name of the unit to be run. This may be hashed for performance reasons.
	unit: Required[UnitId]

	#: Configuration hash, if unit defaults were overridden. The underlying values can be resolved with
	#: :meth:`UnitLoader.get_init_config() <ampel.core.UnitLoader.UnitLoader.get_init_config>`
	config: Required[None | int]

	#: References to input data
	link: Required[T2Link]

	#: visible by any projection (not channel bound)
	tag: Sequence[Tag]

	#: Ampel channel(s) associated with this document
	channel: Required[Sequence[ChannelId]]

	#: Records of activity on this document
	meta: Required[Sequence[MetaRecord]]

	#: Name of the database collection holding the input data (t1 if unspecified)
	#: (enables efficient DB queries at T3 level)
	col: str

	#: DocumentCode.NEW for new T2 document, DocumentCode.OK if computation was successful
	code: Required[int]

	#: value(s) returned by T2 unit execution(s)
	body: Required[Sequence[UBson]]
