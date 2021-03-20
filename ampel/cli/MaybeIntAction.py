#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/cli/MaybeIntAction.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 17.03.2021
# Last Modified Date: 18.03.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from argparse import Action

class MaybeIntAction(Action):

	def __call__(self, parser, namespace, values, option_string=None):
		v = [int(el) if el.lstrip("-+").isdigit() else el for el in values]
		setattr(namespace, self.dest, v[0] if len(v) == 1 else v)
