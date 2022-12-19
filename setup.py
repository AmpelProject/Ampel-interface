#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/setup.py
# License:             BSD-3-Clause
# Author:              vb, jvs
# Date:                Unspecified
# Last Modified Date:  19.12.2022
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from setuptools import setup, find_namespace_packages

install_requires = ['PyYAML>=5.4.1,<7.0.0', 'pydantic>=1.8,<2']
extras_require = {
	'docs': [
		'Sphinx>=3.5.1,<4.0.0',
		'sphinx-autodoc-typehints>=1.11.1,<2.0.0',
		'tomlkit>=0.7.0,<0.8.0'
	]
}

setup(
	name = 'ampel-interface',
	version = '0.8.3-beta.13',
	description = 'Base classes for the Ampel analysis platform',
	long_description = '# Ampel-interface\n\n`ampel-interface` provides type-hinted abstract base classes for [Ampel](https://ampelproject.github.io).',
	author = 'Valery Brinnel',
	#author_email = None,
	maintainer = 'Jakob van Santen',
	maintainer_email = 'jakob.van.santen@desy.de',
	url = 'https://ampelproject.github.io',
	packages = find_namespace_packages(),
	package_data = {'': ['*']},
	install_requires = install_requires,
	extras_require = extras_require,
	python_requires = '>=3.10,<4.0',
)
