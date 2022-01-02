#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/model/operator/AnyOf.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                15.10.2018
# Last Modified Date:  18.03.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

import collections
from typing import Generic
from ampel.types import T
from ampel.model.operator.AllOf import AllOf
from ampel.base.AmpelBaseModel import AmpelBaseModel


class AnyOf(Generic[T], AmpelBaseModel):

	#: Select items by logical OR
	any_of: list[T | AllOf[T]]

	def __init__(self, **kwargs) -> None:
		if 'any_of' in kwargs and not isinstance(kwargs['any_of'], collections.abc.Sequence):
			kwargs['any_of'] = [kwargs['any_of']]
		super().__init__(**kwargs)
