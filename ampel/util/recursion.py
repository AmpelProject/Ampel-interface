#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/util/recursion.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 16.11.2021
# Last Modified Date: 16.11.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Union, Optional, Callable


def walk_and_process_dict(
	arg: Union[dict, list], callback: Callable,
	match: Optional[list[str]] = None, path: str = None, **kwargs
) -> bool:
	"""
	callback is called with 4 arguments:
	1) the path of the possibly nested entry. Ex: 'processor.config.select' or 'processor'
	2) the matching key (from list 'match'). Ex: 'config'
	3) the matching (sub) dict
	4) the **kwargs provided to this method
	and should return True if a modification was performed

	Simplest callback function:
	def my_callback(path, k, d):
		print(f'{path} -> {k}: {d}\n')
		return False

	:returns: True if a modification was performed, False otherwise
	"""

	ret = False

	if isinstance(arg, list):
		for i, el in enumerate(arg):
			ret = walk_and_process_dict(
				el, callback, match, f'{path}.{i}' if path else f'{i}', **kwargs
			) or ret

	if isinstance(arg, dict):

		for k, v in arg.items():

			if not match or k in match:
				ret = callback(path, k, arg, **kwargs) or ret

			if isinstance(v, dict):
				ret = walk_and_process_dict(
					v, callback, match, f'{path}.{k}' if path else f'{k}', **kwargs
				) or ret

			if isinstance(v, list):
				for i, el in enumerate(v):
					ret = walk_and_process_dict(
						el, callback, match, f'{path}.{k}.{i}' if path else f'{k}.{i}', **kwargs
					) or ret

	return ret
