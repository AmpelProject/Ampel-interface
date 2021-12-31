#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/util/freeze.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 10.12.2019
# Last Modified Date: 09.06.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Any
from ampel.view.ReadOnlyDict import ReadOnlyDict


def recursive_freeze(arg: Any) -> Any:
	"""
	Return an immutable shallow copy
	:param arg:
		dict: ReadOnlyDict is returned
		list: tuple is returned
		set: frozenset is returned
		otherwise: arg is returned 'as is'
	"""
	if isinstance(arg, dict):
		return ReadOnlyDict(
			{
				recursive_freeze(k): recursive_freeze(v)
				for k, v in arg.items()
			}
		)

	if isinstance(arg, list):
		return tuple(
			map(recursive_freeze, arg)
		)

	if isinstance(arg, set):
		return frozenset(arg)

	return arg


def recursive_unfreeze(arg: ReadOnlyDict) -> dict:
	"""
	Inverse of recursive_freeze
	"""
	if isinstance(arg, ReadOnlyDict):
		return dict(
			{
				recursive_unfreeze(k): recursive_unfreeze(v)
				for k, v in arg.items()
			}
		)

	if isinstance(arg, tuple):
		return list(
			map(recursive_unfreeze, arg)
		)

	if isinstance(arg, frozenset):
		return set(arg)

	return arg
