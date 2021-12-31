#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/struct/AmpelBuffer.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 31.05.2018
# Last Modified Date: 01.12.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Optional, Any, TypedDict, Literal, Union
from ampel.types import StockId
from ampel.content.StockDocument import StockDocument
from ampel.content.DataPoint import DataPoint
from ampel.content.T1Document import T1Document
from ampel.content.T2Document import T2Document
from ampel.content.LogDocument import LogDocument

# Please update BufferKey on AmpelBuffer udpates
# There is currently unfortunately no way of extracting a Literal out of a TypedDict
BufferKey = Literal['id', 'stock', 'origin', 't0', 't1', 't2', 'logs', 'extra']

class AmpelBuffer(TypedDict, total=False):
	"""
	Content bundle used to build :class:`~ampel.view.SnapView.SnapView`.
	
	This is a dict containing 1 or more of the following items:
	"""
	# Could stock be of type list[StockDocument] to enable hybrid/dual transients ?
	id: StockId
	stock: Optional[StockDocument]
	origin: Optional[Union[int, list[int]]]
	t0: Optional[list[DataPoint]]
	t1: Optional[list[T1Document]]
	t2: Optional[list[T2Document]]
	logs: Optional[list[LogDocument]]
	extra: Optional[dict[str, Any]]
