#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/base/decorator.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                27.12.2017
# Last Modified Date:  04.11.2025
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from collections.abc import Callable
from functools import partial
from typing import TypeVar, overload

F = TypeVar('F', bound=Callable)


@overload
def abstractmethod(func: F) -> F:
	...

@overload
def abstractmethod(*, strict_names: bool = False, force: bool = False, var_args: bool = False) -> Callable[[F], F]:
	...

def abstractmethod(func=None, strict_names=False, force=False, var_args: bool = False):
	"""
	:param strict_names: if True, requires exact parameter name match in the implementing method
	:param force: whether implementation of methods must be checked even if the subclass is abstract as well
	:param var_args: allow variables arguments (default behavior in native python abc)
	"""

	if func is None:
		return partial(
			abstractmethod, strict_names=strict_names, force=force, var_args=var_args
		)

	if strict_names:
		func.strict_names = True

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
def defaultmethod(*, strict_names: bool = False, check_super_call: bool = False) -> Callable[[F], F]:
	...

def defaultmethod(func=None, strict_names=False, check_super_call=False):

	if func is None:
		return partial(
			defaultmethod, strict_names=strict_names,
			check_super_call=check_super_call
		)

	func.default_method = True

	if strict_names:
		func.strict_names = True

	if check_super_call:
		func.check_super_call = True

	return func
