#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/util/compression.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                29.06.2021
# Last Modified Date:  20.04.2022
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

import zipfile
from io import BytesIO
from typing import Literal

TCompression = Literal['ZIP_DEFLATED', 'ZIP_LZMA', 'ZIP_BZIP2']

def compress(
	payload: bytes,
	filename: str,
	alg: TCompression = "ZIP_DEFLATED",
	compression_level: int = 9
) -> bytes:

	outbio, zf = _new_zip_file(alg, compression_level)
	zf.writestr(filename, payload)
	zf.close()
	return outbio.getvalue()


def compress_many(
	arg: dict[str, bytes],
	alg: TCompression = "ZIP_DEFLATED",
	compression_level: int = 9
) -> bytes:

	outbio, zf = _new_zip_file(alg, compression_level)
	for k, v in arg.items():
		zf.writestr(k, v)
	zf.close()

	return outbio.getvalue()


def _new_zip_file(
	alg: TCompression = "ZIP_DEFLATED",
	compression_level: int = 9
) -> tuple[BytesIO, zipfile.ZipFile]:

	outbio = BytesIO()
	return outbio, zipfile.ZipFile(
		outbio, "w", getattr(zipfile, alg), False,
		compresslevel = compression_level
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
