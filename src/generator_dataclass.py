from json import load
from dataclasses import dataclass
from src_road_graph.evrp_location_node import *
from generate import generate_evrp_instance
from instance_dataclass import Instance



@dataclass
class CustomerNodeGenerator():
    """ Class representing input parameters for a `customer` node for an EVRP benchmark. """

    latitude: float
    longitude: float
    demand: int
    start_time: int
    end_time: int



@dataclass
class DepotNodeGenerator():
    """ Class representing input parameters for a `depot` node for an EVRP benchmark. """

    latitude: float
    longitude: float



@dataclass
class EVChargePointNodeGenerator():
    """ Class representing input parameters for a `charger` node for an EVRP benchmark. """

    latitude: float
    longitude: float
    charge_rate: float



@dataclass
class Generator():
    """ Class representing input parameters for an EVRP benchmark. """

    customers: list[CustomerNodeGenerator]
    depots: list[DepotNodeGenerator]
    chargers: list[EVChargePointNodeGenerator]
    output_path: str
    instance_id: str

    def run(self) -> Instance:
        """ Function to generate and return an EVRP Instance from a generator """

        cust_nodes = [CustomerNode(c.latitude, c.longitude, (c.start_time, c.end_time), c.demand, "C" + str(i)) for i, c in enumerate(self.customers)]
        depot_nodes = [DepotNode(c.latitude, c.longitude, "D" + str(i)) for i, c in enumerate(self.depots)]
        chargers = [EVChargeNode(c.latitude, c.longitude, c.charge_rate, "E" + str(i)) for i, c in enumerate(self.chargers)]
        return generate_evrp_instance(cust_nodes, depot_nodes, chargers)



def load_json(path: str) -> dict|Exception:
    """ Function to load a JSON configuration file """

    with open(path, 'r') as config_file: return load(config_file)



def build_customer_generator(customer_dict: dict) -> CustomerNodeGenerator:
    """ Function to build an Customer Node input node, from a dictionary (parsed from config. file JSON) """

    return CustomerNodeGenerator(latitude=customer_dict['latitude'], longitude=customer_dict['longitude'], demand=customer_dict['demand'], start_time=customer_dict['start_time'], end_time=customer_dict['end_time'])



def build_depot_node_generator(depot_dict: dict) -> DepotNodeGenerator:
    """ Function to build an Depot Node input node, from a dictionary (parsed from config. file JSON) """

    return DepotNodeGenerator(latitude=depot_dict['latitude'], longitude=depot_dict['longitude'])



def build_ev_node_generator(ev_dict: dict) -> EVChargePointNodeGenerator:
    """ Function to build an EV Node input node, from a dictionary (parsed from config. file JSON) """

    return EVChargePointNodeGenerator(latitude=ev_dict['latitude'], longitude=ev_dict['longitude'], charge_rate=ev_dict['charge_rate'])



def build_generator(path: str):
    """ Function to construct a generator from a configuration file. """

    try: config = load_json(path)
    except Exception as e: raise Exception(f"Failed to open configuration file: {e}")

    # Construct & Return Generator
    return Generator([build_customer_generator(c) for c in config['customers']],
                     [build_depot_node_generator(d) for d in config['depots']],
                    [build_ev_node_generator(ev) for ev in config['chargers']],
                     config['output_path'], config['instance_id'])



if __name__ == "__main__":
    g=build_generator("test2.json")
    i = g.run()
    print(i)
    i.write("test.output")




