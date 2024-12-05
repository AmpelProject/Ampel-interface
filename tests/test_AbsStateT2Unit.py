
from typing import TypedDict

from ampel.abstract.AbsStateT2Unit import AbsStateT2Unit


class Result(TypedDict):
    a: str

# NB: this does nothing at runtime, and exists only to check type annotations
def test_subclass():
    """Subclasses may return TypedDicts"""
    class PlainDictAllowed(AbsStateT2Unit):
        def process(self, compound, datapoints) -> dict[str, str]:
            return {"a": "b"}
    class TypedDictAllowed(AbsStateT2Unit):
        def process(self, compound, datapoints) -> Result:
            return {"a": "b"}