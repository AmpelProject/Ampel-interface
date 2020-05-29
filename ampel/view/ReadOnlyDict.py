#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/view/ReadOnlyDict.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : Unspecified
# Last Modified Date: 16.04.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>


class ReadOnlyDict(dict):

	def __readonly__(self, *args, **kwargs):
		raise RuntimeError("Cannot modify ReadOnlyDict")

	__setitem__ = __readonly__
	__delitem__ = __readonly__
	pop = __readonly__ # type: ignore
	popitem = __readonly__
	clear = __readonly__
	update = __readonly__ # type: ignore
	setdefault = __readonly__

	del __readonly__
