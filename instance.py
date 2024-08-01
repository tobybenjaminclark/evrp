from dataclasses import dataclass



@dataclass
class CustomerInstance():
    demand: float
    start_time: int
    end_time: int
    id: str
    journeys_energy: list[tuple[str, float]]
    journeys_time: list[tuple[str, int]]



@dataclass
class DepotInstance():
    id: str
    journeys_energy: list[tuple[str, float]]
    journeys_time: list[tuple[str, int]]



@dataclass
class EVChargeInstance:
    charge_rate: float
    id: str
    journeys_energy: list[tuple[str, float]]
    journeys_time: list[tuple[str, int]]



@dataclass
class Instance():
    customers: list[CustomerInstance]
    depots: list[DepotInstance]
    chargers: list[EVChargeInstance]


