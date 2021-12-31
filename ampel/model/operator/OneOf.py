#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/model/operator/OneOf.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 22.10.2018
# Last Modified Date: 18.03.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Generic
from ampel.types import T
from ampel.base.AmpelBaseModel import AmpelBaseModel

class OneOf(Generic[T], AmpelBaseModel):
	one_of: list[T]
