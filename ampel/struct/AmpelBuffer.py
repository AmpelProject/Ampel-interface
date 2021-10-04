#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/struct/AmpelBuffer.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 31.05.2018
# Last Modified Date: 04.04.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Optional, Dict, List, Any, TypedDict, Literal
from ampel.types import StockId
from ampel.content.StockDocument import StockDocument
from ampel.content.DataPoint import DataPoint
from ampel.content.T1Document import T1Document
from ampel.content.T2Document import T2Document
from ampel.content.T3Document import T3Document
from ampel.content.LogDocument import LogDocument

# Please update BufferKey on AmpelBuffer udpates
# There is currently unfortunately no way of extracting a Literal out of a TypedDict
BufferKey = Literal['id', 'stock', 't0', 't1', 't2', 't3', 'logs', 'extra']

class AmpelBuffer(TypedDict, total=False):
	"""
	Content bundle used to build :class:`~ampel.view.SnapView.SnapView`.
	
	This is a dict containing 1 or more of the following items:
	"""
	# Could stock be of type List[StockDocument] to enable hybrid/dual transients ?
	id: StockId
	stock: Optional[StockDocument]
	t0: Optional[List[DataPoint]]
	t1: Optional[List[T1Document]]
	t2: Optional[List[T2Document]]
	t3: Optional[List[T3Document]]
	logs: Optional[List[LogDocument]]
	extra: Optional[Dict[str, Any]]