from src_road_graph.evrp_location_node import *
import logging
import concurrent.futures
import timeit
from src_road_graph.find_locations import get_directions
from instance import *



def calculate_journeys(customers, depots, chargers):
    start_time = timeit.default_timer()
    a = customers + depots + chargers

    def fetch_directions(origin_index: int, destination_index: int) -> tuple[any, any, float]:
        origin_loc = a[origin_index]
        dest_loc = a[destination_index]
        r = get_directions(f"{origin_loc.latitude}, {origin_loc.longitude}",f"{dest_loc.latitude}, {dest_loc.longitude}")
        origin_loc.jt.append((dest_loc.id, r.time_taken))
        origin_loc.je.append((dest_loc.id, r.total))

        return origin_loc, dest_loc, r.total

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for ind, origin_loc in enumerate(a):
            for other_loc_index in range(0, len(a)):
                if(ind == other_loc_index): continue
                futures.append(executor.submit(fetch_directions, ind, other_loc_index))

        for future in concurrent.futures.as_completed(futures):
            origin, destination, total = future.result()
            if total is not None: print(f"EC from: \n{origin} to \n{destination}\n is {total}")
            else:                 print(f"Error?? {total}")
            continue

    end_time = timeit.default_timer()

    logging.info(f"")
    logging.info(f"Total Time Taken (to calculate Journeys): {end_time - start_time}")



def generate_evrp_instance(customers, depots, chargers):
    calculate_journeys(customers, depots, chargers)

    # Generate Node Instances & Return List
    cust_instances = [CustomerInstance(c.demand, c.time_slot[0], c.time_slot[1], c.id, c.je, c.jt) for c in customers]
    depot_instances = [DepotInstance(c.id, c.je, c.jt) for c in depots]
    charger_instances = [EVChargeInstance(c.charge_rate, c.id, c.je, c.jt) for c in chargers]
    return Instance(cust_instances, depot_instances, charger_instances)