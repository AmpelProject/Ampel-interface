#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/cli/LoadAnyOfAction.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                18.03.2021
# Last Modified Date:  22.10.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from argparse import Action
from ampel.model.operator.AnyOf import AnyOf

class LoadAnyOfAction(Action):

	def __call__(self, parser, namespace, values, option_string=None):

		v = [
			int(el) if el.lstrip("-+").isdigit() else el
			for el in values
		]

		setattr(
			namespace,
			self.dest,
			v[0] if len(v) == 1 else AnyOf(any_of = v)
		)
