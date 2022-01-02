#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/struct/AmpelBuffer.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                31.05.2018
# Last Modified Date:  01.12.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from typing import Any, TypedDict, Literal
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
	stock: None | StockDocument
	origin: None | int | list[int]
	t0: None | list[DataPoint]
	t1: None | list[T1Document]
	t2: None | list[T2Document]
	logs: None | list[LogDocument]
	extra: None | dict[str, Any]
