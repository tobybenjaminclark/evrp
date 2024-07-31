from json import load
from dataclasses import dataclass

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
    depots: list[DepotNodeGenerator]
    chargers: list[EVChargePointNodeGenerator]

def load_json(path: str) -> dict|Exception:
    with open(path, 'r') as config_file: return load(config_file)

def build_customer_generator(customer_dict: dict) -> CustomerNodeGenerator:
    return CustomerNodeGenerator(latitude=customer_dict['latitude'], longitude=customer_dict['longitude'], demand=customer_dict['demand'], start_time=customer_dict['start_time'], end_time=customer_dict['end_time'])

def build_depot_node_generator(depot_dict: dict) -> DepotNodeGenerator:
    return DepotNodeGenerator(latitude=depot_dict['latitude'], longitude=depot_dict['longitude'])

def build_ev_node_generator(ev_dict: dict) -> EVChargePointNodeGenerator:
    return EVChargePointNodeGenerator(latitude=ev_dict['latitude'], longitude=ev_dict['longitude'], charge_rate=ev_dict['charge_rate'])

def build_generator(path: str):

    # Open JSON
    try: config = load_json(path)
    except Exception as e: raise Exception(f"Failed to open configuration file: {e}")

    print(config)

    customers: list[CustomerNodeGenerator] = [build_customer_generator(c) for c in config['customers']]
    depots: list[DepotNodeGenerator] = [build_depot_node_generator(d) for d in config['depots']]
    chargers: list[EVChargePointNodeGenerator] = [build_ev_node_generator(ev) for ev in config['chargers']]

if __name__ == "__main__":
    build_generator("test.json")




