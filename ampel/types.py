#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/types.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                02.12.2019
# Last Modified Date:  06.11.2025
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from collections.abc import KeysView, Mapping, Sequence, ValuesView
from typing import TYPE_CHECKING, Annotated, Any, TypeVar, Union, get_origin, Final
from typing import _GenericAlias # type: ignore[attr-defined]

if TYPE_CHECKING:
	from ampel.base.AmpelBaseModel import AmpelBaseModel
	from ampel.struct.JournalAttributes import JournalAttributes
	from ampel.struct.StockAttributes import StockAttributes

do_type_check = True

T = TypeVar('T')
TRACELESS: Final[int] = -1 # Used as metadata marker in Annotated[...] for traceless fields
Traceless = Annotated[T, TRACELESS]


StockId = int | bytes | str
ChannelId = int | str
DataPointId = int
Tag = int | str
UnitId = str
JDict = dict[str, Any] # JSON dict

# ruff: noqa: UP007
T2Link = Union[StockId, DataPointId, int]
T3Send = Union['JournalAttributes', 'StockAttributes', tuple[StockId, 'StockAttributes']]

UBson = Union[None, str, int, float, bool, bytes, list[Any], Mapping[str, Any]]
TBson = TypeVar("TBson", str, int, float, bool, bytes, list[Any], Mapping[str, Any])
ubson = (str, int, float, bool, bytes, list, Mapping)

NotIterable = TypeVar("NotIterable", None, str, int, bytes, bytearray)
StrictIterable = Union[list[T], set[T], tuple[T], frozenset[T], ValuesView[T], KeysView[T]]
strict_iterable = (list, tuple, set, frozenset, ValuesView, KeysView)

OneOrMany = Union[Sequence[T], T] # please keep this order


def check_class(
	Klass: type,
	class_type: Union[type["AmpelBaseModel"], tuple[type["AmpelBaseModel"], ...], _GenericAlias]
) -> None:
	""" :raises: ValueError """
	if isinstance(class_type, _GenericAlias):
		class_type = get_origin(class_type)
	if not issubclass(Klass, class_type):
		raise ValueError(f"{Klass} is not a subclass of {class_type}")
