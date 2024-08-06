from dataclasses import dataclass
from generator_dataclass import Generator, DepotNodeGenerator, CustomerNodeGenerator, EVChargePointNodeGenerator
from geopy.distance import geodesic
from random import uniform, gauss
from src_road_graph.find_locations import find_locations
from src_apis.src_google_api import PlaceType
from math import ceil



def generate_customers_random(c_count: int, centre: tuple[float, float], range_m: int) -> list[CustomerNodeGenerator]:
    customers = []

    for _ in range(0, c_count):
        # Generate random distance and bearing
        distance_m = uniform(0, range_m / 1000)
        bearing = uniform(0, 360)

        # Calculate the destination point
        destination = geodesic(kilometers = distance_m).destination(centre, bearing)

        # Create a CustomerNodeGenerator object and add to the list
        customers.append(CustomerNodeGenerator(destination.latitude, destination.longitude, 0, 0, 0))

    return customers[:c_count]



def generate_customers_clustered(count: int, centre: tuple[float, float], range_m: int) -> list[CustomerNodeGenerator]:
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
            customers.append(CustomerNodeGenerator(destination.latitude, destination.longitude, 0, 0, 0))

    # Trim the list if there are extra customers due to ceiling rounding
    return customers[:count]



def generate_customers_realistic(count: int, centre: tuple[float, float], range_m: int) -> list[CustomerNodeGenerator]:

    ptypes = [PlaceType.ATM, PlaceType.CAFE, PlaceType.PARKING, PlaceType.STORE, PlaceType.RESTAURANT, PlaceType.SUPERMARKET]
    customers = []
    while(len(customers) < count and len(ptypes) > 0):
        locs = find_locations(centre, range_m, "", type = ptypes.pop(0))
        for loc, name in locs:
            if(len(customers) < count): customers.append(CustomerNodeGenerator(loc.latitude, loc.longitude, loc.demand, 0, 0))
            else: break

    # Could always switch to random/clustered?
    if(len(customers) < count):
        raise Exception("Couldn't find enough customers for realistic generation.")

    return customers[:count]



def generate_customers(customer_sampling: str, customer_count: int, centre: tuple[float, float], range: int) -> list[CustomerNodeGenerator]:
    match customer_sampling:
        case "R":
            return generate_customers_random(customer_count, centre, range)
        case "C":
            return generate_customers_clustered(customer_count, centre, range)
        case "RL":
            return generate_customers_realistic(customer_count, centre, range)
        case "R_C":
            random_count = customer_count // 2
            clustered_count = customer_count - random_count
            return generate_customers_random(random_count, centre, range) + generate_customers_clustered(clustered_count, centre, range)
        case "R_RL":
            random_count = customer_count // 2
            realistic_count = customer_count - random_count
            return generate_customers_random(random_count, centre, range) + generate_customers_realistic(realistic_count, centre, range)
        case "C_RL":
            clustered_count = customer_count // 2
            realistic_count = customer_count - clustered_count
            return generate_customers_clustered(clustered_count, centre, range) + generate_customers_realistic(realistic_count, centre, range)
        case "R_C_RL":
            random_count = customer_count // 3
            clustered_count = (customer_count - random_count) // 2
            realistic_count = customer_count - random_count - clustered_count
            return generate_customers_random(random_count, centre, range) + generate_customers_clustered(clustered_count, centre, range) + generate_customers_realistic(realistic_count, centre, range)
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

    def build(self) -> Generator:
        customers = generate_customers(self.customer_sampling, self.customer_count, self.central_location, self.range)

        name = '"name"'
        for c in customers:
            print(f"{c.latitude},{c.longitude},#00FF00,marker,{name}")
        pass

a = AutoGenerator(50, 10, 10, (52.949836, -1.147872), 3000, "RL", "R", "R", "R", "R")
a.build()
