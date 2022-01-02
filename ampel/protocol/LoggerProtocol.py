#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/protocol/LoggerProtocol.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                27.09.2018
# Last Modified Date:  18.12.2020
# Last Modified By:    Jakob van Santen <jakob.van.santen@desy.de>

from typing import Optional, Union, Any, Protocol, runtime_checkable, TYPE_CHECKING

if TYPE_CHECKING:
	from ampel.protocol.LoggingHandlerProtocol import LoggingHandlerProtocol

@runtime_checkable
class LoggerProtocol(Protocol):

	def error(self, msg: Union[str, dict[str, Any]], *args,
		exc_info: Optional[Exception] = None,
		extra: Optional[dict[str, Any]] = None,
	) -> None:
		...

	def warn(self, msg: Union[str, dict[str, Any]], *args,
		extra: Optional[dict[str, Any]] = None,
	) -> None:
		...

	def info(self, msg: Optional[Union[str, dict[str, Any]]], *args,
		extra: Optional[dict[str, Any]] = None,
	) -> None:
		...

	def debug(self, msg: Optional[Union[str, dict[str, Any]]], *args,
		extra: Optional[dict[str, Any]] = None,
	):
		...

	def log(self,
		lvl: int, msg: Optional[Union[str, dict[str, Any]]], *args,
		exc_info: Optional[Union[bool, Exception]] = None,
		extra: Optional[dict[str, Any]] = None,
	):
		...

	def addHandler(self, handler: "LoggingHandlerProtocol"):
		...

	def removeHandler(self, handler: "LoggingHandlerProtocol"):
		...
