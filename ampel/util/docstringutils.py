#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/utils/docstringutils.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 02.09.2018
# Last Modified Date: 11.12.2019
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

import inspect, re

regex_ignore = re.compile(':[ \t]*?ClassVar|[ \t]*?#')
regex_stop = re.compile('^[ \t]*?@|^[ \t]*?def|^class ')

def gendocstring(klass):
	"""
	=============================================================================
	Decorator for model sub-classes and python 3.7 dataclasses.
	-> Automatically generates doctring based on class members (makes required
	variables (including type hints) available in docstring)
	=============================================================================

	Note: the module 'inspect' does not work with classes defined within ipython
	
	Code example:
	~~~~~~~~~~~~~
	
		from ampel.base.AmpelBaseModel import AmpelBaseModel
		from ampel.util.docstringutils import gendocstring
	
		@gendocstring
		class MyConfig(AmpelBaseModel):
			my_str: str
			my_int: int = 0
	
		@gendocstring
		class MyConfig2(AmpelBaseModel):
			\"\"\"
			Existing docstrings will be preserved
			\"\"\"
			my_str2: str
			my_int2: int = 0

	Generated docstrings:
	~~~~~~~~~~~~~~~~~~~~~
	
		In []: print(MyConfig.__doc__)
		Out []:
		===================
		Fields:
		  my_str: str
		  my_int: int = 0
		===================
	
		In []: print(MyConfig2.__doc__)
		Out []:
		=====================================
		Existing docstrings will be preserved
		-------------------------------------
		Fields:
		  my_str2: str
		  my_int2: int = 0
		=====================================
	"""
	out_doc = []
	exisiting_doc = []
	in_doc = inspect.getdoc(klass)

	if in_doc:
		# Gather existing docstring
		for el in in_doc.split('\n'):
			sel = el.strip()
			if not sel:
				continue
			exisiting_doc.append(el)

	for el in inspect.getsource(klass).split('\n')[1:]:

		ell = el.strip()

		# Ignore non field-definitions
		if not ell or ":" not in ell or regex_ignore.findall(ell):
			continue

		if regex_stop.findall(ell):
			break
			
		out_doc.append("  " + ell)

	max_len = max([len(el) for el in out_doc+exisiting_doc]+[19])
	klass.__doc__ = "="*max_len + "\n"

	if exisiting_doc:
		klass.__doc__ += "\n".join(exisiting_doc) + "\n" + "-"*max_len + "\n"

	klass.__doc__ += \
		"Fields: \n" + \
		"\n".join(out_doc) + \
		"\n" + "="*max_len + "\n"
	
	return klass
