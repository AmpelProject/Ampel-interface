#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/cli/config.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                20.08.2022
# Last Modified Date:  20.08.2022
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

import os
from appdirs import user_data_dir # type: ignore[import]

def get_user_data_config_path() -> str:

	app_path = user_data_dir("ampel")
	if not os.path.exists(app_path):
		os.makedirs(app_path)

	app_path = os.path.join(app_path, "conf")
	if not os.path.exists(app_path):
		os.makedirs(app_path)

	env = os.environ.get('CONDA_DEFAULT_ENV')
	if env:
		app_path = os.path.join(app_path, env)
		if not os.path.exists(app_path):
			os.makedirs(app_path)

	return os.path.join(app_path, "conf.yml")
