from src.src_road_graph.evrp_location_node import CustomerNode
from src.src_apis.src_google_api import *
import requests
from enum import Enum
from src.src_road_graph.evrp_route import Route
from tqdm import tqdm

location_types = Enum('location_type', ['customer', 'depot', 'charging_point'])

def get_directions(origin, destination, pbar: tqdm = None):
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={GOOGLE_API_KEY}"
    response = requests.get(url)
    return Route(response.json(), origin, destination, pbar)

def result_to_location(result: dict) -> tuple[CustomerNode, str]:
    return (CustomerNode(result['geometry']['location']['lat'], result['geometry']['location']['lng'], result['name'], result['rating'], "C0"), result['name'])

def find_locations(location: tuple[float, float], radius: int, keyword: str = "", type: PlaceType = PlaceType.NONE) -> list[CustomerNode]:
    results: dict = google_nearby_search(location, radius, keyword, type)
    return list(map(result_to_location, results))


if __name__ == "__main__":
    a = google_nearby_search((51.574088, 0.486017), 5000, "Costa", PlaceType.NONE)

    for p in a:
        print(p['name'], " :: ", p['rating'])
