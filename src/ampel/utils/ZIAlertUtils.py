#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/utils/ZIAlertUtils.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 24.06.2018
# Last Modified Date: 19.10.2018
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

import logging, fastavro, tarfile, os, time
from ampel.base.flags.PhotoFlags import PhotoFlags
from ampel.base.flags.TransientFlags import TransientFlags
from ampel.base.LightCurve import LightCurve
from ampel.base.TransientView import TransientView
from ampel.base.PlainPhotoPoint import PlainPhotoPoint
from ampel.base.PlainUpperLimit import PlainUpperLimit


class ZIAlertUtils:

	# pylint: disable=no-member
	photo_flags = PhotoFlags.INST_ZTF|PhotoFlags.SRC_IPAC
	# pylint: disable=no-member
	tran_flags = TransientFlags.INST_ZTF|TransientFlags.SRC_IPAC


	@staticmethod
	def to_lightcurve(file_path=None, content=None):
		"""
		Creates and returns an instance of ampel.base.LightCurve using a ZTF IPAC alert.
		"""
		return ZIAlertUtils._create_lc(
			*ZIAlertUtils._shape(
				ZIAlertUtils._get_alert_content(file_path, content)
			)
		)


	@staticmethod
	def to_transientview(file_path=None, content=None, science_records=None):
		"""
		Creates and returns an instance of ampel.base.LightCurve using a ZTF IPAC alert.
		"""
		alert_content = ZIAlertUtils._get_alert_content(file_path, content)
		now = time.time()
		lc = ZIAlertUtils._create_lc(
			*ZIAlertUtils._shape(alert_content), now
		)

		return TransientView(
			alert_content['objectId'], ZIAlertUtils.tran_flags, 
			[{'dt': now, 'tier': 0, 'loadedBy': 'ZIAlertUtils'}],
			now, photopoints=lc.ppo_list, upperlimits=lc.ulo_list,
			compounds=None, lightcurves=[lc], t2records=science_records
		)


	@staticmethod
	def _create_lc(pps, uls, now=None):
		""" """
		return LightCurve(
			os.urandom(16), 
			[PlainPhotoPoint(el, ZIAlertUtils.photo_flags, read_only=True) for el in pps], 
			[PlainUpperLimit(el, ZIAlertUtils.photo_flags, read_only=True) for el in uls] if uls else None, 
			info={'tier': 0, 'added': time.time() if now is None else now}, 
			read_only=True
		)


	@staticmethod
	def _get_alert_content(file_path=None, content=None):
		""" """
		# deserialize extracted alert content
		if file_path is not None:
			with open(file_path, 'rb') as f:
				content = ZIAlertUtils._deserialize(f)

		if content is None:
			raise ValueError("Illegal parameter")

		return content


	@staticmethod
	def _deserialize(f):
		""" """
		reader = fastavro.reader(f)
		return next(reader, None)


	@staticmethod
	def _shape(alert_content):
		""" """
		alert_content['candidate']['_id'] = alert_content['candidate'].pop('candid')
		if alert_content.get('prv_candidates') is not None:
			pps = [alert_content['candidate']]
			uls = []
			for el in alert_content['prv_candidates']:
				if el.get('candid') is not None:
					el['_id'] = el.pop('candid')
					pps.append(el)
				else:
					el['_id'] = int("%i%s%i" % (
						(2457754.5 - el['jd']) * 1000000, 
						str(el['pid'])[8:10], 
						round(el['diffmaglim'] * 1000)
					))
					uls.append(el)
			return pps, uls
		else:
			return [alert_content['candidate']], None
