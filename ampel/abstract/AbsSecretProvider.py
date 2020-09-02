#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsSecretProvider.py
# License           : BSD-3-Clause
# Author            : Jakob van Santen <jakob.van.santen@desy.de>
# Date              : 14.08.2020
# Last Modified Date: 14.08.2020
# Last Modified By  : Jakob van Santen <jakob.van.santen@desy.de>

from typing import Any, Type, TypeVar
from ampel.base import abstractmethod, AmpelABC
from ampel.model.Secret import Secret

T = TypeVar('T')

class AbsSecretProvider(AmpelABC, abstract=True):
    """
    Interface to a secret store. This may be as simple as a dict loaded from a
    JSON file, or a complete key manager like Vault.
    """

    @abstractmethod
    def get(self, key: str, value_type: Type[T]) -> Secret[T]:
        """
        Fetch a secret by key. May raise an exception if the key is not known.
        """
        ...
