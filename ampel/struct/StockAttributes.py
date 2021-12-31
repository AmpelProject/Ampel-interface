#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/struct/StockAttributes.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 02.09.2021
# Last Modified Date: 02.09.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Optional, Union
from collections.abc import Sequence
from ampel.types import Tag
from ampel.struct.JournalAttributes import JournalAttributes


class StockAttributes:
	"""
	Structure potentialy used by Ampel units to customize
	journal entries along with stock tags or names.
	"""

	__slots__ = 'journal', 'tag', 'name'

	#: Journal entry customization (mandatory)
	journal: JournalAttributes

	#: Stock document tag(s)
	tag: Optional[Union[Tag, Sequence[Tag]]]

	#: stock external name(s) / reference id(s)
	name: Optional[Union[str, Sequence[str]]]


	def __init__(self,
		journal: JournalAttributes,
		tag: Optional[Union[Tag, Sequence[Tag]]] = None,
		name: Optional[Union[str, Sequence[str]]] = None
	) -> None:
		"""
		:param journal: Journal entry customization
		:param tag: stock document tag(s)
		:param name: stock external name(s) / reference id(s)
		"""
		self.journal = journal
		self.tag = tag
		self.name = name
