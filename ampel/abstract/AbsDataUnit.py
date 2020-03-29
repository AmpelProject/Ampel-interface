#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsDataUnit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 12.10.2019
# Last Modified Date: 18.02.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from pydantic import BaseModel, root_validator
from pydantic.main import Extra
from typing import Tuple, Dict, Any, Optional, ClassVar, Union
from ampel.abc import defaultmethod
from ampel.abc.AmpelABC import AmpelABC
from ampel.logging.AmpelLogger import AmpelLogger


class AbsDataUnit(AmpelABC, BaseModel):

	class Config:
		extra = Extra.forbid
		arbitrary_types_allowed = True

	# Named resources required by this unit.
	# This can be overridden by subclasses to register dependencies on local resources
	require: ClassVar[Optional[Tuple[str, ...]]]
	version: ClassVar[Optional[Union[str, float]]]

	logger: AmpelLogger = ... # type: ignore
	resource: Dict[str, Any] = {}
	# In the future, some participcant might want to restrict units usage
	# by scoping them to their respective distribution name (str)
	private: Optional[str] = None


	@defaultmethod(check_super_call=True)
	def __init__(self, **kwargs):

		self.__config__.extra = Extra.forbid
		BaseModel.__init__(self, **kwargs)
		self.__config__.extra = Extra.allow


	def get_version(self) -> Optional[Union[str, float]]:
		return self.version


	@root_validator(pre=True)
	def _set_default_logger(cls, values):
		if not values.get('logger'):
			values['logger'] = AmpelLogger.get_logger()
		return values
