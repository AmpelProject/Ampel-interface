#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/base/AmpelFlexModel.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 17.03.2021
# Last Modified Date: 17.03.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from ampel.base.AmpelBaseModel import AmpelBaseModel


class AmpelFlexModel(AmpelBaseModel):
	"""
	Allows/Ignores extra kwargs parameters
	"""

	def __init__(self, **kwargs):
		super().__init__(**{k: kwargs[k] for k in kwargs if k in self._annots})
