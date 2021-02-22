#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/model/PlotProperties.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 12.02.2021
# Last Modified Date: 17.02.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import List, Optional, Dict, Any, Type, Union
from ampel.type import StockId
from ampel.model.StrictModel import StrictModel
from ampel.abstract.AbsIdMapper import AbsIdMapper
from ampel.base.AuxUnitRegister import AuxUnitRegister


class FormatModel(StrictModel):
	"""
	:param format_str: ex: %s_figure.png
	:param arg_keys: keys to use as arguments from the extra dict (extra dict is to be built by classes)
	"""
	format_str: str
	arg_keys: Optional[List[str]]


class PlotProperties(StrictModel):
	"""
	Contains customization values for:
	- given matplotlib properties (width, height, title, ...)
	- properties associated with the figure (save filename and path, compression, tags, ...)

	If id_mapper is set (ex: ZTFIdMapper) and FormatModel.arg_keys contains 'stock',
	then the native ampel stock id will be converted to the 'external' id.
	Note that for this feature to work, an AmpelContext must have been loaded once.

	Parameter disk_save is optional and when used, makes sure that plots are additionally save to disk
	(std save procedure saves plots into the DB).

	For example:
	{
		"tags": ["SALT", "SNCOSMO"],
		"file_name": {
			"format_str": "%s_%s_fit.svg",
			"arg_keys": ["stock", "model"]
		},
		"title": {
			"format_str": "%s %s lightcurve fit",
			"arg_keys": ["stock", "catalog"]
		},
		"width": 10,
		"height": 6,
		"id_mapper": "ZTFIdMapper",
		"disk_save": "/tmp/"
	}
	will create a file called /tmp/ZTF27dpytkhq_salt2.svg for a transient with internal id 274878346346.
	The plot title will be "ZTF27dpytkhq Ned based lightcurve fit".

	Note that it is up to the class using PlotSaveOptions to make sure that
	the right argument is passed to the methods get_file_name() get_title.
	For example, if arg_keys = ["stock", "model"] (FormatModel),
	then {'stock': 123, 'model': 'salt'} must be passed as argument.


	Examples:
	In []: a = PlotProperties(**{"file_name": {"format_str": "%s_%s_fit.svg", "arg_keys": ["stock", "model"]}})

	In []: a.get_file_name(extra={'stock': 12345678, 'model': 'salt2'})
	Out[]: '12345678_salt2_fit.svg'

	# Note the reversed order of arg_keys
	In []: a = PlotProperties(**{"file_name": {"format_str": "%s_%s_fit.svg", "arg_keys": ["model", "stock"]}})

	In []: a.get_file_name(extra={'stock': 12345678, 'model': 'salt2'})
	Out[]: 'salt2_12345678_fit.svg'

	# Examples using id_mapper (error is intentional, explanation follows):
	In []: a = PlotProperties(**{"file_name": {"format_str": "%s_%s_fit.svg", "arg_keys": ["model", "stock"]}, "id_mapper": "ZTFIdMapper"})
	---------------------------------------------------------------------------
	ValidationError: 1 validation error for PlotProperties
	id_mapper
		Unknown auxiliary unit ZTFIdMapper (type=value_error)

	# As stated further above, an AmpelContext must have been loaded once for ID mapping to work.
	# For production, you need not worry about this.
	# But you might encounter this error in your local / notebook if you did not load a context.

	# The following should fix the error from above:
	In []: ctx = DevAmpelContext.load("ampel_conf.yaml")

	# Then:
	In []: a = PlotProperties(**{"file_name": {"format_str": "%s_%s_fit.svg", "arg_keys": ["model", "stock"]}, "id_mapper": "ZTFIdMapper"})
	In []: a.get_file_name(extra={'stock': 12345678, 'model': 'salt2'})
	Out[]: 'salt2_ZTF31aabrxlc_fit.svg'
	"""

	file_name: FormatModel
	title: Optional[FormatModel]
	fig_include_title: Optional[bool]
	fig_text: Optional[FormatModel] # for matplotlib
	tags: Optional[List[str]]
	width: Optional[int]
	height: Optional[int]
	compress: Optional[int]
	id_mapper: Optional[Union[str, Type[AbsIdMapper]]]
	disk_save: Optional[str] # Local folder path


	# TODO: implement other validators ?:
	# - for title and file_name: if FormatModel.arg_keys then format_str must contain '%s'
	# - if id_mapper is set but FormatModel.arg_keys does not contain 'stock' do ?

	def get_file_name(self, extra: Optional[Dict[str, Any]] = None) -> str:
		return self._format_attr(self.file_name, extra)

	def get_title(self, extra: Optional[Dict[str, Any]] = None) -> Optional[str]:
		return self._format_attr(self.title, extra) if self.title else None

	def get_fig_text(self, extra: Optional[Dict[str, Any]] = None) -> Optional[str]:
		return self._format_attr(self.fig_text, extra) if self.fig_text else None

	def _format_attr(self, attr: FormatModel, extra: Optional[Dict[str, Any]] = None) -> str:

		if attr.arg_keys and extra:

			if 'stock' in attr.arg_keys and self.id_mapper:
				extra = extra.copy()
				extra['stock'] = self.get_ext_name(extra['stock'])

			return attr.format_str % tuple(extra[k] for k in attr.arg_keys if k in extra)

		return attr.format_str


	def get_ext_name(self, ampel_id: StockId) -> str:
		""" If no id mapper is avail, the stringified ampel id is returned """

		if self.id_mapper is None:
			return str(ampel_id)

		if isinstance(self.id_mapper, str):
			self.id_mapper = AuxUnitRegister.get_aux_class(self.id_mapper, sub_type=AbsIdMapper)

		return self.id_mapper.to_ext_id(ampel_id)


	def get_compress(self) -> int:

		if self.compress: # if explicit compress is set, return this
			return self.compress
		if self.disk_save:
			return 2
		return 1
