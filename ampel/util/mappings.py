#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/util/mappings.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                07.06.2018
# Last Modified Date:  30.12.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from collections.abc import Iterable, Mapping, MutableMapping, Sequence
from contextlib import suppress
from typing import Any, overload

from ampel.base.AmpelBaseModel import AmpelBaseModel
from ampel.types import T, UBson, strict_iterable


def try_int(key: str | int) -> str | int:
	try:
		return int(key)
	except (ValueError, TypeError):
		return key


def get_by_path(
	mapping: Mapping, path: str | int | Sequence[str | int], delimiter: str = '.'
) -> None | UBson:
	"""
	Get an item from a nested mapping by path, e.g.
	'foo.bar.baz' -> mapping['foo']['bar']['baz']

	:param path: example: 'foo.bar.baz' or ['foo', 'bar', 'baz']
	:param delimiter: example: '.'
	"""

	if isinstance(path, str):
		parsed_path: Sequence[int | str] = [try_int(el) for el in path.split(delimiter)]
	elif isinstance(path, int):
		parsed_path = [path]
	else:
		parsed_path = path

	for el in parsed_path:
		try:
			mapping = mapping[el]
		except (TypeError, IndexError, KeyError): # noqa: PERF203
			return None

	return mapping


def get_by_json_path(d: Mapping, path: str | Sequence[str], delimiter: str = '.') -> None | tuple[str, UBson]:
	"""
	Lacks robustness, unflexible, fast.
	Supports only Bracket notation with number (https://cburgmer.github.io/json-path-comparison/)

	In []: d
	Out[]: {'id': 1, 'body': [{'data': [{'a': 1}]}]}

	In []: s
	Out[]: 'body[-1].data[0]'

	In []: %timeit get_by_json_path(d, s)
	1.43 µs ± 5.42 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)

	In []: from jsonpath_ng import jsonpath, parse
	In []: jsonpath_expression = parse('$.body[-1].data[0]')
	In []: %timeit jsonpath_expression.find(d)[0].value
	Out[]: 11.2 µs ± 222 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
	In []: %timeit parse('$.body[-1].data[0]').find(d)[0].value
	Out[]: 5.87 ms ± 66.8 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
	"""

	if isinstance(path, str):
		path = path.split(delimiter)

	try:
		for el in path:
			if el[-1] == ']':
				splits = el.split("[")
				el = splits[0] # noqa: PLW2901
				idx = int(splits[1][:-1])
				d = d[el][idx]
				continue
			if el == "*" and path[-1] == "*":
				return "*", d
			if el not in d:
				return None
			d = d[el]
	except Exception:
		return None

	return el, d


def set_by_path(
	d: MutableMapping, path: str | Sequence[str], val: Any,
	delimiter: str = '.', create: bool = True
) -> bool:
	"""
	:param create: whether to create directory sub-structures if they do not exits
	(in this case, this method will alawys return False)
	:returns: False if the key was successfully set, True otherwise
	"""
	if isinstance(path, str):
		path = path.split(delimiter)
	l = len(path) - 1
	for i, k in enumerate(path):
		if k not in d:
			if not create:
				return True
			d[k] = {}
		if i == l:
			d[k] = val
			return False
		d = d[k]
	return True


def del_by_path(d: MutableMapping, path: str | Sequence[str], delimiter: str = '.') -> bool:
	""" :returns: False if the key was successfully deleted, True otherwise """

	if isinstance(path, str):
		path = path.split(delimiter)
	l = len(path) - 1
	for i, k in enumerate(path):
		if k not in d:
			return True
		if i == l:
			del d[k]
			return False
		d = d[k]
	return True


