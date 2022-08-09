#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/model/operator/OneOf.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                22.10.2018
# Last Modified Date:  18.03.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from typing import Generic
from ampel.types import T
from ampel.base.AmpelGenericModel import AmpelGenericModel

class OneOf(AmpelGenericModel, Generic[T]):
	one_of: list[T]
