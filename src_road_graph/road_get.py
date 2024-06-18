import requests
import networkx as nx
import matplotlib.pyplot as plt
import polyline as pl
from functools import reduce
from constants import GOOGLE_API_KEY
import math

# Convert 2 Coordinatea into a distance (in metres)
def haversine(coord1, coord2):
    lat1, lon1 = map(math.radians, coord1)
    lat2, lon2 = map(math.radians, coord2)
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return 6387000 * c

meters: type = type("meters", (), {})

class RouteStep():
    def __init__(self, _encoded_polyline: str, _dist: meters):
        self.dist = _dist
        self.polyline: list[tuple[float, float]] = pl.decode(_encoded_polyline, 5)
        self.calc_dist = self.total_distance()
        pass

    def total_distance(self) -> meters:
        return sum([haversine(self.polyline[i], self.polyline[i + 1]) for i in range(len(self.polyline) - 1)])

    def __repr__(self):
        return f"RouteStep :: Dist: {self.dist}, Calculated Dist: {self.calc_dist}"

def parse_step(step: dict) -> RouteStep:
    return RouteStep(step['polyline']['points'], step['distance']['value'])

class Route():
    def __init__(self, response: dict):
        self.steps: list[RouteStep] = map(parse_step, [step for route in response['routes'] for leg in route['legs'] for step in leg['steps']])
        for step in self.steps: print(str(step) + "\n")


def get_directions(origin, destination):
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={GOOGLE_API_KEY}"
    response = requests.get(url)
    r = Route(response.json())
    if response.status_code == 200:
        directions = response.json()
        if directions.get('status') == 'OK':
            steps = []
            for route in directions['routes']:
                for leg in route['legs']:
                    steps.extend(leg['steps'])

            for step in steps:
                print(step['polyline'])
                polyline = pl.decode(step['polyline']['points'], 5)
                print(polyline)
                start_location = step['start_location']
                end_location = step['end_location']
                start_point = (start_location['lat'], start_location['lng'])
                end_point = (end_location['lat'], end_location['lng'])
            return directions
    return None




def parse_directions(directions):
    G = nx.Graph()
    if not directions or directions.get('status') != 'OK':
        return G

    for route in directions['routes']:
        for leg in route['legs']:
            for step in leg['steps']:
                start_location = step['start_location']
                end_location = step['end_location']
                start_point = (start_location['lat'], start_location['lng'])
                end_point = (end_location['lat'], end_location['lng'])
                G.add_edge(start_point, end_point)
    return G


def draw_graph(G, altitude_data=None):
    # Draw the graph with colored edges
    edge_colors = 'black'  # Default color
    pos = {node: (node[1], node[0]) for node in G.nodes()}
    nx.draw(G, pos, node_size=10, with_labels=False, edge_color=edge_colors)
    plt.show()

if(__name__ == '__main__'):
    get_directions("210 Great Knightleys, Basildon, Essex", "81 Great Knightleys, Basildon, Essex")
