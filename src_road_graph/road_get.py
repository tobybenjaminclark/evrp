
import requests
from evrp_route import Route
from keys import GOOGLE_API_KEY
import re


def get_directions(origin, destination):

    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={GOOGLE_API_KEY}"
    response = requests.get(url)
    r = Route(response.json(), origin, destination)
    return r

if(__name__ == '__main__'):
    get_directions( "KFC Nottingham - Daleside Road, Daleside Road Former Magpie Public House, Nottingham NG2 3GG", "KFC Nottingham - Alfreton Road, 515 Alfreton Rd, Nottingham NG7 3NH        ")

