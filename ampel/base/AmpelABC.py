#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/base/AmpelABC.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 27.12.2017
# Last Modified Date: 17.02.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

import inspect
from typing import Type, Callable


class AmpelABC:
	"""
	This class resembles python's standart ABC module (Abstract Base Class) but can additionaly
	check method signatures. As a consequence, a subclass that inherits AmpelABC, will not be able to
	implement methods declared as abstract by the parent class using different method arguments.
	Notes:
	- Multi-level and multiple inheritance are supported.
	- Overriding abstractmethod is supported (if subclass itself is abstract)
	- This class relies on the module 'inspect'
	- Setting AmpelABC._abcheck = False deactivates all checks
	- If a sub-classes implements __init_subclass__ for some reason, \
		super().__init_subclass__(**kwargs) must be called within the (class) method.
	"""

	_abcheck = True

	@classmethod
	def __init_subclass__(cls, abstract: bool = False, **kwargs) -> None:
		"""
		Creates the corresponding class
		Note: all checks can be deactivated by setting AmpelABC._abcheck = False

		:raises NotImplementedError: if an abstract method is not implemented by the child class
		:raises TypeError: if decorator flag check_signature was set for an abstract method but \
		the corresponding method signatures differ implementation by the sub class \
		:raises ValueError: if decorator flag check_super_call was set and the corresponding method \
		omits to call to the super method.
		"""

		# https://github.com/python/mypy/issues/5887
		super().__init_subclass__(**kwargs) # type: ignore

		# Class is abstract
		if abstract:
			setattr(cls, '__new__', _raise_error)
			if cls._abcheck:
				cls._check_methods(cls, "force_check")
		else:
			setattr(cls, '__new__', __std_new__)
			for method_name, method in cls.__dict__.items():
				if hasattr(method, "abstract_method"):
					raise ValueError(
						f"Method {method_name} cannot be marked as abstract "
						f"since {cls.__name__} is not an abstract class"
					)

			if cls._abcheck:
				cls._check_methods(cls, "abstract_method")
				cls._check_methods(cls, "default_method")


	@staticmethod
	def _check_methods(Klass: Type, func_attr: str) -> None:

		# Gather abstract methods (marked by the decorator @abstractmethod)
		abs_methods = {
			method_name: (base_cls, method)
			for base_cls in reversed(Klass.mro())
				for method_name, method in base_cls.__dict__.items()
					if hasattr(method, func_attr)
		}

		# Check implementation
		for method_name, value in abs_methods.items():

			if value[0] == Klass:
				continue

			# Check if method was implemented by child
			func = getattr(Klass, method_name)
			if func.__qualname__.split(".")[0] == value[0].__name__:

				# default implementation available
				if hasattr(value[1], "default_method"):
					continue
				raise NotImplementedError(
					f"Class {Klass.__name__} must implement abstract method "
					f"'{method_name}' defined in class {value[0].__name__}"
				)

			if hasattr(value[1], "check_super_call"):
				src = inspect.getsource(func)
				if not (f"super().{method_name}" in src or f".{method_name}(self" in src):
					raise ValueError(
						f"Method {method_name} from class {Klass.__name__} "
						f"must call super().{method_name}(...)"
					)

			# No signature check for methods allowing variable arguments
			if hasattr(value[1], "var_args"):
				continue

			# Get implemented method signature
			if method_name in Klass.__dict__:
				impl = Klass.__dict__[method_name]
			else:
				for K in reversed(Klass.mro()):
					if method_name in K.__dict__:
						impl = K.__dict__[method_name]
						break

			# Get abstract method signatures
			if isinstance(value[1], classmethod):
				abstract_sig = inspect.signature(value[1].__func__)
				if isinstance(impl, classmethod):
					impl = impl.__func__
				else:
					raise TypeError(f"@classmethod missing for '{Klass.__name__}.{method_name}(...)'")
			elif isinstance(value[1], staticmethod):
				abstract_sig = inspect.signature(value[1].__func__)
				if isinstance(impl, staticmethod):
					impl = impl.__func__
				else:
					raise TypeError(f"@staticmethod missing for '{Klass.__name__}.{method_name}(...)'")
			else:
				abstract_sig = inspect.signature(value[1])

			impl_sig_keys = list(inspect.signature(impl).parameters.keys())

			# Manually at cls for bound methods
			if (inspect.ismethod(impl)):
				impl_sig_keys.insert(0, 'cls')

			if (
				len(abstract_sig.parameters) != len(impl_sig_keys) or
				hasattr(value[1], "check_signature") and
				# important cast because odict_keys(['a', 'b']) == odict_keys(['b', 'a']) is True
				list(abstract_sig.parameters.keys()) != list(impl_sig_keys)
			):
				raise TypeError(
					f"Wrong method signature. Please change the arguments of method "
					f"'{method_name}' to match those defined by the corresponding "
					f"abstract method in class {value[0].__name__}\n"
					f"Required: {list(abstract_sig.parameters.keys())}\n"
					f"Implemented: {impl_sig_keys}\n"
				)


def _raise_error(cls, *args, **kwargs) -> None:
	"""
	Abstract classes cannot be instantiated
	:raises: TypeError
	"""
	raise TypeError(
		f"Class {cls.__name__} is abstract and can thus not be instantiated"
	)


def __std_new__(mcs, *arg, **kwargs) -> Callable:
	""" Standard class creation """
	cls = None
	for el in mcs.__mro__:
		# stop at first built-in type ('object' usually, but it can be 'dict'
		# for example if # the abstract subclass inherits from a python primitive type.
		# Avoids this kind of error: TypeError: object.__new__(MyDict) is not safe, use dict.__new__()
		if '__new__' in el.__dict__ and type(el.__dict__['__new__']).__name__ == "builtin_function_or_method":
			cls = el
			break
	return cls.__new__(mcs)
