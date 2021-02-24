#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/base/decorator.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 27.12.2017
# Last Modified Date: 17.05.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from functools import partial
from typing import TypeVar, Callable, overload

F = TypeVar('F', bound=Callable)


@overload
def abstractmethod(func: F) -> F:
	...

@overload
def abstractmethod(*, check_signature: bool = False, force: bool = False, var_args: bool = False) -> Callable[[F], F]:
	...

def abstractmethod(func=None, check_signature=False, force=False, var_args: bool = False):
	"""
	:param check_signature: checks method signature (parameter names must equal)
	:param force: whether implementation of methods must be checked even if the subclass is abstract as well
	:param var_args: allow variables arguments (default behavior in native python abc)
	"""

	if func is None:
		return partial(
			abstractmethod, check_signature=check_signature, force=force, var_args=var_args
		)

	if check_signature:
		func.check_signature = True

	if force:
		func.force_check = True

	if var_args:
		func.var_args = True

	func.abstract_method = True
	# emulate abc.abstractmethod to inform autodoc of abstract methods
	func.__isabstractmethod__ = True
	return func


@overload
def defaultmethod(func: F) -> F:
	...

@overload
def defaultmethod(*, check_signature: bool = False, check_super_call: bool = False) -> Callable[[F], F]:
	...

def defaultmethod(func=None, check_signature=False, check_super_call=False):

	if func is None:
		return partial(
			defaultmethod, check_signature=check_signature,
			check_super_call=check_super_call
		)

	func.default_method = True

	if check_signature:
		func.check_signature = True

	if check_super_call:
		func.check_super_call = True

	return func
