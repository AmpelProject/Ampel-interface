#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/util/tag.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                25.11.2021
# Last Modified Date:  25.11.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from ampel.types import Tag
from typing import Literal, overload
from collections.abc import Sequence


@overload
def merge_tags(
	arg1: Tag | Sequence[Tag] | set[Tag],
	arg2: None | Tag | Sequence[Tag] | set[Tag]
) -> list[Tag]:
	...

@overload
def merge_tags(
	arg1: None | Tag | Sequence[Tag] | set[Tag],
	arg2: Tag | Sequence[Tag] | set[Tag]
) -> list[Tag]:
	...

@overload
def merge_tags(
	arg1: None | Tag | Sequence[Tag] | set[Tag],
	arg2: None | Tag | Sequence[Tag] | set[Tag]
) -> None | list[Tag]:
	...

@overload
def merge_tags(
	arg1: Tag | Sequence[Tag] | set[Tag],
	arg2: None | Tag | Sequence[Tag] | set[Tag], *,
	reduce: Literal[False]
) -> list[Tag]:
	...

@overload
def merge_tags(
	arg1: None | Tag | Sequence[Tag] | set[Tag],
	arg2: Tag | Sequence[Tag] | set[Tag], *,
	reduce: Literal[False]
) -> list[Tag]:
	...

@overload
def merge_tags(
	arg1: None | Tag | Sequence[Tag] | set[Tag],
	arg2: None | Tag | Sequence[Tag] | set[Tag], *,
	reduce: Literal[False]
) -> None | list[Tag]:
	...

@overload
def merge_tags(
	arg1: Tag | Sequence[Tag] | set[Tag],
	arg2: None | Tag | Sequence[Tag] | set[Tag], *,
	reduce: Literal[True]
) -> Tag | list[Tag]:
	...

@overload
def merge_tags(
	arg1: None | Tag | Sequence[Tag] | set[Tag],
	arg2: Tag | Sequence[Tag] | set[Tag], *,
	reduce: Literal[True]
) -> Tag | list[Tag]:
	...

@overload
def merge_tags(
	arg1: None | Tag | Sequence[Tag] | set[Tag],
	arg2: None | Tag | Sequence[Tag] | set[Tag], *,
	reduce: Literal[True]
) -> None | Tag | list[Tag]:
	...

def merge_tags(
	arg1: None | Tag | Sequence[Tag] | set[Tag],
	arg2: None | Tag | Sequence[Tag] | set[Tag], *,
	reduce: bool = True
) -> None | Tag | list[Tag]:
	""" A mypy friendly method that merges tags together """

	if arg2 is None:
		if arg1 is None:
			return None
		if isinstance(arg1, (int, str)):
			return arg1
		if reduce and len(arg1) == 1:
			if isinstance(arg1, set):
				return next(iter(arg1))
			return arg1[0]
		return arg1 if isinstance(arg1, list) else list(arg1)

	if arg1 is None:
		if arg2 is None:
			return None
		return merge_tags(arg2, arg1, reduce) # type: ignore # no idea, no time

	if isinstance(arg1, (str, int)):
		if isinstance(arg2, (str, int)):
			if arg2 != arg1:
				return [arg1, arg2]
			return arg1 if reduce else [arg1]
		else:
			if arg1 in arg2:
				return arg2 if isinstance(arg2, list) else list(arg2)
			l = list(arg2)
			l.append(arg1)
			return l

	# arg1 is a sequence (str excluded)
	else:
		if isinstance(arg2, (int, str)):
			if arg2 in arg1:
				return arg1 if isinstance(arg1, list) else list(arg1)
			l = list(arg1)
			l.append(arg2)
	
		# arg1 and arg2 are sequences (str excluded)
		else:
			l = list(
				(arg1 if isinstance(arg1, set) else set(arg1)) |
				(arg2 if isinstance(arg2, set) else set(arg2))
			)

		return l[0] if reduce and len(l) == 1 else l
