#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/abstract/AbsCLIOperation.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                16.03.2021
# Last Modified Date:  14.08.2022
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from typing import Any
from collections.abc import Sequence
from argparse import ArgumentParser
from ampel.base.AmpelABC import AmpelABC
from ampel.base.decorator import abstractmethod
from ampel.cli.AmpelArgumentParser import AmpelArgumentParser


class AbsCLIOperation(AmpelABC, abstract=True):
	"""
	Implementing subclasses shall be placed in package ampel.cli
	"""

	@staticmethod
	@abstractmethod
	def get_sub_ops() -> None | list[str]:
		...

	@abstractmethod
	def get_parser(self, sub_op: None | str = None) -> ArgumentParser | AmpelArgumentParser:
		...

	@abstractmethod
	def run(self, args: dict[str, Any], unknown_args: Sequence[str], sub_op: None | str = None) -> None:
		...
