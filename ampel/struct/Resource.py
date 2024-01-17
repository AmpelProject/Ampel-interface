#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/struct/Resource.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                19.12.2022
# Last Modified Date:  19.12.2022
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from collections.abc import Sequence
from typing import Any

from ampel.types import Tag


class Resource:
	"""
	Potentialy created by T3 units aiming at generating resources dynamically
	(ex: T3AuthTokenGenerator). These resources should be saved in T3Store.
	A note regarding provenance: resources - unlike unit configurations - are not tracked.
	The config of T3AuthTokenGenerator is traced, the output of its process()
	method (type: UBson | UnitResult) will be recorded if a non-null value is returned
	(useful for debugging purposes for example) but the generated resource saved in
	T3Store won't be and will vanish after run-time.
	"""

	__slots__ = 'name', 'value', 'tag', 'extra'

	#: id / label. Should match logical unit resource definition in most cases
	name: str

	#: serializability is required if multiprocessing is used
	value: Any

	#: could be used for permission purposes
	tag: None | Tag | Sequence[Tag]

	extra: None | dict[str, Any]


	def __init__(self,
		name: str,
		value: Any,
		tag: None | Tag | Sequence[Tag] = None,
		extra: None | dict[str, Any] = None
	) -> None:
		self.name = name
		self.value = value
		self.tag = tag
		self.extra = extra


	def dict(self) -> dict[str, Any]:
		return {
			'name': self.name,
			'value': self.value,
			'tag': self.tag,
			'extra': self.extra
		}
