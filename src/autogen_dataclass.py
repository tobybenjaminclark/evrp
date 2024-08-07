from dataclasses import dataclass
from generator_dataclass import Generator, DepotNodeGenerator, CustomerNodeGenerator, EVChargePointNodeGenerator
from geopy.distance import geodesic
from random import uniform, gauss
from src.src_apis.src_open_heat_map import find_ev_charging_points
from src_road_graph.find_locations import find_locations
from src_apis.src_google_api import PlaceType
from math import ceil
from random import randrange, randint
from json import dump
from itertools import combinations
from src_road_graph.evrp_route_utils import haversine

def generate_random_windows(customers: list[CustomerNodeGenerator], window_length: int, horizon: tuple[int, int]) -> None:
    for customer in customers:
        start = randint(horizon[0], horizon[1] - window_length)
        end = start + window_length
        customer.start_time = start
        customer.end_time = end
    return



def generate_stratisfied_windows(customers: list[CustomerNodeGenerator], window_length: int, horizon: tuple[int, int]) -> None:
    n_customers = len(customers)
    total_range = horizon[1] - horizon[0]
    interval = total_range // n_customers

    for i, customer in enumerate(customers):
        start = horizon[0] + (i * interval) % total_range
        end = start + window_length
        if end > horizon[1]:
            end = end % total_range
        customer.start_time = start
        customer.end_time = end
    return


def generate_time_windows(customers: list[CustomerNodeGenerator], method: str, wtype: str, horizon: tuple[int, int]) -> None:
    window_length = 120 if wtype == "NARROW" else (240 if wtype == "MODERATE" else 360)
    match(method):
        case "R": return generate_random_windows(customers, window_length, horizon)
        case "S": return generate_stratisfied_windows(customers, window_length, horizon)



def genp_random(c_count: int, centre: tuple[float, float], range_m: int, _type: type) -> list[CustomerNodeGenerator]|list[DepotNodeGenerator]|list[EVChargePointNodeGenerator]:
    customers = []

    for _ in range(0, c_count):
        # Generate random distance and bearing
        distance_m = uniform(0, range_m / 1000)
        bearing = uniform(0, 360)

        # Calculate the destination point
        destination = geodesic(kilometers = distance_m).destination(centre, bearing)

        # Create a CustomerNodeGenerator object and add to the list
        customers.append((destination.latitude, destination.longitude))

    # Map points back to desired type.
    if _type is CustomerNodeGenerator: customers = list(map(lambda v: CustomerNodeGenerator(*v, randrange(0, 50) / 10, 0, 0), customers))
    elif _type is DepotNodeGenerator: customers = list(map(lambda v: DepotNodeGenerator(*v), customers))
    elif _type is EVChargePointNodeGenerator: customers = list(map(lambda v: EVChargePointNodeGenerator(*v, randrange(4, 6) * 10), customers))

    return customers[:c_count]



def genp_clustered(count: int, centre: tuple[float, float], range_m: int, _type: type) -> list[CustomerNodeGenerator]|list[DepotNodeGenerator]|list[EVChargePointNodeGenerator]:
    customers = []
    cluster_count = max(1, ceil(count / 6))  # Ensure at least one cluster
    customers_per_cluster = ceil(count / cluster_count)
    cluster_range_m = range_m / 10  # The range for each cluster around its center

    # Randomly assign each customer to a cluster!
    # ...

    for _ in range(cluster_count):
        # Generate a center point for each cluster
        cluster_distance_m = uniform(0, range_m / 1000)
        cluster_bearing = uniform(0, 360)
        cluster_centre = geodesic(kilometers=cluster_distance_m).destination(centre, cluster_bearing)

        # Generate customers around the cluster center
        for _ in range(customers_per_cluster):
            distance_m = abs(uniform(0, cluster_range_m / 1000))  # Smaller range for tighter clustering
            bearing = uniform(0, 360)

            # Calculate the destination point for the customer
            destination = geodesic(kilometers=distance_m).destination((cluster_centre.latitude, cluster_centre.longitude), bearing)

            # Create a CustomerNodeGenerator object and add to the list
            customers.append((destination.latitude, destination.longitude))

    # Map points back to desired type.
    if _type is CustomerNodeGenerator: customers = list(map(lambda v: CustomerNodeGenerator(*v, randrange(0, 50) / 10, 0, 0), customers))
    elif _type is DepotNodeGenerator: customers = list(map(lambda v: DepotNodeGenerator(*v), customers))
    elif _type is EVChargePointNodeGenerator: customers = list(map(lambda v: EVChargePointNodeGenerator(*v, randrange(2, 6) * 10), customers))

    # Trim the list if there are extra customers due to ceiling rounding
    return customers[:count]



