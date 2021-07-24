#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/abstract/AbsCLIOperation.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 16.03.2021
# Last Modified Date: 22.03.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Sequence, Dict, Any, Optional, Union
from argparse import ArgumentParser
from ampel.base.AmpelABC import AmpelABC
from ampel.base.decorator import abstractmethod
from ampel.cli.AmpelArgumentParser import AmpelArgumentParser


class AbsCLIOperation(AmpelABC, abstract=True):
	"""
	Implementing subclasses shall be placed in package ampel.cli
	"""

	@abstractmethod
	def get_parser(self, sub_op: Optional[str] = None) -> Union[ArgumentParser, AmpelArgumentParser]:
		...

	@abstractmethod
	def run(self, args: Dict[str, Any], unknown_args: Sequence[str], sub_op: Optional[str] = None) -> None:
		...
