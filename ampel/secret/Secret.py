#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/secret/Secret.py
# License:             BSD-3-Clause
# Author:              Jakob van Santen <jakob.van.santen@desy.de>
# Date:                14.08.2020
# Last Modified Date:  08.09.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from typing import Generic, TypeVar

from ampel.base.AmpelABC import AmpelABC
from ampel.base.decorator import abstractmethod

T = TypeVar('T')

# mypy: disable-error-code = empty-body
class Secret(Generic[T], AmpelABC, abstract=True):
    """
    A wrapper for a piece of sensitive data, e.g. a password or access token.
    """

    @abstractmethod
    def get(self) -> T:
        """ Returns secret value """

    @abstractmethod
    def set(self, arg: T) -> None:
        """ Sets secret value """
