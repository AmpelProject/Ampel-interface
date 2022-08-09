#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/struct/UnitResult.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                04.05.2021
# Last Modified Date:  20.04.2022
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from ampel.types import UBson, OneOrMany, Tag
from ampel.struct.JournalAttributes import JournalAttributes


class UnitResult:
	"""
	Structure potentialy returned by Ampel units to customize
	document information such as body, code, tag or the stock journal entry.
	"""

	__slots__ = 'body', 'tag', 'code', 'journal', 'adapter'

	def __init__(self,
		body: UBson = None,
		tag: None | OneOrMany[Tag] = None,
		code: None | int = None,
		journal: None | JournalAttributes = None,
		adapter: None | str = None
	) -> None:
		"""
		:param body: content for the field 'body' of the associated tier document
		:param tag: tag(s) to be added to the content of the field 'tag' of the associated tier document.
		Note that tags are 'public' attributes (they are not channel bound) and as such, they:
		- are visible by any projection
		- can be used for any db queries
		:param code: customize 'code' of the associated tier document:
		- Either a member of `ampel.enum.DocumentCode` such as DocumentCode.RERUN_REQUESTED (negative values)
		- Or any positive integer number (custom defined for a particular ampel unit)
		:param journal: customization of the journal entry associated with the stock document
		:param adapter: optionally specify which subclass of T3UnitResultAdapter should handle/morph
		this structure before its insertion into the database (ex: 'AmpelPlotAdapter')
		"""
		self.body = body
		self.tag = tag
		self.code = code
		self.journal = journal
		self.adapter = adapter
