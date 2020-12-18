#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsAmpelLogger.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 27.09.2018
# Last Modified Date: 18.12.2020
# Last Modified By  : Jakob van Santen <jakob.van.santen@desy.de>

from typing import Dict, Optional, Union, Any, List

from ampel.base.AmpelABC import AmpelABC
from ampel.base.decorator import abstractmethod
from ampel.type import ChannelId, StockId

class AbsAmpelLogger(AmpelABC, abstract=True):

	@abstractmethod
	def error(self, msg: Union[str, Dict[str, Any]], *args,
		exc_info: Optional[Exception] = None,
		channel: Optional[Union[ChannelId, List[ChannelId]]] = None,
		stock: Optional[StockId] = None,
		extra: Optional[Dict[str, Any]] = None,
		**kwargs
	):
		...

	@abstractmethod
	def warn(self, msg: Union[str, Dict[str, Any]], *args,
		channel: Optional[Union[ChannelId, List[ChannelId]]] = None,
		stock: Optional[StockId] = None,
		extra: Optional[Dict[str, Any]] = None,
		**kwargs
	):
		...

	@abstractmethod
	def info(self, msg: Optional[Union[str, Dict[str, Any]]], *args,
		channel: Optional[Union[ChannelId, List[ChannelId]]] = None,
		stock: Optional[StockId] = None,
		extra: Optional[Dict[str, Any]] = None,
		**kwargs
	) -> None:
		...

	@abstractmethod
	def debug(self, msg: Optional[Union[str, Dict[str, Any]]], *args,
		channel: Optional[Union[ChannelId, List[ChannelId]]] = None,
		stock: Optional[StockId] = None,
		extra: Optional[Dict[str, Any]] = None,
		**kwargs
	):
		...

	@abstractmethod
	def log(self,
		lvl: int, msg: Optional[Union[str, Dict[str, Any]]], *args,
		exc_info: Optional[Union[bool, Exception]] = None,
		channel: Optional[Union[ChannelId, List[ChannelId]]] = None,
		stock: Optional[StockId] = None,
		extra: Optional[Dict[str, Any]] = None,
		**kwargs
	):
		...