def flatten_dict(
	d: Mapping,
	separator: str = '.',
	sort_keys: bool = False,
	flatten_list_members: bool = False,
	flatten_lists: bool = False,
	sort_lists: bool = False
) -> MutableMapping:
	"""
	This function is useful, among other things, for building "hash ids" of serializable dicts

	:param separator: character to be used to concatenate dict keys of different levels: {'a': {'b': 1}} -> {'a.b': 1}
	:param sort_keys: whether to sort dict keys. This applies to all dicts regardless of their depth/nesting
	:param flatten_list_members: whether to flatten dict structures embedded in list/sequences
	:param flatten_lists: whether to flatten lists, effectively converting ['a', 'b'] into {'0': 'a', '2': 'b'}
	:param sort_lists: whether to sort lists when possible, effectively converting ['r', 'a', 4, 1] into [1, 4, 'a', 'r']

	Example:
	Simplest case:
	In []: flatten_dict({'count': {'chans': {'HU_SN': 10}}})
	Out[]: {'count.chans.HU_SN': 10}

	In []: flatten_dict({'d': {'e':1}, 'a': [{'c':2}, {'b':{'f':[3, 1, 2]}}]}, sort_keys=True)
	Out[]: {'a': [{'c': 2}, {'b': {'f': [3, 1, 2]}}], 'd.e': 1}

	In []: flatten_dict({'d': {'e':1}, 'a': [{'c':2}, {'b':{'f':[3, 1, 2]}}]}, sort_keys=True, flatten_list_members=True)
	Out[]: {'a': [{'c': 2}, {'b.f': [3, 1, 2]}], 'd.e': 1}

	In []: flatten_dict({'d': {'e':1}, 'a': [{'c':2}, {'b':{'f':[3, 1, 2]}}]}, sort_keys=True, flatten_list_members=True, sort_lists=True)
	Out[]: {'a': [{'b.f': [1, 2, 3]}, {'c': 2}], 'd.e': 1}

	In []: flatten_dict({'d': {'e':1}, 'a': [{'b':{'f': [1, 2, 3]}}, {'c':2}]}, sort_keys=True, flatten_list_members=True, sort_lists=True)
	Out[]: {'a': [{'b.f': [1, 2, 3]}, {'c': 2}], 'd.e': 1}

	In []: flatten_dict({'d': {'e':1}, 'a': [{'b':{'f': [1, 2, 3]}}, {'c':2}]}, sort_keys=True, flatten_list_members=True, sort_lists=True, flatten_lists=True)
	Out[]: {'a.0.b.f.0': 1, 'a.0.b.f.1': 2, 'a.0.b.f.2': 3, 'a.1.c': 2, 'd.e': 1}

	In []: flatten_dict({'d': {'e':1}, 'a': [{'c':2}, {'b':{'f':[3, 1, 2]}}]}, sort_keys=True, flatten_list_members=True, sort_lists=True, flatten_lists=True)
	Out[]: {'a.0.b.f.0': 1, 'a.0.b.f.1': 2, 'a.0.b.f.2': 3, 'a.1.c': 2, 'd.e': 1}
	"""

	try:
		out = {}
		for k in sorted(d.keys()) if sort_keys else d:

			v = d[k]

			if isinstance(v, dict):
				for kk, vv in flatten_dict(
					v, separator, sort_keys, flatten_list_members, flatten_lists, sort_lists
				).items():
					out[f'{k}{separator}{kk}'] = vv

			elif isinstance(v, strict_iterable):

				if flatten_list_members:
					v = [
						flatten_dict(el, separator, sort_keys, flatten_list_members, flatten_lists, sort_lists)
						if isinstance(el, dict) else el
						for el in v
					]

				if sort_lists:

					# allow int/str mixed up
					with suppress(Exception):
						v = sorted(v, key=lambda x: str(x))

					# In []: sorted([{'c': 2}, {'b.f.0': 1, 'b.f.1': 2, 'b.f.2': 3}], key=lambda x: next(iter(x.keys())))
					# Out[]: [{'b.f.0': 1, 'b.f.1': 2, 'b.f.2': 3}, {'c': 2}]
					if flatten_list_members and all(isinstance(el, dict) for el in v):
						v = sorted(v, key=lambda x: next(iter(x.keys())))

				if flatten_lists:
					for kk, vv in flatten_dict(
						{i: v[i] for i in range(len(v))},
						separator, sort_keys, flatten_list_members, flatten_lists, sort_lists
					).items():
						out[f'{k}{separator}{kk}'] = vv

				else:
					out[k] = v
			else:
				out[k] = v

		return out

	except Exception as e:
		raise ValueError(f"Offending input: {d}") from e


