#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/util/compression.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 29.06.2021
# Last Modified Date: 29.06.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

import zipfile
from io import BytesIO
from typing import Literal

Compression = Literal['ZIP_DEFLATED', 'ZIP_DEFLATED', 'ZIP_BZIP2']

def compress(
	payload: bytes,
	filename: str,
	alg: Compression = "ZIP_DEFLATED",
	compress_level: int = 9
) -> bytes:

	outbio, zf = _new(alg, compress_level)
	zf.writestr(filename, payload)
	zf.close()
	return outbio.getvalue()


def compress_many(
	arg: dict[str, bytes],
	alg: Compression = "ZIP_DEFLATED",
	compress_level: int = 9
) -> bytes:

	outbio, zf = _new(alg, compress_level)
	for k, v in arg.items():
		zf.writestr(k, v)
	zf.close()

	return outbio.getvalue()


def _new(
	alg: Compression = "ZIP_DEFLATED",
	compress_level: int = 9
) -> tuple[BytesIO, zipfile.ZipFile]:

	outbio = BytesIO()
	return outbio, zipfile.ZipFile(
		outbio, "w", getattr(zipfile, alg), False,
		compresslevel = compress_level
	)


def decompress(arg: bytes) -> bytes:
	bio = BytesIO()
	bio.write(arg)
	zf = zipfile.ZipFile(bio)
	file_name = zf.namelist()[0]
	return zf.read(file_name)


def decompress_str(arg: bytes) -> str:
	return str(decompress(arg), "utf8")


def decompress_many(arg: bytes) -> dict[str, bytes]:
	bio = BytesIO()
	bio.write(arg)
	zf = zipfile.ZipFile(bio)
	return {file_name: zf.read(file_name) for file_name in zf.namelist()}
