#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/model/StateT2Dependency.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 06.02.2021
# Last Modified Date: 28.09.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Optional, Generic
from ampel.types import T
from ampel.model.UnitModel import UnitModel
from ampel.model.DPSelection import DPSelection

# Note class inheritance order matters
# "TypeError: Cannot create a consistent method resolution"
# is raised if order is switched (possibly due to pydantic's metaclass)
class StateT2Dependency(UnitModel[T], Generic[T]):
	"""
	Used to specify how "tied state t2" units should select the associated required t2 document.

	T2Processor needs to retrieve the T2Records of units tied with this unit.
	If link_override is unspecified, t2 dependencies are resolved - for each StateT2Dependency -
	using the db match query: {unit: <unit_name>, link: <same link as root doc>}.

	This behavior is overridable/customizable via 't2_dependency->link_override' (t2 config dict).
	'link_override' allows to link a state T2 with a different value than the one registered as 'link' in the T2Record.

	For example, link_override enables to tie a state T2 with the result of a point t2
	(the returned link could be the id of the first datapoint contained in the compound)
	"""

	#: - None: the state associated with the root tied state T2 will be used (value of 'link' in t2 doc)
	#: - DPSelection: allows tied state T2 units to be bound with point t2 units.
	link_override: Optional[DPSelection]
