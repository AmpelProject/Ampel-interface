#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/config/AmpelConfig.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                22.10.2019
# Last Modified Date:  12.11.2025
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

import os
import json
import importlib.metadata
from dataclasses import dataclass
from packaging.version import Version
from collections.abc import Sequence
from typing import Any, Literal, TypeVar, Union, get_origin, overload
from typing_extensions import Self, TypedDict

import yaml

from ampel.util.freeze import recursive_freeze
from ampel.util.mappings import try_int
from ampel.view.ReadOnlyDict import ReadOnlyDict
from ampel.config.OutdatedConfigError import OutdatedConfigError
from ampel.config.InvalidConfigError import InvalidConfigError

UJson = Union[None, str, int, float, bool, list[Any], dict[str, Any]] # noqa: UP007
JT = TypeVar('JT', None, str, int, float, bool, bytes, list[Any], dict[str, Any])


class VersionMismatch(TypedDict):
	package: str
	installed_version: str
	config_version: str

@dataclass
class ConfigLoadOptions:
	check_installed_versions: bool = True
	require_build_section: bool = False
	reconcile_deps_versions: bool = True

class AmpelConfig:
	"""Container for the central Ampel configuration"""

	_config: dict
	_check_types: int = 1


	@classmethod
	def load(cls,
		config_file_path: str,
		freeze: bool = True,
		options: ConfigLoadOptions | None = None
	) -> Self:
		"""
		Load an Ampel configuration from a YAML file.

		The configuration is parsed, normalized, and optionally checked against
		the versions of installed Ampel packages and external dependencies.
		Behavior is controlled by the provided :class:`ConfigLoadOptions`:

		* ``check_installed_versions``: If True, compare the versions recorded in
		the ``build`` section against installed Ampel packages. If a mismatch is
		found, an error report is printed and :class:`OutdatedConfigError` is raised.
		* ``require_build_section``: If True, raise :class:`InvalidConfigError` when
		the configuration has no ``build`` section. If False, absence of the section
		is tolerated.
		* ``reconcile_deps_versions``: If True, update the ``environment`` section
		with current versions of external dependencies (e.g. numpy, astropy).
		If False, leave recorded versions unchanged.

		:param config_file_path: Path to the YAML configuration file.
		:param freeze: If True, freeze the configuration to prevent further mutation.
		:param options: Options controlling version checks and dependency reconciliation.

		:returns: An AmpelConfig instance initialized with the loaded configuration.

		:raises OutdatedConfigError: If ``check_installed_versions`` is True and the
		configuration records outdated Ampel package versions.
		:raises InvalidConfigError: If ``require_build_section`` is True and the
		configuration does not contain a ``build`` section.
		"""

		with open(config_file_path) as f:
			config = yaml.safe_load(f)

		# Convert potentially stringified int keys (JSON compatibility) back to int
		for s in ('channel', 'confid'):
			for k in list(config[s]):
				config[s][try_int(k)] = config[s].pop(k)

		# Spawn the AmpelConfig instance
		cfg = cls(config, freeze)

		if options is None:
			options = ConfigLoadOptions()

		if (
			options.check_installed_versions and
			(mismatch := cfg.detect_ampel_mismatch(options.require_build_section))
		):
			cfg.report_mismatch(mismatch, config_file_path)
			raise OutdatedConfigError()

		if options.reconcile_deps_versions:
			cfg.reconcile_deps_versions(require_env_section=False)

		return cfg


	def __init__(self, config: dict, freeze: bool = False) -> None:
		"""
		Initialize an AmpelConfig instance.

		The provided configuration is optionally frozen to prevent mutation.
		External dependencies are potentially reconciled against the current environment.

		:param config: configuration dictionary.
		:param freeze: If True, freeze the configuration.

		:raises ValueError: If the provided config is None or empty.
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

			if not isinstance(ret, ret_type):
				raise ValueError(
					f"Retrieved value has not the expected type.\n"
					f"Expected: {ret_type}\n"
					f"Found: {type(ret)}"
				)

		return ret


	def get_conf_by_id(self, conf_id: int) -> dict[str, Any]:
		"""
		Retrieve a configuration entry by its integer hash identifier.

		The ``confid`` section of the ampel configuration stores entries keyed by
		integer hashes (xxhash64). This method looks up the entry associated
		with the provided hash.

		:param conf_id: xxhash64 integer identifier of the configuration entry.
		:returns: The configuration entry associated with the given identifier.
		:raises ValueError: If no entry exists for the given identifier.
		"""
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


	def reconcile_deps_versions(self, require_env_section: bool = False) -> bool:
		"""
		Reconcile external dependency versions recorded in the config with installed versions.

		Iterates over the ``environment`` section of the configuration and updates
		package versions if they differ from the currently installed ones. Returns
		True if any updates were made, False otherwise.

		:param require_env_section: If True, raise :class:`InvalidConfigError` when
		the ``environment`` section is missing.
		:returns: True if any dependency versions were updated, False otherwise.
		:raises InvalidConfigError: If ``require_env_section`` is True and the
		configuration has no environment section.
		"""


		env = ('conda_' + os.environ["CONDA_DEFAULT_ENV"]) \
			if 'CONDA_DEFAULT_ENV' in os.environ else 'default'

		if "environment" not in self._config or env not in self._config["environment"]:
			if require_env_section:
				raise InvalidConfigError()
			return False

		env_info = self._config["environment"][env]
		ret = False

		for pkg_name, cfg_version_str in env_info.items():

			cfg_version = Version(cfg_version_str)

			try:
				installed_version = Version(importlib.metadata.version(pkg_name))
			except Exception:
				continue  # skip if package is no longer installed

			if cfg_version != installed_version:
				print( # noqa T201
					f"Version mismatch for {pkg_name}: "
					f"config={cfg_version}, installed={installed_version}."
				)
				dict.__setitem__(self._config, pkg_name, installed_version)
				ret = True

		if ret:
			print( # noqa T201
				"Environment version mismatch detected\n"
				"Configuration was updated dynamically\n"
				"Please rebuild your Ampel config to suppress this message"
			)

		return ret


	def detect_ampel_mismatch(self, require_build_section: bool = False) -> VersionMismatch | None:
		"""
		Detect mismatches between recorded Ampel component versions and installed versions.

		Compares the versions in the ``build`` section of the configuration against
		the currently installed Ampel packages. Returns details about the first
		mismatch found, or None if all versions match.

		:param require_build_section: If True, raise :class:`InvalidConfigError` when
		the ``build`` section is missing.
		:returns: A mapping with package name, installed version, and config version
		for the first mismatch found, or None if no mismatch exists.
		:raises InvalidConfigError: If ``require_build_section`` is True and the
		configuration has no ``build`` section.
		"""

		if "build" not in self._config:
			if require_build_section:
				raise InvalidConfigError()
			return None

		build_info = self._config["build"]

		for pkg_name, cfg_version_str in build_info.items():

			if "ampel" not in pkg_name:
				continue

			cfg_version = Version(cfg_version_str)

			try:
				installed_version = Version(importlib.metadata.version(pkg_name))
			except Exception:
				# skip if package is no longer installed
				continue

			if cfg_version < installed_version:
				return VersionMismatch(
					package = pkg_name,
					installed_version = str(installed_version),
					config_version = str(cfg_version)
				)

		return None


	def report_mismatch(self, mismatch: VersionMismatch, config_file_path: str | None = None) -> None:
		"""
		Print a formatted report of a version mismatch.

		Displays details about the mismatch between recorded and installed versions,
		and provides instructions for rebuilding the configuration.

		:param mismatch: Mismatch details to report.
		:param config_file_path: Optional path to the configuration file.
		"""

		from rich.console import Console  # noqa: PLC0415

		console = Console(force_terminal=True, color_system="truecolor")
		console.print(
			f"\n Package [green bold]{mismatch['package']}[/] "
			f"has changed since the last configuration build"
		)

		console.print(f"   Version in config: [salmon1 bold]{mismatch['config_version']}[/]")
		console.print(f" Currently installed: [red bold]{mismatch['installed_version']}[/]\n")
		console.print(" [red bold]Your Ampel configuration is out of date and must be rebuilt[/]")

		if config_file_path:
			console.print(f" Location: [pink]{config_file_path}[/]\n")

		console.print(
			" • For a default installation, please run: " +
			"[blue bold]ampel config build -install[/]"
		)

		console.print(
			" • For advanced options, please see: " +
			"[steel_blue bold]ampel config build help[/]\n"
		)
