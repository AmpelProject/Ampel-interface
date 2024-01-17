
import inspect
import json
from enum import IntFlag
from functools import partial
from importlib import import_module
from types import MappingProxyType

import bson.json_util


def load(fileobj, ignore_missing_modules=True):
	for line in fileobj:
		yield json.loads(
			line,
			object_hook=partial(
				object_hook,
				ignore_missing_modules=ignore_missing_modules
			)
		)

class AmpelEncoder(json.JSONEncoder):
	"""
	Serialize objects in a mix of:
	a) JSONRPC 1.0-like class hinting for custom Ampel types
	b) PyMongo-provided JSON representation for BSON types
	"""
	def __init__(self, *args, lossy: bool=False, **kwargs):
		"""
		if lossy, cast mappingproxy to dict, set and tuple to list, etc
		"""
		self.lossy = lossy
		super().__init__(*args, **kwargs)
		self.bson_options = bson.json_util.CANONICAL_JSON_OPTIONS

	def default(self, obj, fallthrough=False):
		"""
		Encode selected types in jsonrpc class-hint notation
		"""
		serializer = self.get_serializer(obj) # type: ignore[no-untyped-call]
		if serializer is not None:
			if obj.__class__.__module__ == "builtins":
				module_name = "builtins"
			else:
				if (module := inspect.getmodule(obj)) is None:
					raise ValueError("Cannot serialize object without module")
				module_name = module.__name__
			json_class = obj.__class__.__name__
			if module_name not in ['', '__main__']:
				json_class = f'{module_name}.{json_class}'
			# mappingproxy lies about its type
			if type(obj) == MappingProxyType:
				json_class = 'types.MappingProxyType'
			rep = serializer(obj)
			if isinstance(rep, tuple):
				assert len(rep) == 2
				params, attrs = rep
			elif isinstance(rep, dict):
				params, attrs = [], rep
			else:
				params, attrs = rep, {}
			return {"__jsonclass__": [json_class, *self.default(params, True)], **self.default(attrs, True)} # type: ignore[no-untyped-call]
		if hasattr(obj, 'items'):
			return {self.default(k, True): self.default(v, True) for k,v in obj.items()} # type: ignore[no-untyped-call]
		if isinstance(obj, list | set | tuple):
			return [self.default(k, True) for k in obj] # type: ignore[no-untyped-call]
		# convert remaining Mongo types
		try:
			return bson.json_util.default(obj, self.bson_options)
		except TypeError:
			if fallthrough:
				return obj
			raise

	def get_serializer(self, obj):
		"""
		Serializers for types we want to preserve
		"""
		if (hasattr(type(obj), "__reduce__") and (reduce := getattr(type(obj), "__reduce__")) != object.__reduce__): # noqa: B009
			return lambda x: (list(reduce(x)[1]), {})
		if hasattr(obj, '__dataclass_fields__'):
			return lambda x: x.__dict__
		if isinstance(obj, IntFlag):
			return lambda x: [int(x)]
		if self.lossy:
			return None

		# try to preserve types
		if isinstance(obj, set | tuple):
			return lambda x: [list(x)]
		if isinstance(obj, MappingProxyType):
			return lambda x: [dict(obj)]
		return None

def object_hook(
    dct,
    options=bson.json_util.CANONICAL_JSON_OPTIONS,
    ignore_missing_modules=True
):
	"""
	Deserialize an object serialized by AmpelEncoder
	"""
	obj = bson.json_util.object_hook(dct, options)
	if type(obj) != type(dct):
		return obj
	if "__jsonclass__" in dct:
		ctor = dct.pop("__jsonclass__")
		parts = ctor[0].split('.')
		try:
			mod = import_module('.'.join(parts[:-1]))
		except ModuleNotFoundError:
			if ignore_missing_modules:
				return None
			raise
		klass = getattr(mod, parts[-1])
		# Here we treat the jsonrpc-style attrs as keyword args. This does not
		# necessarily conform to the 1.0 spec, but it's deprecated anyhow.
		return klass(*ctor[1:], **dct)
	return dct
