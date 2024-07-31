from json import load
from dataclasses import dataclass

def load_json(path: str) -> dict|Exception:
    with open(path, 'r') as config_file: return load(config_file)

def build_generator(path: str):
    return

@dataclass
class CustomerNodeGenerator():
    latitude: float
    longitude: float
    demand: int
    start_time: int
    end_time: int

@dataclass
class DepotNodeGenerator():
    latitude: float
    longitude: float

@dataclass
class EVChargePointNodeGenerator():
    latitude: float
    longitude: float
    charge_rate: float

@dataclass
class Generator():
    customers: list[CustomerNodeGenerator]



