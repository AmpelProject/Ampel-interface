#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-core/ampel/log/handlers/LoggingHandlerProtocol.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 09.05.2020
# Last Modified Date: 11.06.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class LoggingHandlerProtocol(Protocol):

	level: int

	def handle(self, record: Any) -> None:
		...

	def flush(self) -> None:
		...

class AggregatingLoggingHandlerProtocol(LoggingHandlerProtocol):

	aggregate_interval: float

	def break_aggregation(self) -> None:
		...