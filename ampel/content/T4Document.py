#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/content/T4Document.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                03.04.2023
# Last Modified Date:  03.04.2023
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from collections.abc import Sequence
from typing import Any, TypedDict

from typing_extensions import Required

from ampel.content.MetaRecord import MetaRecord
from ampel.types import ChannelId, Tag, UBson, UnitId


class T4Document(TypedDict, total=False):
	""" Specifications for tier4 documents stored as BSON structures in the ampel DB """

	#: Database primary id
	_id: str | bytes

	#: Name of the associated T4 process (may be a hash)
	process: int | str

	#: T4 unit name
	unit: Required[UnitId]

	#: Hash of config (including defaults defined in unit class)
	confid: Required[int]

	#: Resolved T4 unit config for convenience
	config: dict[str, Any]

	#: visible by any projection (not channel bound)
	tag: Tag | Sequence[Tag]

	#: Ampel channel(s) associated with this document
	channel: ChannelId | Sequence[ChannelId]

	#: Note: might contain versions of dependent external services
	meta: Required[MetaRecord]

	#: Negative values must be member of :class:`~ampel.enum.DocumentCode.DocumentCode`
	code: Required[int]

	#: Optional human friendly date time stamp
	datetime: str

	#: Optional in t1, t3 and t4 docs, mandatory in t0 and t2 docs
	body: UBson
