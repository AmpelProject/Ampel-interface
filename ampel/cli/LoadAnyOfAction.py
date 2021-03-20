#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/cli/LoadAnyOfAction.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 18.03.2021
# Last Modified Date: 18.03.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from argparse import Action
from ampel.model.operator.AnyOf import AnyOf

class LoadAnyOfAction(Action):

	def __call__(self, parser, namespace, values, option_string=None):

		v = [
			int(el) if el.lstrip("-+").isdigit() else el
			for el in values
		]

		if len(v) == 1:
			v = [0]

		setattr(namespace, self.dest, AnyOf(any_of = v))
