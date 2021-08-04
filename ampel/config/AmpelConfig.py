#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/config/AmpelConfig.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 22.10.2019
# Last Modified Date: 04.08.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

import yaml, json
from typing import Dict, List, Union, Optional, Type, Literal, Any, TypeVar, overload, get_origin
from ampel.util.freeze import recursive_freeze
from ampel.view.ReadOnlyDict import ReadOnlyDict

UJson = Union[None, str, int, float, bool, List[Any], Dict[str, Any]]
JT = TypeVar('JT', None, str, int, float, bool, bytes, List[Any], Dict[str, Any])


class AmpelConfig:
	"""Container for the central Ampel configuration"""

	_config: Dict
	_check_types: int = 1


	@classmethod
	def load(cls, config_file_path: str, freeze: bool = True) -> 'AmpelConfig':
		with open(config_file_path, "r") as f:
			return cls(yaml.safe_load(f), freeze)


	def __init__(self, config: Dict, freeze: bool = False) -> None:
		"""
		:raises: ValueError if provided config is None or empty
		"""
		if config is None or not config:
			raise ValueError("Please provide a config")

		# Convert potentially stringified int keys (JSON compatibility) back to int
		for s in ('channel', 'confid'):
			for k in [el for el in config[s].keys() if isinstance(el, str) and el.isdigit()]:
				config[s][int(k)] = config[s].pop(k)

		self._config: Dict = recursive_freeze(config) if freeze else config

		if 'general' in config and 'check_types' in config['general']:
			self._check_types = config['general']['check_types']

	# Overloads for method call without 'entry'

	@overload
	def get(self) -> Dict[str, Any]:
		""" config.get() """

	@overload
	def get(self, entry: None) -> Dict[str, Any]:
		""" config.get(None) """

	@overload
	def get(self, entry: None, ret_type: Any) -> Dict[str, Any]:
		""" config.get(None, None/dict) """

	@overload
	def get(self, entry: None, ret_type: Any, *, raise_exc: bool) -> Dict[str, Any]:
		""" config.get(None, None/dict, raise_exc=True/False) """

	@overload
	def get(self, entry: None, *, raise_exc: bool) -> Dict[str, Any]:
		""" config.get(None, raise_exc=True/False) """


	# Overloads for method call with 'entry' but without return type

	@overload
	def get(self, entry: Union[str, List[str]]) -> UJson:
		""" config.get('logging') """

	@overload
	def get(self, entry: Union[str, List[str]], ret_type: None) -> UJson:
		""" config.get('logging', None) """

	@overload
	def get(self, entry: Union[str, List[str]], *, raise_exc: bool) -> UJson:
		""" config.get('logging', raise_exc=False/True) """

	@overload
	def get(self, entry: Union[str, List[str]], ret_type: None, *, raise_exc: bool) -> UJson:
		""" config.get('logging', None, raise_exc=False/True) """


	# Overloads for method call with 'entry' and return type

	@overload
	def get(self, entry: Union[str, List[str]], ret_type: Type[JT]) -> Optional[JT]:
		""" config.get('logging', dict) """

	@overload
	def get(self, entry: Union[str, List[str]], ret_type: Type[JT], *, raise_exc: Literal[False]) -> Optional[JT]:
		""" config.get('logging', dict, raise_exc=False) """

	@overload
	def get(self, entry: Union[str, List[str]], ret_type: Type[JT], *, raise_exc: Literal[True]) -> JT:
		""" config.get('logging', dict, raise_exc=True) """


	def get(self, # type: ignore[misc]
		entry: Optional[Union[str, List[str]]] = None,
		ret_type: Optional[Type[JT]] = None,
		*, raise_exc: bool = False
	) -> Union[UJson, Optional[JT]]:
		"""
		Optional arguments:
		
		:param ret_type: expected return type (str, int, Dict, List, ...).
		:param entry: sub-config element will be returned.
		
		Examples::
			
			get("channel.HU_RANDOM")
		
		::
			
			get(['foo', 'bar', 'baz'])
		
		:raise ValueError: if the retrieved value has not the expected type
		"""

		if entry is None:
			return self._config

		if isinstance(entry, str):
			entry = entry.split(".")

		ret = self._config # pointer

		# Integerizes int path elements encoded as str
		for el in [(el if not el.isdigit() else int(el)) for el in entry]:
			if el not in ret:
				if raise_exc:
					raise ValueError(f'Config element \'{".".join(entry)}\' not found')
				return None
			ret = ret[el]

		if ret_type:

			if origin := get_origin(ret_type):
				ret_type = origin

			if not isinstance(ret, ret_type): # type: ignore[arg-type]
				raise ValueError(
					f"Retrieved value has not the expected type.\n"
					f"Expected: {ret_type}\n"
					f"Found: {type(ret)}"
				)

		return ret


	def get_conf_id(self, conf_id: int) -> Dict[str, Any]:

		if conf_id not in self._config['confid']:
			raise ValueError(f"Config with id {conf_id} not found")

		return self._config['confid'][conf_id]


	def print(self,
		entry: Optional[str] = None, format: Literal['json', 'yaml'] = 'yaml'
	) -> None:

		out = self.get(entry)
		print(
			yaml.dump(out) if format == 'yaml'
			else json.dumps(out, indent=4)
		)


	def freeze(self) -> None:
		if not self.is_frozen():
			self._config = recursive_freeze(self._config)


	def is_frozen(self) -> bool:
		return isinstance(self._config, ReadOnlyDict)
