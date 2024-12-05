#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/types.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                02.12.2019
# Last Modified Date:  31.12.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from collections.abc import KeysView, Mapping, Sequence, ValuesView
from typing import (  # type: ignore[attr-defined]
	TYPE_CHECKING,
	Annotated,
	Any,
	TypeVar,
	Union,
	_GenericAlias,
	get_origin,
)

if TYPE_CHECKING:
	from ampel.base.AmpelBaseModel import AmpelBaseModel
	from ampel.struct.JournalAttributes import JournalAttributes
	from ampel.struct.StockAttributes import StockAttributes

do_type_check = True

TRACELESS = -1
T = TypeVar('T')
Traceless = Annotated[T, TRACELESS]

# ruff: noqa: UP007
StockId = Union[int, bytes, str]
ChannelId = Union[int, str]
DataPointId = int
Tag = Union[int, str]
UnitId = str
JDict = dict[str, Any] # JSON dict

T2Link = Union[StockId, DataPointId, int]
T3Send = Union['JournalAttributes', 'StockAttributes', tuple[StockId, 'StockAttributes']]

UBson = Union[None, str, int, float, bool, bytes, list[Any], Mapping[str, Any]]
TBson = TypeVar("TBson", str, int, float, bool, bytes, list[Any], Mapping[str, Any])
ubson = (str, int, float, bool, bytes, list, Mapping)
StrictIterable = Union[list[T], set[T], tuple[T], frozenset[T], ValuesView[T], KeysView[T]]
strict_iterable = (list, tuple, set, frozenset, ValuesView, KeysView)

OneOrMany = Union[Sequence[T], T] # please keep this order


def check_class(Klass: type, class_type: Union[type["AmpelBaseModel"], tuple[type["AmpelBaseModel"], ...], _GenericAlias]) -> None:
	""" :raises: ValueError """
	if isinstance(class_type, _GenericAlias):
		class_type = get_origin(class_type)
	if not issubclass(Klass, class_type):
		raise ValueError(f"{Klass} is not a subclass of {class_type}")
