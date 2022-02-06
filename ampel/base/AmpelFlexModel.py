#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/base/AmpelFlexModel.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                17.03.2021
# Last Modified Date:  06.02.2022
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from ampel.base.AmpelBaseModel import AmpelBaseModel


class AmpelFlexModel(AmpelBaseModel):
	"""
	Allows/Ignores extra kwargs parameters
	"""

	def __init__(self, **kwargs):
		super().__init__(**{k: kwargs[k] for k in kwargs if k in self.get_model_keys()})
