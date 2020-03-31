#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/src/ampel/types.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 02.12.2019
# Last Modified Date: 14.01.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from bson.int64 import Int64
from pydantic import StrictInt, StrictStr
from collections.abc import ValuesView as values_view
from collections.abc import KeysView as keys_view
from typing import Union, TypeVar, Set, Tuple, FrozenSet, List, KeysView, ValuesView, Literal

from ampel.model.PlainUnitModel import PlainUnitModel
from ampel.model.DataUnitModel import DataUnitModel
from ampel.model.AliasedUnitModel import AliasedUnitModel
from ampel.model.AliasedDataUnitModel import AliasedDataUnitModel


StockId = Union[int, bytes, str]
ChannelId = Union[int, str]
Tag = Union[int, str]
DataPointId = int
UnitId = str
datapoint_id = (int, Int64)

AllUnitModels = Union[PlainUnitModel, AliasedUnitModel, DataUnitModel, AliasedDataUnitModel]
ProcUnitModels = Union[PlainUnitModel, AliasedUnitModel]
DataUnitModels = Union[DataUnitModel, AliasedDataUnitModel]
AmpelMainCol = Literal['stock', 't0', 't1', 't2']

T = TypeVar('T')
StrictIterable = Union[List[T], Set[T], Tuple[T], FrozenSet[T], ValuesView[T], KeysView[T]]
strict_iterable = (list, tuple, set, frozenset, values_view, keys_view)
