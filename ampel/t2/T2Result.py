#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/t2/T2Result.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 29.11.2019
# Last Modified Date: 16.02.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Any, Dict, Union, Optional, List, TypedDict

class T2Result(TypedDict, total=False):
	result: Dict[str, Any]
	journal: Optional[
		Dict[
			str,
			Union[
				float, int, bytes, str,
				List[Union[float, int, bytes, str]]
			]
		]
	]
