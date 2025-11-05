#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/base/AmpelABC.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                27.12.2017
# Last Modified Date:  02.11.2025
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

import inspect
from collections.abc import Callable


class AmpelABC:
	"""
	This class resembles Python's standard `ABC` module (Abstract Base Class) but additionally
	enforces method signature checks. As a result, any subclass inheriting from `AmpelABC`
	cannot implement abstract methods with differing argument signatures.

	Notes:
	- Supports multi-level and multiple inheritance.
	- Allows overriding abstract methods if the subclass is itself abstract.
	- Relies on the `inspect` module.
	- Set `AmpelABC._abcheck = False` to disable all checks.
	- If a subclass defines `__init_subclass__`, it must call
	  `super().__init_subclass__(**kwargs)` within that method.
	- By convention, abstract classes that enforce methods are prefixed with `Abs`,
	  while structural ones intended only for inheritance can omit the prefix.
	"""

	_abcheck = True

	@classmethod
	def __init_subclass__(cls, abstract: bool = False, **kwargs) -> None:
		"""
		Creates the corresponding class
		Note: all checks can be deactivated by setting AmpelABC._abcheck = False

		:raises NotImplementedError: if an abstract method is not implemented by the child class
		:raises TypeError: if subclasses implement marked abstract method with a different signature \
		than the one defined in the abstract class. \
		:raises ValueError: if decorator flag check_super_call was set and the corresponding method \
		omits to call to the super method.
		"""

		super().__init_subclass__(**kwargs)

		# If class name contains '[', it is parameterization of a subclass of
		# (AmpelBaseModel, Generic), and not a true subclass. Skip it.
		if '[' in cls.__name__:
			return

		# Class is abstract
		if abstract:
			setattr(cls, '__new__', _raise_error) # noqa: B010
			if cls._abcheck:
				cls._check_methods(cls, "force_check")
		else:
			setattr(cls, '__new__', __std_new__) # noqa: B010
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
	def _check_methods(Klass: type, func_attr: str) -> None:

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
			if func.__qualname__.split(".")[-2] == value[0].__name__:

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
				(hasattr(value[1], "strict_names") and
				# important cast because odict_keys(['a', 'b']) == odict_keys(['b', 'a']) is True
				list(abstract_sig.parameters.keys()) != list(impl_sig_keys))
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
