#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/util/serialize.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                25.03.2021
# Last Modified Date:  20.12.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from typing import Any
from base64 import b64encode, b64decode

try:
	from bson import ObjectId
	HAVE_BSON = True
except ImportError:
	HAVE_BSON = False
 
dsi = dict.__setitem__

def walk_and_encode(arg: Any, destructive: bool = True) -> Any:
	"""
	Convert bytes values into "b64:<string>"
	Convert ObjectId instances into "oid:<hex>"
	:param destructive: true modifies the input dict(s)
	"""

	if isinstance(arg, (list, tuple, set)):
		return [walk_and_encode(el, destructive) for el in arg]

	elif isinstance(arg, dict):
		if destructive:
			for k, v in arg.items():
				if HAVE_BSON and isinstance(v, ObjectId):
					dsi(arg, k, "oid:" + v.binary.hex())
				elif isinstance(v, bytes):
					dsi(arg, k, "b64:" + b64encode(v).decode('ascii'))
				else:
					dsi(arg, k, walk_and_encode(v, destructive))
			return arg
		else:
			return {
				k: ("oid:" + v.binary.hex())
				if HAVE_BSON and isinstance(v, ObjectId) else (
					("b64:" + b64encode(v).decode('ascii'))
					if isinstance(v, bytes)
					else walk_and_encode(v, destructive)
				)
				for k, v in arg.items()
			}

	elif HAVE_BSON and isinstance(arg, ObjectId):
		return "oid:" + arg.binary.hex()

	elif isinstance(arg, bytes):
		return "b64:" + b64encode(arg).decode('ascii')

	return arg


def walk_and_decode(arg: Any) -> Any:
	"""
	Convert str values starting with "base64:" into bytes
	Note: modifies the input dict(s)
	"""

	if isinstance(arg, list):
		return [walk_and_decode(el) for el in arg]

	elif isinstance(arg, dict):
		for k, v in arg.items():
			if isinstance(v, str) and v.startswith("b64:"):
				arg[k] = b64decode(v[4:])
			elif isinstance(v, str) and v.startswith("oid:"):
				if HAVE_BSON:
					arg[k] = ObjectId(v[4:])
				else:
					raise ValueError(f"got ObjectId {v}, but pymongo is not installed")

			else:
				arg[k] = walk_and_decode(v)
		return arg

	elif isinstance(arg, str) and arg.startswith("b64:"):
		return b64decode(arg[4:])

	elif isinstance(arg, str) and arg.startswith("oid:"):
		if HAVE_BSON:
			return ObjectId(arg[4:])
		else:
			raise ValueError(f"got ObjectId {arg}, but pymongo is not installed")

	return arg
