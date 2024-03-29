#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/cli/LoadJSONAction.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                18.03.2021
# Last Modified Date:  18.03.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

import json
from argparse import Action


class LoadJSONAction(Action):
	def __call__(self, parser, namespace, value, option_string=None):
		setattr(namespace, self.dest, json.loads(value))
