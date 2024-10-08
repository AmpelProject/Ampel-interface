#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/config/AmpelConfig.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                22.10.2019
# Last Modified Date:  04.08.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

import json
from collections.abc import Sequence
from typing import Any, Literal, TypeVar, Union, get_origin, overload

import yaml

from ampel.util.freeze import recursive_freeze
from ampel.util.mappings import try_int
from ampel.view.ReadOnlyDict import ReadOnlyDict

UJson = Union[None, str, int, float, bool, list[Any], dict[str, Any]] # noqa: UP007
JT = TypeVar('JT', None, str, int, float, bool, bytes, list[Any], dict[str, Any])


class AmpelConfig:
	"""Container for the central Ampel configuration"""

	_config: dict
	_check_types: int = 1


	@classmethod
	def load(cls, config_file_path: str, freeze: bool = True) -> 'AmpelConfig':
		with open(config_file_path) as f:
			config = yaml.safe_load(f)
		# Convert potentially stringified int keys (JSON compatibility) back to int
		for s in ('channel', 'confid'):
			for k in list(config[s]):
				config[s][try_int(k)] = config[s].pop(k)
		return cls(config, freeze)


	def __init__(self, config: dict, freeze: bool = False) -> None:
		"""
		:raises: ValueError if provided config is None or empty
		"""
		if config is None or not config:
			raise ValueError("Please provide a config")

		self._config: dict = recursive_freeze(config) if freeze else config

		if 'general' in config and 'check_types' in config['general']:
			self._check_types = config['general']['check_types']

	# Overloads for method call without 'entry'

	@overload
	def get(self) -> dict[str, Any]:
		""" config.get() """

	@overload
	def get(self, entry: None) -> dict[str, Any]:
		""" config.get(None) """

	@overload
	def get(self, entry: None, ret_type: Any) -> dict[str, Any]:
		""" config.get(None, None/dict) """

	@overload
	def get(self, entry: None, ret_type: Any, *, raise_exc: bool) -> dict[str, Any]:
		""" config.get(None, None/dict, raise_exc=True/False) """

	@overload
	def get(self, entry: None, *, raise_exc: bool) -> dict[str, Any]:
		""" config.get(None, raise_exc=True/False) """


	# Overloads for method call with 'entry' but without return type

	@overload
	def get(self, entry: str | int | Sequence[str | int]) -> UJson:
		""" config.get('logging') """

	@overload
	def get(self, entry: str | int | Sequence[str | int], ret_type: None) -> UJson:
		""" config.get('logging', None) """

	@overload
	def get(self, entry: str | int | Sequence[str | int], *, raise_exc: bool) -> UJson:
		""" config.get('logging', raise_exc=False/True) """

	@overload
	def get(self, entry: str | int | Sequence[str | int], ret_type: None, *, raise_exc: bool) -> UJson:
		""" config.get('logging', None, raise_exc=False/True) """


	# Overloads for method call with 'entry' and return type

	@overload
	def get(self, entry: str | int | Sequence[str | int], ret_type: type[JT]) -> None | JT:
		""" config.get('logging', dict) """

	@overload
	def get(self, entry: str | int | Sequence[str | int], ret_type: type[JT], *, raise_exc: Literal[False]) -> None | JT:
		""" config.get('logging', dict, raise_exc=False) """

	@overload
	def get(self, entry: str | int | Sequence[str | int], ret_type: type[JT], *, raise_exc: Literal[True]) -> JT:
		""" config.get('logging', dict, raise_exc=True) """


	def get(self,
		entry: None | str | int | Sequence[str | int] = None,
		ret_type: None | type[JT] = None,
		*, raise_exc: bool = False
	) -> UJson | None | JT:
		"""
		Optional arguments:
		
		:param ret_type: expected return type (str, int, dict, list, ...).
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
		for el in [entry] if isinstance(entry, int) else (try_int(el) for el in entry):
			if el not in ret:
				if raise_exc:
					raise ValueError(f'Config element {entry!r} not found')
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


	def get_conf_id(self, conf_id: int) -> dict[str, Any]:

		if conf_id not in self._config['confid']:
			raise ValueError(f"Config with id {conf_id} not found")

		return self._config['confid'][conf_id]


	def print(self,
		entry: None | str = None, format: Literal['json', 'yaml'] = 'yaml'
	) -> None:

		out = self.get(entry)
		print( # noqa: T201
			yaml.dump(out) if format == 'yaml'
			else json.dumps(out, indent=4)
		)


	def freeze(self) -> None:
		if not self.is_frozen():
			self._config = recursive_freeze(self._config)


	def is_frozen(self) -> bool:
		return isinstance(self._config, ReadOnlyDict)
