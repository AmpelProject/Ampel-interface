#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/model/StateT2Dependency.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 06.02.2021
# Last Modified Date: 17.02.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Optional, Dict, Any, Generic
from ampel.types import T
from ampel.model.UnitModel import UnitModel

# Note class inheritance order matters
# "TypeError: Cannot create a consistent method resolution"
# is raised if order is switched (possibly due to pydantic's metaclass)
class StateT2Dependency(UnitModel[T], Generic[T]):
	"""
	Used to specify how "tied state t2" units should select the associated required t2 document.
	"""
	#: - None: the state associated with the root tied state T2 will be used (value of 'link' in t2 doc)
	#: - Dict: allows tied state T2 units to be bound with point t2 units.
	#:   The value provided here must be understandable by
	#:      :func:`AbsTiedStateT2Unit.get_link <ampel.abstract.AbsTiedStateT2Unit.AbsTiedStateT2Unit.get_link>`
	#:   Ampel extensions such as Ampel-photometry accept more 'link_override' options than vanilla Ampel.
	link_override: Optional[Dict[str, Any]]
