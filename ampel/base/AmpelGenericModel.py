#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/base/AmpelGenericModel.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                30.09.2018
# Last Modified Date:  05.01.2022
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from ampel.base.AmpelBaseModel import AmpelBaseModel


# pydantic v2 BaseModel supports generics natively
# NB: need to make this a subclass rather than an alias to keep pydantic.mypy happy
class AmpelGenericModel(AmpelBaseModel):
    ...
