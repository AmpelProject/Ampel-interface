#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/view/BaseView.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 19.02.2020
# Last Modified Date: 19.02.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class BaseView:

	def __init_subclass__(cls, *args, **kwargs):
		for field, value in cls.__annotations__.items():
			cls.__annotations__[field] = Union[value, None]
			if not hasattr(cls, field):
				setattr(cls, field, None)
