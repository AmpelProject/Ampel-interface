#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/struct/T2Dependency.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 06.02.2021
# Last Modified Date: 06.02.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import TypedDict, Optional, Dict, Any, Union


class T2Dependency(TypedDict):
	"""
	Used to specify how "tied t2" units should select the associated required t2 document.
	:param unit: None or hash value of the t2 config
	:param config: None or hash value of the t2 config
	:param link_override:
	- None: the state associated with the root tied state T2 will be used (value of 'link' in t2 doc)
	- Dict: allows tied state T2 units to be bound with point t2 units.
		The value provided here must be understandable by AbsTiedStateT2Unit.get_link(<link_override value>, ...)
		Ampel extensions such as Ampel-photometry will typically accept more 'link_override' options than vanilla Ampel.
	"""

	unit: Union[str, int]
	config: Optional[int]
	link_override: Optional[Dict[str, Any]]
