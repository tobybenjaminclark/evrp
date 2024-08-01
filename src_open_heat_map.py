import requests
from keys import OPEN_CHARGE_MAP_KEY
from src_road_graph.evrp_location_node import EVChargeNode, DepotNode, CustomerNode

def find_ev_charging_points(latitude = 37.7749, longitude = -122.4194, count = 50):

    # Define the API endpoint and parameters
    endpoint = "https://api.openchargemap.io/v3/poi/"
    params = {
        "output": "json",
        "latitude": latitude,
        "longitude": longitude,
        "maxresults": count,  # Number of results to return
        "key": OPEN_CHARGE_MAP_KEY  # Add your API key here
    }

    # Make the API request
    response = requests.get(endpoint, params=params)
    nodes = []

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        charging_points = response.json()

        # Print the charging points
        for point in charging_points:
            nodes.append(LocationNode(point['AddressInfo']['Latitude'], point['AddressInfo']['Longitude'], point['AddressInfo']['Title'] + " " + str(point['ID'])))
    else:
        print(f"Error: {response.status_code}")
        print(response.json())

    return nodes

if __name__ == "__main__":
    x = find_ev_charging_points()
    for n in x:
        print(n)