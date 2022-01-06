#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/model/operator/AllOf.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                15.10.2018
# Last Modified Date:  18.03.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from typing import Generic
from ampel.types import T
from ampel.base.AmpelGenericModel import AmpelGenericModel


class AllOf(AmpelGenericModel, Generic[T]):
	#: Select items by logical AND
	all_of: list[T]
