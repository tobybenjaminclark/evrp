from dataclasses import dataclass, field
from typing import List, Tuple, Optional

@dataclass
class CustomerNode:
    latitude: float
    longitude: float
    time_slot: Tuple[int, int]
    demand: float
    id: str
    jt: List[Tuple[str, float]] = field(default_factory=list)
    je: List[Tuple[str, float]] = field(default_factory=list)



@dataclass
class DepotNode:
    latitude: float
    longitude: float
    id: str
    jt: List[Tuple[str, float]] = field(default_factory=list)
    je: List[Tuple[str, float]] = field(default_factory=list)


@dataclass
class EVChargeNode:
    latitude: float
    longitude: float
    charge_rate: float
    id: str
    jt: List[Tuple[str, float]] = field(default_factory=list)
    je: List[Tuple[str, float]] = field(default_factory=list)

