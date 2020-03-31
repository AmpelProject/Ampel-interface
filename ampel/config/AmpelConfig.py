#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/config/AmpelConfig.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 22.10.2019
# Last Modified Date: 03.02.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

import json
from typing import Dict, List, Union, Optional, TypeVar, Type, Literal, Any, overload
from ampel.utils.Freeze import Freeze
from ampel.view.ReadOnlyDict import ReadOnlyDict

T = TypeVar('T')


class AmpelConfig:
	"""
	Class holding the central ampel configuration
	"""


	def __init__(self, config: Dict, freeze: bool = True) -> None:
		self._config: Dict = Freeze.recursive_freeze(config) if freeze else config


	@overload
	def get(self, entry: None) -> Dict[str, Any]:
		...

	@overload
	def get(self, entry: Union[str, List[str]]
	) -> Optional[Union[str, int, float, bool, None, List, Dict]]:
		...

	@overload
	def get(self, entry: Union[str, List[str]], ret_type: None, raise_exc: Literal[False]
	) -> Optional[Union[str, int, float, bool, None, List, Dict]]:
		...

	@overload
	def get(self, entry: Union[str, List[str]], ret_type: None, raise_exc: Literal[True]
	) -> Union[str, int, float, bool, None, List, Dict]:
		...

	@overload
	def get(self, entry: Union[str, List[str]], ret_type: Type[T]) -> Optional[T]:
		...

	@overload
	def get(self, entry: Union[str, List[str]], ret_type: Type[T], raise_exc: Literal[False]) -> Optional[T]:
		...

	@overload
	def get(self, entry: Union[str, List[str]], ret_type: Type[T], raise_exc: Literal[True]) -> T:
		...

	def get(self,
		entry: Optional[Union[str, List[str]]] = None,
		ret_type: Optional[Type[T]] = None,
		raise_exc: bool = False
	) -> Union[Dict[str, Any], T, Optional[T]]:
		"""
		Optional arguments:
		:param ret_type: expected return type (str, int, Dict, List, ...).
		:param entry: sub-config element will be returned.

		Ex: get("channel.HU_RANDOM") or get(['foo', 'bar', 'baz'])
		:raise ValueError: if the retrieved value has not the expected type
		"""

		if entry is None:
			return self._config

		if isinstance(entry, str):
			entry = entry.split(".")

		# check for int elements encoded as str
		array: List[Union[int, str]] = [
			(el if not el.isdigit() else int(el)) for el in entry
		]

		ret = self._config
		for el in array:
			if el not in ret:
				if raise_exc:
					raise ValueError(f"Config element '{entry}' not found")
				return None
			ret = ret[el]

		if ret_type:
			if not isinstance(ret, ret_type):
				raise ValueError(
					f"Retrieved value has not the expected type.\n"
					f"Expected: {ret_type}\n"
					f"Found: {type(ret)}"
				)

		return ret # type: ignore[return-value]


	def print(self, entry: Optional[str] = None) -> None:
		print(
			json.dumps(
				self.get(entry), indent=4 # type: ignore[arg-type]
			)
		)


	def is_frozen(self) -> bool:
		return isinstance(self._config, ReadOnlyDict)
