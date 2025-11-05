#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/abstract/AbsT0Unit.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                07.10.2019
# Last Modified Date:  01.11.2025
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from typing import Any
from ampel.base.decorator import abstractmethod
from ampel.base.LogicalUnit import LogicalUnit
from ampel.content.DataPoint import DataPoint
from ampel.types import StockId


class AbsT0Unit(LogicalUnit, abstract=True):
	"""
	Abstract base class for units that generate :class:`datapoints <ampel.content.DataPoint.DataPoint>` for Ampel

	Before new datapoints are inserted into the database, they undergo light customization — or "ampelization" —
	to support efficient and flexible querying later on. These modifications preserve most of the original content
	while adapting key fields to Ampel's internal conventions.

	For example, in the case of `ZiDataPointShaper` (Ampel-ztf repository):
		* The field `candid` is renamed to `id`
		* A new field `tag` is added
		...
	"""

	@abstractmethod
	def process(self, arg: Any, stock: None | StockId = None) -> list[DataPoint]:
		"""
		Transforms an external object into one or more Ampel-formatted DataPoint instances.

		This method defines the core logic for converting raw input,
		such as alerts, measurements, or domain-specific records,
		into standardized Ampel datapoints suitable for downstream processing and storage.
		Implementations must ensure that the returned datapoints conform to Ampel's schema and tagging conventions.

		Parameters:
			arg (Any): The external input object to be converted.
			stock (None | StockId): Optional stock identifier associated with the input, if available.

		Returns:
			list[DataPoint]: A list of Ampel-compatible datapoints derived from the input.
		"""
