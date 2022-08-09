#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/cli/MaybeIntAction.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                17.03.2021
# Last Modified Date:  31.07.2022
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from argparse import Action

class MaybeIntAction(Action):

	def __call__(self, parser, namespace, values, option_string=None):
		v = [
			int(el) if el.lstrip("-+").isdigit() else el
			for el in [el.strip("'").strip('"') for el in values]
		]
		setattr(namespace, self.dest, v[0] if len(v) == 1 else v)
