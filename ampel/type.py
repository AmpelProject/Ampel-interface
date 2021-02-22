#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/type.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 02.12.2019
# Last Modified Date: 17.02.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from collections.abc import ValuesView as values_view, KeysView as keys_view
from typing import ( # type: ignore[attr-defined]
	Union, TypeVar, Set, Tuple, FrozenSet, List, Type, get_origin, TYPE_CHECKING,
	KeysView, ValuesView, Literal, Dict, Any, Optional, _GenericAlias
)
from ampel.struct.T2BroadUnitResult import T2BroadUnitResult
from ampel.struct.JournalTweak import JournalTweak

if TYPE_CHECKING:
	from ampel.base.AmpelBaseModel import AmpelBaseModel


StockId = Union[int, bytes, str]
ChannelId = Union[int, str]
Tag = Union[int, str]
DataPointId = int
T2UnitResult = Union[int, T2BroadUnitResult, Dict[str, Any], List[Dict[str, Any]]]
T3AddResult = Optional[Union[JournalTweak, Dict[StockId, JournalTweak]]]

AmpelMainCol = Literal['stock', 't0', 't1', 't2']

T = TypeVar('T')
JT = TypeVar('JT', str, int, float, bool, bytes, None, List, Dict[str, Any])

StrictIterable = Union[List[T], Set[T], Tuple[T], FrozenSet[T], ValuesView[T], KeysView[T]]
strict_iterable = (list, tuple, set, frozenset, values_view, keys_view)
JSONTypes = Union[str, int, float, bool, bytes, None, List, Dict[str, Any]]


def check_class(Klass: Type, class_type: Union[Type["AmpelBaseModel"], _GenericAlias]) -> None:
	""" :raises: ValueError """
	if isinstance(class_type, _GenericAlias):
		class_type = get_origin(class_type)
	if not issubclass(Klass, class_type):
		raise ValueError(f"{Klass} is not a subclass of {class_type}")
