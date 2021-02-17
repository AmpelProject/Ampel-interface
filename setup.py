#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/setup.py
# License           : BSD-3-Clause
# Author            : jvs
# Date              : Unspecified
# Last Modified Date: 30.01.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from setuptools import setup, find_namespace_packages

import version_query

setup(
	name='ampel-interface',
	version=version_query.predict_version_str(),
	packages=find_namespace_packages(),
	package_data = {
		'': ['py.typed'],
		'conf': ['*.conf', '**/*.conf', '**/**/*.conf']
	},
	python_requires='>=3.8',
	install_requires = [
		'pydantic==1.4',
		'pymongo>=3.10,<4.0'
	],
	extras_require = {
		"testing": [
			"pytest>=6.2.1,<6.3",
			"pytest-cov",
		],
	},
)
