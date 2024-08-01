import timeit

import matplotlib.pyplot as plt
from src_road_graph.road_get import *
from src_road_graph.evrp_location_node import CustomerNode, EVChargeNode, DepotNode
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

def result_to_location(result: dict) -> CustomerNode:
    return (CustomerNode(result['geometry']['location']['lat'], result['geometry']['location']['lng'], result['name'], result['rating'], "C0"), result['name'])

def find_locations(location: tuple[float, float], radius: int, keyword: str = "", type: PlaceType = PlaceType.NONE) -> list[CustomerNode]:
    results: dict = google_nearby_search(location, radius, keyword, type)
    return list(map(result_to_location, results))


if __name__ == "__main__":
    a = google_nearby_search((51.574088, 0.486017), 5000, "Costa", PlaceType.NONE)

    for p in a:
        print(p['name'], " :: ", p['rating'])
