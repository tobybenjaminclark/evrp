from src_road_graph.road_get import *
from src_road_graph.find_locations import *
from keys import GOOGLE_API_KEY

r = find_locations((52.9540, -1.150000), 3000, "Costa Coffee")
for x in r:
    print(x)
visualize_locations(r)

g = create_full_mesh_graph(r)
draw_full_graph(g)


"""
# Get road stuff!
origin = 'School of Computer Science, University of Nottingham, Nottingham'
destination = 'Tesco Beeston, Beeston, Nottingham'

directions = get_directions(api_key, origin, destination)
print(directions)

G = parse_directions(directions)
print(G)
draw_graph(G)
"""

"""
location = (52.9540, -1.150000)

costa_coffees = find_locations(api_key, location, 3000, "", "electric_vehicle_charging_station")
g = create_full_mesh_graph(costa_coffees, api_key)
draw_graph(g)
"""

"""
import requests
import matplotlib.pyplot as plt

def get_route_altitude(api_key, origin, destination):
    # Get route from Directions API
    directions_url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={api_key}"
    directions_response = requests.get(directions_url)
    directions_data = directions_response.json()
    print(json.dumps(directions_data, indent=4))

    if directions_data['status'] == 'OK':
        # Extract path from directions
        path = []
        for step in directions_data['routes'][0]['legs'][0]['steps']:
            start_location = step['start_location']
            end_location = step['end_location']
            length = step['distance']['value']
            path.append((start_location['lat'], start_location['lng'], length))
            path.append((end_location['lat'], end_location['lng'], step['html_instructions']))

        # Get elevation data for each point in the path
        elevation_url = f"https://maps.googleapis.com/maps/api/elevation/json"
        elevation_data = []
        distance_data = []
        cumulative_distance = 0

        params = {'locations': f"{path[0][0]},{path[0][1]}", 'key': api_key}
        response = requests.get(elevation_url, params=params)
        cumulative_elevation = response.json()['results'][0]['elevation']

        for i in range(0, len(path), 2):
            spoint = path[i]
            epoint = path[i+1]

            params = {'locations': f"{spoint[0]},{spoint[1]}", 'key': api_key}
            response = requests.get(elevation_url, params=params)
            selevation = response.json()['results'][0]['elevation']

            params = {'locations': f"{epoint[0]},{epoint[1]}", 'key': api_key}
            response = requests.get(elevation_url, params=params)
            eelevation = response.json()['results'][0]['elevation']

            print(f"{epoint[2]}\n\t:: {selevation} -> {eelevation} of length {spoint[2]} (cumulative: {cumulative_distance})\n")

            cumulative_elevation += eelevation - selevation;
            elevation_data.append(cumulative_elevation)

            cumulative_distance += spoint[2]
            distance_data.append(cumulative_distance)

        # Plot altitude graph
        plt.figure(figsize=(20, 6))
        plt.plot(distance_data, elevation_data)
        plt.xlabel('Distance (m)')
        plt.ylabel('Altitude (m)')
        plt.title('Altitude Profile of Route')

        # Set x-axis ticks
        plt.xticks(distance_data, rotation=45)

        # Set axis limits
        plt.xlim(min(distance_data), max(distance_data))
        plt.ylim(min(elevation_data), max(elevation_data))

        plt.grid(True)
        plt.show()

    else:
        print("Failed to retrieve directions.")

# Example usage
api_key = GOOGLE_API_KEY
origin = '210 Great Knightleys, Basildon, Essex'
destination = '81 Great Knightelys, Basildon, Essex'
get_route_altitude(api_key, origin, destination)
"""