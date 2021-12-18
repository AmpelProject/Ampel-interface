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
	Union, TypeVar, FrozenSet, Type, Sequence, get_origin,
	TYPE_CHECKING, KeysView, ValuesView, Any, Annotated, _GenericAlias
)

if TYPE_CHECKING:
	from ampel.base.AmpelBaseModel import AmpelBaseModel
	from ampel.struct.JournalAttributes import JournalAttributes
	from ampel.struct.StockAttributes import StockAttributes

TRACELESS = -1
T = TypeVar('T')
Traceless = Annotated[T, TRACELESS]

StockId = Union[int, bytes, str]
ChannelId = Union[int, str]
DataPointId = int
Tag = Union[int, str]
UnitId = str

T2Link = Union[StockId, DataPointId, int]
T3Send = Union['JournalAttributes', 'StockAttributes', tuple[StockId, 'StockAttributes']]

UBson = Union[None, str, int, float, bool, bytes, list[Any], dict[str, Any]]
TBson = TypeVar("TBson", str, int, float, bool, bytes, list, dict)
ubson = (str, int, float, bool, bytes, list, dict)
StrictIterable = Union[list[T], set[T], tuple[T], FrozenSet[T], ValuesView[T], KeysView[T]]
strict_iterable = (list, tuple, set, frozenset, values_view, keys_view)

OneOrMany = Union[Sequence[T], T] # please keep this order


def check_class(Klass: Type, class_type: Union[Type["AmpelBaseModel"], tuple[Type["AmpelBaseModel"], ...], _GenericAlias]) -> None:
	""" :raises: ValueError """
	if isinstance(class_type, _GenericAlias):
		class_type = get_origin(class_type)
	if not issubclass(Klass, class_type):
		raise ValueError(f"{Klass} is not a subclass of {class_type}")
