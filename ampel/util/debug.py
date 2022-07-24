#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/util/debug.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                24.07.2022
# Last Modified Date:  24.07.2022
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

import sys, pdb

# From stackoverflow
class ForkedPdb(pdb.Pdb):
	"""
	A Pdb subclass that may be used within a multiprocessing process

	Forword: If you are not using multiprocessing, just use breakpoint()

	Usage:
	insert: "ForkedPdb().set_trace()" at the wished position
	<run your job>
	a pdb shell should pop up, type "interact" and press enter
	<do debug>
	when you are done, press CTRL-D
	you are back in the pdb shell, type "continue" and press enter
	Hope this helps
	"""

	def interaction(self, *args, **kwargs):
		_stdin = sys.stdin
		try:
			sys.stdin = open('/dev/stdin')
			pdb.Pdb.interaction(self, *args, **kwargs)
		finally:
			sys.stdin = _stdin

