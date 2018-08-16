#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/base/ScienceRecord.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 13.01.2018
# Last Modified Date: 04.07.2018
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from dataclasses import dataclass
from typing import List, Dict
from bson import Binary

@dataclass(frozen=True)
class ScienceRecord:
	"""
	tran_id: transient id
	t2_unit_id: T2 unit id
	compound_id: Compound id
	results: T2 unit return values
	info: extra info
	"""
	tran_id: int
	t2_unit_id: str
	compound_id: Binary
	results: List[Dict]
	info: dict = None

	def get_results(self):
		""" """
		return self.results


	def get_t2_unit_id(self):
		""" """
		return self.t2_unit_id


	def get_compound_id(self):
		""" """
		return self.compound_id


	def has_error(self):
		return self.info.get('hasError')
