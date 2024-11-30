#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/cli/config.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                20.08.2022
# Last Modified Date:  20.08.2022
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from os import environ, path

from platformdirs import user_data_dir


def get_user_data_config_path() -> str:
	"""
	:returns: full path to yaml ampel conf
	"""

	if env := environ.get('AMPEL_CONFIG'):
		return env

	if env := (environ.get('CONDA_PREFIX') or environ.get('VIRTUAL_ENV')):

		# ex: /Users/hu/miniconda3/envs/myCondaEnv/share/ampel/conf.yml
		return path.join(env, 'share', 'ampel', 'conf.yml')

	# ex: /Users/hu/Library/Application Support/ampel/conf/conf.yml
	return path.join(user_data_dir("ampel"), "conf", "conf.yml")
