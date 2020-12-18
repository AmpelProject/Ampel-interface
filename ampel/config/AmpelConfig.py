#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/config/AmpelConfig.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 22.10.2019
# Last Modified Date: 18.04.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

import yaml, json
from typing import Dict, List, Union, Optional, Type, Literal, Any, Iterable, overload, get_origin
from ampel.type import JT, JSONTypes
from ampel.util.freeze import recursive_freeze
from ampel.view.ReadOnlyDict import ReadOnlyDict


class AmpelConfig:
	"""Container for the central Ampel configuration"""

	_config: Dict
	_check_types: int = 1


	@classmethod
	def new(cls,
		config: Dict[str, Any],
		pwd_file_path: Optional[str] = None,
		pwds: Optional[Iterable[str]] = None,
		freeze: bool = True
	) -> 'AmpelConfig':

		if pwd_file_path or pwds:

			try:
				from ampel.util.crypto import aes_recursive_decrypt # type: ignore[import]
			except Exception:
				print("ampel-core is required for this feature")
				return None # type: ignore

			if pwd_file_path:
				with open(pwd_file_path, "r") as f:
					pwds = [l.strip() for l in f.readlines()]

			config['resource'] = aes_recursive_decrypt(
				config['resource'], pwds # type: ignore[arg-type]
			)

		return cls(config, freeze)


	@classmethod
	def load(cls,
		config_file_path: str,
		pwd_file_path: Optional[str] = None,
		pwds: Optional[Iterable[str]] = None,
		freeze: bool = True
	) -> 'AmpelConfig':

		with open(config_file_path, "r") as f:
			return cls.new(yaml.safe_load(f), pwd_file_path, pwds, freeze)


	def __init__(self, config: Dict, freeze: bool = False) -> None:
		"""
		:raises: ValueError if provided config is None or empty
		"""
		if config is None or not config:
			raise ValueError("Please provide a config")

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
	def get(self, entry: Union[str, List[str]]) -> JSONTypes:
		""" config.get('db') """

	@overload
	def get(self, entry: Union[str, List[str]], ret_type: None) -> JSONTypes:
		""" config.get('db', None) """

	@overload
	def get(self, entry: Union[str, List[str]], *, raise_exc: bool) -> JSONTypes:
		""" config.get('db', raise_exc=False/True) """

	@overload
	def get(self, entry: Union[str, List[str]], ret_type: None, *, raise_exc: bool) -> JSONTypes:
		""" config.get('db', None, raise_exc=False/True) """


	# Overloads for method call with 'entry' and return type

	@overload
	def get(self, entry: Union[str, List[str]], ret_type: Type[JT]) -> Optional[JT]:
		""" config.get('db', dict) """

	@overload
	def get(self, entry: Union[str, List[str]], ret_type: Type[JT], *, raise_exc: Literal[False]) -> Optional[JT]:
		""" config.get('db', dict, raise_exc=False) """

	@overload
	def get(self, entry: Union[str, List[str]], ret_type: Type[JT], *, raise_exc: Literal[True]) -> JT:
		""" config.get('db', dict, raise_exc=True) """


	def get(self, # type: ignore[misc]
		entry: Optional[Union[str, List[str]]] = None,
		ret_type: Optional[Type[JT]] = None,
		*, raise_exc: bool = False
	) -> Union[JSONTypes, Optional[JT]]:
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

			if origin := get_origin(ret_type):
				ret_type = origin

			if not isinstance(ret, ret_type): # type: ignore[arg-type]
				raise ValueError(
					f"Retrieved value has not the expected type.\n"
					f"Expected: {ret_type}\n"
					f"Found: {type(ret)}"
				)

		return ret


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
