#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/view/ReadOnlyDict.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                Unspecified
# Last Modified Date:  16.04.2020
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>


class ReadOnlyDict(dict):
	"""A dict whose items can't be changed."""

	def __readonly__(self, *args, **kwargs):
		""":raises RuntimeError: whenever called"""
		raise RuntimeError("Cannot modify ReadOnlyDict")

	__setitem__ = __readonly__
	__delitem__ = __readonly__
	pop = __readonly__ # type: ignore
	popitem = __readonly__
	clear = __readonly__
	update = __readonly__ # type: ignore
	setdefault = __readonly__

	del __readonly__

	def __reduce__(self):
		return type(self), (dict(self),)
