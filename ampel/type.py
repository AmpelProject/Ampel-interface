#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/types.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 02.12.2019
# Last Modified Date: 11.04.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from bson.int64 import Int64
from collections.abc import ValuesView as values_view, KeysView as keys_view
from typing import Union, TypeVar, Set, Tuple, FrozenSet, List, KeysView, ValuesView, Literal, Dict, Any

StockId = Union[int, bytes, str]
ChannelId = Union[int, str]
Tag = Union[int, str]
DataPointId = int
datapoint_id = (int, Int64)

T = TypeVar('T')
StrictIterable = Union[List[T], Set[T], Tuple[T], FrozenSet[T], ValuesView[T], KeysView[T]]
strict_iterable = (list, tuple, set, frozenset, values_view, keys_view)

AmpelMainCol = Literal['stock', 't0', 't1', 't2']
JT = TypeVar('JT', str, int, float, bool, bytes, None, List, Dict[str, Any])
JSONTypes = Union[str, int, float, bool, bytes, None, List, Dict[str, Any]]
