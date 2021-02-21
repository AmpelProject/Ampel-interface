#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/content/SVGRecord.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 13.02.2021
# Last Modified Date: 13.02.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Union, TypedDict, Sequence
from ampel.type import Tag


class SVGRecord(TypedDict, total=False):
	"""
	Dict crafted by :class:`~ampel.plot.SVGUtils.SVGUtils`
	"""
	name: str
	tag: Union[Tag, Sequence[Tag]]
	title: str
	compressed: bool
	svg: Union[bytes, str]
	svg_str: str
