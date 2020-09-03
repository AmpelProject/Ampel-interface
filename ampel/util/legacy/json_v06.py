# Deserialize JSON representations of dataclasses from Ampel v0.6

from importlib import import_module
from typing import Any, Callable, Dict, Tuple

import bson.json_util

from ampel.content.DataPoint import DataPoint
from ampel.view.LightCurve import LightCurve  # type: ignore[import]
from ampel.view.ReadOnlyDict import ReadOnlyDict

legacy_classes: Dict[str, Callable[[str, Tuple, Dict[str, Any]], Any]] = {}


def object_hook(
    dct: Dict[str, Any], options=bson.json_util.STRICT_JSON_OPTIONS,
) -> Any:
    """
	Deserialize an object serialized by AmpelEncoder
	"""
    obj = bson.json_util.object_hook(dct, options)
    if type(obj) != type(dct):
        return obj
    elif "__jsonclass__" in dct:
        jsonclass = dct.pop("__jsonclass__")
        ctor, args = jsonclass[0], jsonclass[1:]
        return legacy_classes.get(ctor, default_loader)(ctor, args, dct)
    else:
        return dct


def upgrade(*fqn):
    def decorator(func):
        for f in fqn:
            legacy_classes[f] = func
        return func

    return decorator


@upgrade("ampel.base.flags.PhotoFlags.PhotoFlags")
def flags(ctor: str, args: Tuple, kwargs: Dict[str, Any]) -> None:
    # TODO: translate flags -> tags
    return None


@upgrade(
    "ampel.base.PlainPhotoPoint.PlainPhotoPoint",
    "ampel.base.PlainUpperLimit.PlainUpperLimit",
)
def photopoint(ctor: str, args: Tuple, kwargs: Dict[str, Any]) -> DataPoint:
    return DataPoint(
        {
            "_id": kwargs["content"]["_id"],
            "body": kwargs["content"],
            "tag": kwargs["flags"],
        }
    )


@upgrade("ampel.base.LightCurve.LightCurve")
def lightcurve(ctor: str, args: Tuple, kwargs: Dict[str, Any]) -> LightCurve:
    return LightCurve(
        compound_id=bytes(kwargs["compound_id"]),
        photopoints=kwargs["ppo_list"],
        upperlimits=kwargs["ulo_list"],
        tier=kwargs["info"]["tier"],
        added=kwargs["info"]["added"],
    )


@upgrade("types.MappingProxyType")
def mappingproxy(ctor: str, args: Tuple, kwargs: Dict[str, Any]) -> ReadOnlyDict:
    return ReadOnlyDict(args[0])


def default_loader(ctor: str, args: Tuple, kwargs: Dict[str, Any]) -> DataPoint:
    parts = ctor.split(".")
    mod = import_module(".".join(parts[:-1]))
    klass = getattr(mod, parts[-1])
    # Here we treat the jsonrpc-style attrs as keyword args. This does not
    # necessarily conform to the 1.0 spec, but it's deprecated anyhow.
    return klass(*args, **kwargs)
