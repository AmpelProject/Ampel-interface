#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/struct/DocAttributes.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 11.02.2021
# Last Modified Date: 18.04.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from enum import IntEnum
from typing import Optional, Union, List, Generic
from ampel.type import T, Tag
from ampel.enum.DocumentCode import DocumentCode


class DocAttributes(Generic[T]):
	"""
	Structure potentialy returned by Ampel units to customize:
	- 'code' of the associated ampel record (ampel.content.T[1,2,3]Record)
	- 'code' and/or 'tag' of the associated ampel document (ampel.content.T[1,2,3]Document)
	"""

	__slots__ = 'data', 'rec_code', 'doc_code', 'doc_tag'

	def __init__(self,
		data: T = None,
		rec_code: int = 0,
		doc_code: Union[DocumentCode, int] = 0,
		doc_tag: Optional[Union[Tag, List[Tag]]] = None
	) -> None:
		"""
		:param rec_code: integer code of the record (T[2,3]Record)
		:param doc_code: integer code of the document (DocumentCode or custom positive int)
		"""
		#: result of unit invocation
		self.data = data

		#: integer code of the associated Record
		self.rec_code = rec_code if isinstance(rec_code, IntEnum) else abs(rec_code)

		#: integer code of the associated Document
		self.doc_code = doc_code

		#: tag(s) to be added
		self.doc_tag = doc_tag
