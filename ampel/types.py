#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/types.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 02.12.2019
# Last Modified Date: 05.09.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from collections.abc import ValuesView as values_view, KeysView as keys_view
from typing import ( # type: ignore[attr-defined]
	Union, TypeVar, Set, Tuple, FrozenSet, List, Type, get_origin,
	TYPE_CHECKING, KeysView, ValuesView, Dict, Any, _GenericAlias
)

if TYPE_CHECKING:
	from ampel.base.AmpelBaseModel import AmpelBaseModel
	from ampel.struct.JournalAttributes import JournalAttributes
	from ampel.struct.StockAttributes import StockAttributes

T = TypeVar('T')
StockId = Union[int, bytes, str]
ChannelId = Union[int, str]
DataPointId = int
Tag = Union[int, str]
UnitId = str
T2Link = Union[StockId, DataPointId, int]
T3Send = Union['JournalAttributes', 'StockAttributes', tuple[StockId, 'StockAttributes']]

UBson = Union[None, str, int, float, bool, bytes, List[Any], Dict[str, Any]]
ubson = (str, int, float, bool, bytes, list, dict)
StrictIterable = Union[List[T], Set[T], Tuple[T], FrozenSet[T], ValuesView[T], KeysView[T]]
strict_iterable = (list, tuple, set, frozenset, values_view, keys_view)


def check_class(Klass: Type, class_type: Union[Type["AmpelBaseModel"], Tuple[Type["AmpelBaseModel"], ...], _GenericAlias]) -> None:
	""" :raises: ValueError """
	if isinstance(class_type, _GenericAlias):
		class_type = get_origin(class_type)
	if not issubclass(Klass, class_type):
		raise ValueError(f"{Klass} is not a subclass of {class_type}")
