#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/setup.py
# License           : BSD-3-Clause
# Author            : jvs
# Date              : Unspecified
# Last Modified Date: 30.01.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from setuptools import setup, find_namespace_packages

setup(
	name='ampel-interface',
	version='0.7',
	packages=find_namespace_packages(),
	package_data = {
		'': ['py.typed'],
		'conf': ['*.conf', '**/*.conf', '**/**/*.conf']
	},
	install_requires = ['pydantic==1.4']
)
