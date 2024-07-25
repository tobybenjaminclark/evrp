import timeit

import matplotlib.pyplot as plt
from src_road_graph.road_get import *
from src_road_graph.evrp_location_node import LocationNode
from src_open_heat_map import find_ev_charging_points
import requests
from enum import Enum
from keys import GOOGLE_API_KEY
from src_google_api import *
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import requests
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
import logging
from src_road_graph.evrp_route import Route
import concurrent.futures
from typing import List, Any

location_types = Enum('location_type', ['customer', 'depot', 'charging_point'])

def get_directions(origin, destination):
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={GOOGLE_API_KEY}"
    response = requests.get(url)
    r = Route(response.json(), origin, destination)
    return r

def result_to_location(result: dict) -> LocationNode:
    return LocationNode(result['geometry']['location']['lat'], result['geometry']['location']['lng'], result['name'])

def find_locations(location: tuple[float, float], radius: int, keyword: str = "", type: PlaceType = PlaceType.NONE) -> list[LocationNode]:
    results: dict = google_nearby_search(location, radius, keyword, type)
    return list(map(result_to_location, results))

def create_customer_graph2(customers, depots, evs):

    start_time = timeit.default_timer()
    a = customers + depots + evs

    # Print the found locations
    for x in a:
        print(x)

    def fetch_directions(origin_index: int, destination_index: int) -> tuple[Any, Any, float]:
        origin_loc = a[origin_index]
        dest_loc = a[destination_index]
        r = get_directions(
            f"{origin_loc.latitude}, {origin_loc.longitude}",
            f"{dest_loc.latitude}, {dest_loc.longitude}"
        )
        origin_loc.journeys.append((dest_loc.id, r.total))
        return origin_loc, dest_loc, r.total


    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for ind, origin_loc in enumerate(a):
            for other_loc_index in range(0, len(a)):
                if(ind == other_loc_index): continue
                futures.append(executor.submit(fetch_directions, ind, other_loc_index))

        for future in concurrent.futures.as_completed(futures):

            origin, destination, total = future.result()
            if total is not None:
                print(f"EC from: \n{origin} to \n{destination}\n is {total}")
            else:
                print(f"Error?? {total}")
            continue

    end_time = timeit.default_timer()

    logging.info(f"")
    logging.info(f"Total Time Taken: {end_time - start_time}")

if __name__ == "__main__":
    create_customer_graph2()
