import matplotlib.pyplot as plt
from src_road_graph.road_get import *
import requests
from enum import Enum

location_types = Enum('location_type', ['customer', 'depot', 'charging_point'])

class LocationNode():

    # Constructor Method for a Location Node
    def __init__(self, _langitude: float, _longitude: float) -> None:
        if _langitude not in range(-90, 90): raise ValueError("Langitude must be between -90 and 90")
        if _longitude not in range(-180, 180): raise ValueError("Longitude must be between -180 and 180")
        self.initialize_location(_langitude, _longitude)

    # Initialization for a Location Node
    def initialize_location(self, _langitude: float, _longitude: float) -> None:
        self.langitude: float = _langitude
        self.longitude: float = _longitude
        self.label: str = ""



def



def find_locations(api_key, location, radius=5000, keyword="Costa Coffee", type="cafe"):

    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'location': f"{location[0]},{location[1]}",
        'radius': radius,
        'type': type,
        'keyword': keyword,
        'key': api_key
    }

    try:
        # Send request to Google Places API
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Extract relevant information from response
        results = response.json().get('results', [])
        print(results)
        costa_coffees = [
            {
                'name': place['name'],
                'address': place.get('vicinity', 'N/A'),
                'location': place['geometry']['location']
            }
            for place in results if keyword.lower() in place['name'].lower()
        ]
        return costa_coffees

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")  # Print error message
        return []             # Return an empty list in case of error





def visualize_locations(locations):
    # Extract latitude, longitude, and address of each location
    latitudes = [location['location']['lat'] for location in locations]
    longitudes = [location['location']['lng'] for location in locations]
    names = [location['name'] for location in locations]
    addresses = [location['address'] for location in locations]

    # Plot the locations on a full mesh graph
    plt.figure(figsize=(15, 15))
    plt.scatter(longitudes, latitudes, color='red', marker='o')
    for i, txt in enumerate(names):
        plt.annotate(txt + '\n' + addresses[i].split(",")[0], (longitudes[i], latitudes[i]))
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Costa Coffee Locations')
    plt.grid(True)
    plt.show()

def create_full_mesh_graph(locations, api_key):
    G = nx.Graph()

    # Iterate through each pair of locations
    for i in range(len(locations)):
        for j in range(i + 1, len(locations)):
            origin = f"{locations[i]['location']['lat']},{locations[i]['location']['lng']}"
            destination = f"{locations[j]['location']['lat']},{locations[j]['location']['lng']}"
            directions = get_directions(api_key, origin, destination)
            if directions:
                parsed_graph = parse_directions(directions)
                G.add_edges_from(parsed_graph.edges())
    return G
