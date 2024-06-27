
import requests
from evrp_route import Route
from constants import GOOGLE_API_KEY



def get_directions(origin, destination):
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={GOOGLE_API_KEY}"
    response = requests.get(url)
    r = Route(response.json(), origin, destination)



if(__name__ == '__main__'):
    get_directions( "210 Great Knightleys, Basildon, Essex", "McDonalds Festival Lesiure, Basildon, Essex")