def genp_realistic(count: int, centre: tuple[float, float], range_m: int, _type: type) -> list[CustomerNodeGenerator]|list[DepotNodeGenerator]|list[EVChargePointNodeGenerator]:

    ptypes = [PlaceType.ATM, PlaceType.CAFE, PlaceType.PARKING, PlaceType.STORE, PlaceType.RESTAURANT, PlaceType.SUPERMARKET]
    customers = []
    while(len(customers) < count and len(ptypes) > 0):
        locs = find_locations(centre, range_m, "", type = ptypes.pop(0))
        for loc, name in locs:
            if(len(customers) < count):
                customers.append(CustomerNodeGenerator(loc.latitude, loc.longitude, loc.demand, 0, 0))
            else: break

    # Could always switch to random/clustered?
    if(len(customers) < count):
        raise Exception(f"Couldn't find enough customers for realistic generation, found {len(customers)}, required {count}.\n Centre is {centre}")

    return customers[:count]



def genp_ev(c: int, centre: tuple[float, float]) -> list[EVChargePointNodeGenerator]:
    return list(map(lambda v: EVChargePointNodeGenerator(v[0].latitude, v[0].longitude, v[0].charge_rate), find_ev_charging_points(*centre, c)))[:c]



def generate_nodes(samp: str, num: int, centre: tuple[float, float], max_dist: int, _type: type) -> list[CustomerNodeGenerator] | list[DepotNodeGenerator] | list[EVChargePointNodeGenerator]:

    rando = lambda c: genp_random(c, centre, max_dist, _type)
    clust = lambda c: genp_clustered(c, centre, max_dist, _type)
    if _type is CustomerNodeGenerator or _type is DepotNodeGenerator: reali = lambda c: genp_realistic(c, centre, max_dist, _type)
    else: reali = lambda c: genp_ev(c, centre)

    match samp:
        case "R":       return rando(num)
        case "C":       return clust(num)
        case "RL":      return reali(num)
        case "R_C":     return rando(num // 2) + clust(num - num // 2)
        case "R_RL":    return rando(num // 2) + reali(num - num // 2)
        case "C_RL":    return clust(num // 2) + reali(num - num // 2)
        case "R_C_RL":
            # rando(num // 3) + clust((num - num // 3) // 2) + reali(num - num // 3 - (num - num // 3) // 2)
            r = rando(num // 3)
            c = clust((num - num // 3) // 2)
            rl = reali(num - num // 3 - (num - num // 3) // 2)
            return r+c+rl
        case _:
            raise Exception("Customer sampling does not match any of predefined constants.")



@dataclass
class AutoGenerator:

    customer_count: int
    depot_count: int
    charger_count: int

    central_location: tuple[float, float]
    range: int

    # Sampling Types
    customer_sampling: str
    depot_sampling: str
    charger_sampling: str

    # Time Window Sampling
    time_window_gen: str
    time_window_type: str

    # Instance number
    inst_num: int

    def build(self) -> Generator:

        customers = generate_nodes(self.customer_sampling, self.customer_count, self.central_location, self.range, CustomerNodeGenerator)
        depots = generate_nodes(self.depot_sampling, self.depot_count, self.central_location, self.range, DepotNodeGenerator)
        chargers = generate_nodes(self.charger_sampling, self.charger_count, self.central_location, self.range, EVChargePointNodeGenerator)
        generate_time_windows(customers, self.time_window_gen, self.time_window_type, [0, 1440])
        instance_id = self.customer_sampling + {"WIDE": "3", "MODERATE": "2", "NARROW": "1"}[self.time_window_type] + str(self.inst_num) + "_" + str(len(customers)) + "_" + str(len(chargers))

        generator_data = {
            "customers" : [{"latitude": c.latitude,
                            "longitude": c.longitude,
                            "demand": c.demand,
                            "start_time": c.start_time,
                            "end_time": c.end_time} for c in customers],
            "depots" : [{"latitude": d.latitude,
                        "longitude": d.longitude} for d in depots],
            "chargers" : [{"latitude": c.latitude,
                            "longitude": c.longitude,
                           "charge_rate": c.charge_rate} for c in chargers],
            "output_path": "output/",
            "instance_id": instance_id
        }

        # Longest distance between any 2 points
        longest_dist = max([haversine((n1.latitude, n1.longitude), (n2.latitude, n2.longitude)) for n1, n2 in combinations(customers + depots + chargers, 2)])
        print(f"Longest distance between any 2 nodes is {longest_dist}m")

        filename = instance_id + ".spec"
        with open(filename, 'w') as file:
            dump(generator_data, file, indent = 4)  # `indent=4` for pretty printing



a = AutoGenerator(3, 1, 3, (52.949836, -1.147872), 3000, "R_C_RL", "R_C_RL", "R_C_RL", "S", "WIDE", 1)
a.build()
