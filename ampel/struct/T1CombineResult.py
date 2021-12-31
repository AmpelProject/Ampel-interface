#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/struct/T1CombineResult.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 04.05.2021
# Last Modified Date: 17.06.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Optional, Any
from ampel.types import DataPointId


class T1CombineResult:
	"""
	Structure potentialy returned by Ampel AbsT1CombineUnit instances
	to customize code or meta of T1Documents.
	"""

	__slots__ = 'code', 'meta', 'dps'

	def __init__(self,
		dps: list[DataPointId],
		code: Optional[int] = None,
		meta: Optional[dict[str, Any]] = None
	) -> None:
		"""
		:param dps: ids of the datapoints to combine
		:param code: customize DocumentCode (ex: DocumentCode.RERUN_REQUESTED)
		:param meta: customize meta dict
		"""

		self.dps = dps
		self.code = code
		self.meta = meta


	def add_meta(self, key, value) -> 'T1CombineResult':

		if self.meta:
			if self.meta.get(key):
				if isinstance(self.meta.get(key), list):
					self.meta[key].append(value)
				else:
					self.meta[key] = [self.meta[key], value]
			else:
				self.meta[key] = value
		else:
			self.meta = {key: value}

		return self
