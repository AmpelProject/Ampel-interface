#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/base/dataclass/JournalUpdate.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 15.10.2018
# Last Modified Date: 15.10.2018
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Any, Dict, List, Union
from pydantic.dataclasses import dataclass

@dataclass
class JournalUpdate:
	tranId: Union[int, List[int]]
	content: Dict[str, Any]
	ext: bool = False
