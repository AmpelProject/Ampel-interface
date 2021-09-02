#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/struct/StockAttributes.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 02.09.2021
# Last Modified Date: 02.09.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Optional, Sequence, Union
from ampel.types import Tag
from ampel.struct.JournalAttributes import JournalAttributes


class StockAttributes:
	"""
	Structure potentialy used by Ampel units to customize
	stock tags, names or journal entries.
	"""

	__slots__ = 'tag', 'journal', 'name'

	#: Stock document tag(s)
	tag: Optional[Union[Tag, Sequence[Tag]]]

	#: Journal entry customization
	journal: Optional[JournalAttributes]

	#: stock external name(s) / reference id(s)
	name: Optional[Union[str, Sequence[str]]]


	def __init__(self,
		tag: Optional[Union[Tag, Sequence[Tag]]] = None,
		journal: Optional[JournalAttributes] = None,
		name: Optional[Union[str, Sequence[str]]] = None
	) -> None:
		"""
		:param tag: stock document tag(s)
		:param journal: Journal entry customization
		:param name: stock external name(s) / reference id(s)
		"""
		self.tag = tag
		self.journal = journal
		self.name = name
