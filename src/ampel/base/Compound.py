
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class Compound:
	id: Any
	comp: Any = None
	added: Any = None
	alDocType: Any = None
	alFlags: Any = None
	lastJD: Any = None
	len: int = None
	ppId: Any = None
	tier: int = None
	tranId: Any = None
	flavors: Any = None
