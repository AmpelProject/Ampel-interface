#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsTiedT2Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 06.02.2021
# Last Modified Date: 10.02.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import List, Optional, Sequence, Union
from ampel.base import abstractmethod, AmpelABC, DataUnit
from ampel.struct.T2Dependency import T2Dependency


class AbsTiedT2Unit(AmpelABC, DataUnit, abstract=True):
	"""
	Top level abstract class for T2 units depending on other T2 units.
	"""

	t2_dependency: Optional[Union[T2Dependency, Sequence[T2Dependency]]]

	@abstractmethod
	def get_tied_unit_names(self) -> List[str]:
		"""
		ex: return ["T2CatalogMatch"]
		"""
