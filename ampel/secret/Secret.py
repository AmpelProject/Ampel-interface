#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/secret/Secret.py
# License           : BSD-3-Clause
# Author            : Jakob van Santen <jakob.van.santen@desy.de>
# Date              : 14.08.2020
# Last Modified Date: 20.06.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Generic
from ampel.types import T
from ampel.base.decorator import abstractmethod
from ampel.base.AmpelABC import AmpelABC


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
