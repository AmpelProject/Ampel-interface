from typing import Union

from ampel.struct.JournalAttributes import JournalAttributes
from ampel.struct.StockAttributes import StockAttributes
from ampel.types import StockId

T3Send = Union[JournalAttributes, StockAttributes, tuple[StockId, StockAttributes]]
