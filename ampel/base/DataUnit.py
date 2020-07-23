#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/base/DataUnit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 12.10.2019
# Last Modified Date: 15.06.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Tuple, Dict, Any, Optional, Union, TYPE_CHECKING
from ampel.base.AmpelBaseModel import AmpelBaseModel
if TYPE_CHECKING:
	from ampel.log.AmpelLogger import AmpelLogger


class DataUnit(AmpelBaseModel):

	# Named resources required by this unit.
	require: Optional[Tuple[str, ...]] = None
	version: Optional[Union[str, float]] = None

	# Some unit contributors might want to restrict units usage
	# by scoping them to their respective distribution name (str)
	# private: Optional[str] = None

	def __init__(self,
		logger: 'AmpelLogger', resource: Optional[Dict[str, Any]] = None, **kwargs
	) -> None:
		self.logger = logger
		self.resource = resource
		AmpelBaseModel.__init__(self, **kwargs)

		if hasattr(self, "post_init"):
			self.post_init() # type: ignore


	def get_version(self) -> Optional[Union[str, float]]:
		return self.version
