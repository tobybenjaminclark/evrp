from typing import Generator
from src_google_api import get_elevation_data
import requests
import networkx as nx
import matplotlib.pyplot as plt
import polyline as pl
from functools import reduce
from constants import GOOGLE_API_KEY
import math



meters: type = type("meters", (), {})



# Function to chunk list into sublists of given size
def chunk_list(locations: list[tuple[float, float]], chunk_size: int = 512) -> Generator[list[tuple[float, float]], None, None]:
    for index in range(0, len(locations), chunk_size): yield locations[index : index + chunk_size]



# Convert 2 Coordinatea into a distance (in metres)
def haversine(coord1, coord2):
    lat1, lon1 = map(math.radians, coord1)
    lat2, lon2 = map(math.radians, coord2)
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return 6387000 * c



class RouteStep():
    def __init__(self, _encoded_polyline: str, _dist: meters):
        self.dist = _dist
        self.polyline: list[tuple[float, float]] = pl.decode(_encoded_polyline, 5)
        self.calc_dist = self.total_distance()
        self.elevation_data = self.get_elevation_data()
        self.locdata = zip(self.polyline, self.elevation_data)
        for n in self.locdata: print(n)


    def get_elevation_data(self):
        # Convert polyline to list of latitude/longitude pairs
        polyline = self.polyline
        locations = self.polyline

        elevation_data = []

        # Process each chunk of locations
        for chunk in chunk_list(locations, 512):
            # Convert the list of tuples into the required format for the URL
            locations_str = '|'.join([f'{lat},{lng}' for (lat, lng) in chunk])
            print(chunk[0])
            response = get_elevation_data(locations_str)

            # Check if the request was successful
            if response != None:
                elevation_data.extend(response)
            else:
                print(f'Error: {response.status_code}\n{response.text}')
                return None

        return elevation_data

    def total_distance(self) -> meters:
        return sum([haversine(self.polyline[i], self.polyline[i + 1]) for i in range(len(self.polyline) - 1)])

    def __repr__(self):
        return f"RouteStep :: Dist: {self.dist}, Calculated Dist: {self.calc_dist}"



def parse_step(step: dict) -> RouteStep:
    return RouteStep(step['polyline']['points'], step['distance']['value'])



class Route():
    def __init__(self, response: dict):
        print(response)
        self.steps: list[RouteStep] = map(parse_step, [step for route in response['routes'] for leg in route['legs'] for step in leg['steps']])
        for step in self.steps: print(str(step) + "\n")



def get_directions(origin, destination):
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={GOOGLE_API_KEY}"
    response = requests.get(url)
    r = Route(response.json())



if(__name__ == '__main__'):
    get_directions("210 Great Knightleys, Basildon, Essex", "81 Great Knightleys, Basildon, Essex")
