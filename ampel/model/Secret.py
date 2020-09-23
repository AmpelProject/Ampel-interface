#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/model/Secret.py
# License           : BSD-3-Clause
# Author            : Jakob van Santen <jakob.van.santen@desy.de>
# Date              : 14.08.2020
# Last Modified Date: 14.08.2020
# Last Modified By  : Jakob van Santen <jakob.van.santen@desy.de>

from typing import Any, Generic, TypeVar, Union

from ampel.base import abstractmethod, AmpelABC
from ampel.model.StrictModel import StrictModel

T = TypeVar('T')

class Secret(Generic[T], AmpelABC, StrictModel, abstract=True):
    """
    A wrapper for a piece of sensitive data, e.g. a password or access token.
    """

    key: str #: The name of the secret.

    @abstractmethod
    def get(self) -> T:
        """
        Resolve the secret and return its value.
        """
        ...
