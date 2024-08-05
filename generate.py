from src_road_graph.evrp_location_node import *
import logging
import concurrent.futures
import timeit
from src_road_graph.find_locations import get_directions
from instance import *
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def calculate_journeys(customers, depots, chargers) -> tuple[list[CustomerNode], list[DepotNode], list[EVChargeNode]]:
    start_time = timeit.default_timer()
    a = customers + depots + chargers

    # Little function
    def fetch_directions(origin_index: int, destination_index: int, pbar: tqdm = None) -> tuple[any, any, float]:
        origin_loc = a[origin_index]
        dest_loc = a[destination_index]
        r = get_directions(f"{origin_loc.latitude}, {origin_loc.longitude}", f"{dest_loc.latitude}, {dest_loc.longitude}", pbar)
        origin_loc.jt.append((dest_loc.id, r.time_taken))
        origin_loc.je.append((dest_loc.id, r.total))
        return origin_loc, dest_loc, r.total

    pbar = tqdm(total = (len(a) * (len(a) - 1)))
    with ThreadPoolExecutor() as executor:
        # Use tqdm to create a progress bar
        futures = [
            executor.submit(fetch_directions, ind, other_loc_index, pbar)
            for ind in range(len(a))
            for other_loc_index in range(len(a))
            if ind != other_loc_index
        ]

        # Update progress bar as tasks complete
        for _ in as_completed(futures):
            pbar.update(1)

    pbar.close()
    end_time = timeit.default_timer()
    logging.info(f"Total Time Taken (to calculate Journeys): {end_time - start_time}")

def generate_evrp_instance(customers: list[CustomerNode], depots: list[DepotNode], chargers: list[EVChargeNode]) -> Instance:
    calculate_journeys(customers, depots, chargers)

    # Generate Node Instances & Return List
    cust_instances = [CustomerInstance(c.demand, c.time_slot[0], c.time_slot[1], c.id, c.je, c.jt) for c in customers]
    depot_instances = [DepotInstance(c.id, c.je, c.jt) for c in depots]
    charger_instances = [EVChargeInstance(c.charge_rate, c.id, c.je, c.jt) for c in chargers]

    return Instance(cust_instances, depot_instances, charger_instances)