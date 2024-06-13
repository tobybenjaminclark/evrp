import requests
import networkx as nx
import matplotlib.pyplot as plt


def get_directions(api_key, origin, destination):
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        directions = response.json()
        if directions.get('status') == 'OK':
            steps = []
            for route in directions['routes']:
                for leg in route['legs']:
                    steps.extend(leg['steps'])

            for step in steps:
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