def unflatten_dict(
	d: Mapping[str, Any],
	separator: str = '.',
	unflatten_list: bool = False,
	sort: bool = False
) -> MutableMapping[str, Any]:
	"""
	Example:

	In []: unflatten_dict({'count.chans.HU_SN': 10})
	Out[]: {'count': {'chans': {'HU_SN': 10}}}

	In []: unflatten_dict({'a.0.b.f.0': 1, 'a.0.b.f.1': 2, 'a.0.b.f.2': 3, 'a.1.c': 2, 'd.e': 1}, unflatten_list=True)
	Out[]: {'a': [{'b': {'f': [1, 2, 3]}}, {'c': 2}], 'd': {'e': 1}}
	"""
	out: dict[str, Any] = {}

	for key in sorted(d.keys()) if sort else d:

		parts = key.split(separator)
		target: dict[str, Any] = out

		for part in parts[:-1]:
			if part not in target:
				target[part] = {}
			target = target[part]

		target[parts[-1]] = d[key]

	if unflatten_list:
		return _unflatten_lists(out)

	return out


def _unflatten_lists(d: dict) -> dict:
	"""
	Note: modifies dict

	In []: _unflatten_lists({'a': {'0': {'b': {'f': {'0': 1, '1': 2, '2': 3}}}, '1': {'c': 2}}, 'd': {'e': 1}})
	Out[]: {'a': [{'b': {'f': [1, 2, 3]}}, {'c': 2}], 'd': {'e': 1}}
	"""

	for k, v in d.items():
		try:
			# Following line's purpose is just to trigger an error when needed:
			# it only works if v is a dict whose keys are integer (all of them)
			[int(kk) for kk in v]
			d[k] = [
				_unflatten_lists(d[k][kk]) if isinstance(d[k][kk], dict) else d[k][kk]
				for kk in v
			]
		except Exception: # noqa: PERF203
			if isinstance(v, dict):
				d[k] = _unflatten_lists(v)

	return d


def merge_dict(d1: dict, d2: dict) -> dict:
	k1 = set(d1.keys())
	k2 = set(d2.keys())
	return {k: d1[k] for k in k1.difference(k2)} | {k: d2[k] for k in k2.difference(k1)} | {
		k: merge_dict(d1[k], d2[k]) if isinstance(d1[k], dict) else d2[k]
		for k in k1.intersection(k2)
	}

@overload
def dictify(item: AmpelBaseModel) -> dict[str, UBson]:
	...

@overload
def dictify(item: list[Any]) -> list[UBson]:
	...

@overload
def dictify(item: dict[str, Any]) -> dict[str, UBson]:
	...

def dictify(item: AmpelBaseModel | list[Any] | dict[str, Any] | UBson) -> list[UBson] | dict[str, UBson] | UBson:
	"""
	Recursively dictifies input
	"""
	if isinstance(item, AmpelBaseModel):
		return item.dict()

	if isinstance(item, dict):
		# cast potential dict subclasses into plain old dicts
		return {k: dictify(v) for k, v in item.items()}

	if isinstance(item, list):
		return [dictify(v) for v in item]

	return item


def merge_dicts(items: Sequence[None | dict[T, Any]]) -> None | dict[T, Any]:
	"""
	Merge a sequence of dicts recursively. Elements that are None are skipped.
	"""
	left = None
	for right in items:
		if left and right:
			left = merge_dict(left, right)
		elif right or left is None:
			left = right
	return left


def compare_dict_values(d1: dict, d2: dict, keys: Iterable[str]) -> bool:
	"""
	:returns: true if the values of dict one and two are equal for all keys requested
	Note: dict keys absent in both dicts mean that both dicts are equals wrt the dict key.

	In []: compare_dict_values({'a': 1}, {'b': 1}, ['a'])
	Out[56]: False

	In []: compare_dict_values({'a': 1}, {'a': 2}, ['a'])
	Out[]: False

	In []: compare_dict_values({'a': 1}, {'a': 1}, ['a'])
	Out[]: True

	In []: compare_dict_values({'a': 1}, {'a': 1}, ['a', 'b'])
	Out[]: True
	"""

	for f in keys:
		if f in d1:
			if f in d2:
				if d1[f] != d2[f]:
					return False
			else:
				return False
		elif f in d2:
				return False
	return True


def get_nested_attr(obj, path):
	"""
	Get a nested attribute from object:

	:param Object obj:
	:param str path: example: 'foo.bar.baz'
	:rtype: object or None

	.. sourcecode:: python\n
		In []: time_constraint_config.before.value
		Out[]: 1531306299

		In []: AmpelUtils.get_nested_attr(time_constraint_config, "before.value")
		Out[]: 1531306299
	"""
	try:
		for name in path.split("."):
			obj = getattr(obj, name)
		return obj
	except AttributeError:
		return None
