#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/cli/config.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                20.08.2022
# Last Modified Date:  20.08.2022
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from os import path, environ, makedirs
from appdirs import user_data_dir # type: ignore[import]

def get_user_data_config_path() -> str:
	"""
	:returns: full path to yaml ampel conf
	"""

	if env := environ.get('CONDA_PREFIX'):

		app_path = path.join(env, 'share')
		if not path.exists(app_path):
			raise ValueError('Conda path does not contain a shared folder?')

		app_path = path.join(app_path, 'ampel')
		if not path.exists(app_path):
			makedirs(app_path)

		# ex: /Users/hu/miniconda3/envs/myCondaEnv/share/ampel/conf.yml
		return path.join(app_path, "conf.yml")

	app_path = user_data_dir("ampel")
	if not path.exists(app_path):
		makedirs(app_path)

	app_path = path.join(app_path, "conf")
	if not path.exists(app_path):
		makedirs(app_path)

	# ex: /Users/hu/Library/Application Support/ampel/conf.yml
	return path.join(app_path, "conf.yml")
