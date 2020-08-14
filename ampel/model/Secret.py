#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/model/Secret.py
# License           : BSD-3-Clause
# Author            : Jakob van Santen <jakob.van.santen@desy.de>
# Date              : 14.08.2020
# Last Modified Date: 14.08.2020
# Last Modified By  : Jakob van Santen <jakob.van.santen@desy.de>

from typing import Any

from ampel.base import abstractmethod, AmpelABC
from ampel.model.StrictModel import StrictModel


class Secret(AmpelABC, StrictModel, abstract=True):
    """
    A wrapper for a piece of sensitive data, e.g. a password or access token.
    """

    key: str

    @abstractmethod
    def get(self) -> Any:
        """
        Resolve the secret and return its value.
        """
        ...

    def __str__(self) -> str:
        return str(self.get())
