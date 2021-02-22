# Deserialize JSON representations of dataclasses from Ampel v0.6

from importlib import import_module
from typing import Any, Callable, Dict, List, Tuple

import bson.json_util  # type: ignore[import]

from ampel.content.Compound import Compound
from ampel.content.DataPoint import DataPoint
from ampel.content.T2Document import T2Document
from ampel.view.LightCurve import LightCurve  # type: ignore[import]
from ampel.view.ReadOnlyDict import ReadOnlyDict
from ampel.view.TransientView import TransientView  # type: ignore[import]

from ampel.ztf.legacy_utils import to_ztf_id  # type: ignore[import]
from ampel.ztf.util.ZTFIdMapper import to_ampel_id  # type: ignore[import]

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


_ampel_flags = {
    0: "ZTF",
}

_ampel_photo_flags = {
    20: "PHOTOPOINT",
    21: "UPPERLIMIT",
    22: "BAND_ZTF_G",
    23: "BAND_ZTF_R",
    24: "BAND_ZTF_I",
    25: "ZTF_COLLAB",
    26: "ZTF_PUB",
}

_ampel_tran_flags = {
    20: "HAS_ERROR",
    21: "T1_AUTO_COMPLETE",
}

_ampel_compound_flags = {
    20: "HAS_UPPER_LIMITS",
    21: "HAS_AUTOCOMPLETED_PHOTO",
    22: "HAS_SUPERSEDED_PPS",
    23: "HAS_EXCLUDED_PPS",
    24: "HAS_MANUAL_EXCLUSION",
    25: "HAS_DATARIGHTS_EXCLUSION",
    26: "WITH_CUSTOM_POLICIES",
    27: "ZTF_COLLAB_DATA",
}


@upgrade("ampel.base.flags.PhotoFlags.PhotoFlags")
def photoflags(ctor: str, args: Tuple, kwargs: Dict[str, Any]) -> List[str]:
    return [
        v
        for k, v in {**_ampel_flags, **_ampel_photo_flags}.items()
        if args[0] & (1 << k)
    ]


@upgrade("ampel.base.flags.TransientFlags.TransientFlags")
def tranflags(ctor: str, args: Tuple, kwargs: Dict[str, Any]) -> List[str]:
    return [
        v
        for k, v in {**_ampel_flags, **_ampel_tran_flags}.items()
        if args[0] & (1 << k)
    ]


@upgrade("ampel.core.flags.CompoundFlags.CompoundFlags")
def compflags(ctor: str, args: Tuple, kwargs: Dict[str, Any]) -> List[str]:
    return [
        v
        for k, v in {**_ampel_flags, **_ampel_compound_flags}.items()
        if args[0] & (1 << k)
    ]


@upgrade("ampel.base.Compound.Compound")
def comp(ctor: str, args: Tuple, kwargs: Dict[str, Any]) -> Compound:
    return Compound(
        {
            "_id": bytes(kwargs["id"]),
            "added": kwargs["added"],
            "tier": kwargs["tier"],
            "stock": kwargs["stockId"],  # FIXME: translate old stockIds?
            "len": kwargs["len"],
            "tag": kwargs["alTags"],
            "body": [
                {"id": v, "tag": ["UPPERLIMIT" if k == "ul" else "PHOTOPOINT"]}
                for entry in kwargs["comp"]
                for k, v in entry.items()
            ],
        }
    )


@upgrade("ampel.base.ScienceRecord.ScienceRecord")
def t2(ctor: str, args: Tuple, kwargs: Dict[str, Any]) -> T2Document:
    return T2Document(
        {
            "_id": bytes(),
            "stock": kwargs["tran_id"],  # FIXME: translate old stockIds?
            "unit": kwargs["t2_unit_id"],
            "link": [bytes(c) for c in kwargs["compound_id"]],
            "body": [
                {
                    "version": entry["versions"]["py"],
                    "ts": entry["dt"],
                    "duration": entry["duration"],
                    "run": entry["runId"],
                    "result": entry["output"],
                }
                for entry in kwargs["results"]
            ],
        }
    )


@upgrade("ampel.base.TransientView.TransientView")
def tview(ctor: str, args: Tuple, kwargs: Dict[str, Any]) -> TransientView:
    # translate legacy id
    ampel_id = to_ampel_id(to_ztf_id(kwargs["tran_id"]))
    return TransientView(
        id=ampel_id,
        extra={},
        stock={
            "_id": ampel_id,
            "tag": kwargs["flags"],
            "name": kwargs["tran_names"],
            "journal": kwargs["journal"],
            "channel": kwargs["channel"],
        },
        t0=kwargs["photopoints"] + kwargs["upperlimits"],
        t1=kwargs["compounds"],
        t2=kwargs["t2records"],
    )


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
        stock_id=bytes(kwargs["stock_id"]),
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
