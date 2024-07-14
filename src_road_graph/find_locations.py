import matplotlib.pyplot as plt
from src_road_graph.road_get import *
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

location_types = Enum('location_type', ['customer', 'depot', 'charging_point'])

class LocationNode():

    # Constructor Method for a Location Node
    def __init__(self, _latitude: float, _longitude: float, _name: str = '') -> None:
        self.latitude: float = _latitude
        self.longitude: float = _longitude
        self.label: str = _name

    def __repr__(self) -> str:
        return f"{self.label}\t@\t{self.latitude}, {self.longitude}"

def result_to_location(result: dict) -> LocationNode:
    return LocationNode(result['geometry']['location']['lat'], result['geometry']['location']['lng'], result['name'])

def find_locations(location: tuple[float, float], radius: int, keyword: str = "", type: PlaceType = PlaceType.NONE) -> list[LocationNode]:
    results: dict = google_nearby_search(location, radius, keyword, type)
    return list(map(result_to_location, results))

def visualize_locations(locations):
    # Extract latitude, longitude, and address of each location
    latitudes = [location.latitude for location in locations]
    longitudes = [location.longitude for location in locations]
    names = [location.label for location in locations]

    # Plot the locations on a full mesh graph
    plt.figure(figsize=(15, 15))
    plt.scatter(longitudes, latitudes, color='red', marker='o')
    for i, txt in enumerate(names):
        plt.annotate(txt, (longitudes[i], latitudes[i]))
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Costa Coffee Locations')
    plt.grid(True)
    plt.show()

def create_full_mesh_graph(locations, api_key = GOOGLE_API_KEY):
    G = nx.Graph()
    for i in range(len(locations)):
        for j in range(i + 1, len(locations)):
            origin = f"{locations[i].latitude},{locations[i].longitude}"
            destination = f"{locations[j].latitude},{locations[j].longitude}"
            directions = get_directions(api_key, origin, destination)
            if directions:
                parsed_graph = parse_directions(directions)
                for edge in parsed_graph.edges():
                    G.add_edge(locations[i], locations[j], path=list(parsed_graph.edges(edge)))
    return G

def draw_full_graph(G):
    pos = {node: (node.longitude, node.latitude) for node in G.nodes()}
    colors = plt.cm.rainbow(np.linspace(0, 1, len(G.edges())))

    plt.figure(figsize=(10, 10))
    for i, (u, v, data) in enumerate(G.edges(data=True)):
        path = data['path']
        edge_pos = [(point[1], point[0]) for segment in path for point in segment]
        xs, ys = zip(*edge_pos)
        plt.plot(xs, ys, color=colors[i])

    plt.scatter([pos[node][0] for node in pos], [pos[node][1] for node in pos], color='red')
    for node in pos:
        plt.annotate(node.label, (pos[node][0], pos[node][1]))

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Full Mesh Network of Roads')
    plt.grid(True)
    plt.show()
