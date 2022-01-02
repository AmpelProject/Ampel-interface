#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/util/bson.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                24.05.2020
# Last Modified Date:  24.05.2020
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from bson.binary import Binary

def int_to_bindata(int_arg: int) -> Binary:
	"""
	converts a python integer number (unlimited length) into a BSON data type 'BinData'.
	The used subtype 0 (\\x00): "Generic binary subtype"
	The int to bytes conversion uses the little Endian byte ordering
	(most significant byte is at the end of the byte array)
	"""
	return Binary(
		int_arg.to_bytes(
			(int_arg.bit_length() + 7) // 8,
			'little'
		),
		0
	)

def bindata_to_int(bin_data_bytes: Binary) -> int:
	"""
	converts a BSON data type 'BinData' (subtype 0) into a python integer number
	The little Endian byte ordering is used
	(most significant byte is at the end of the byte array)
	"""
	return int.from_bytes(bin_data_bytes, byteorder='little')
