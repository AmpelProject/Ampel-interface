#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/struct/JournalTweak.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 15.10.2018
# Last Modified Date: 08.06.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Dict, Optional, Sequence, Union, Any

# Cannot import Tag from ampel.type because of cyclic import issues
Tag = Union[int, str]


class JournalTweak:
	"""
	Structure potentialy returned by Ampel units to customize
	the transient journal entry created after a process is run.
	"""

	__slots__ = "tag", "status", "extra"

	#: status code of the executed process
	status: Optional[int]
	#: journal entry tag(s)
	tag: Optional[Union[Tag, Sequence[Tag]]]
	#: if provided, will be included as-is under the journal root key 'extra'
	extra: Optional[Dict[str, Any]]

	def __init__(self,
		status: Optional[int] = None,
		tag: Optional[Union[Tag, Sequence[Tag]]] = None,
		extra: Optional[Dict[str, Any]] = None
	) -> None:
		"""
		:param status: potential integer status of the executed process
		:param tag: journal entry tag(s)
		:param extra: optional dict, which if provided, will be included 'as is' under journal root key 'extra'
		Note regarding the type of extra: as of june 2020, mypy does not support recursive / json type
		-> https://github.com/python/mypy/issues/731
		"""
		self.tag = tag
		self.extra = extra
		self.status = status
