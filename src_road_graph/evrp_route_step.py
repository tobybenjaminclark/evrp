from evrp_route_utils import meters, haversine, approximate_distance_from_polyline
from src_google_api import get_elevation_data
from polyline import decode as polyline_decode
from typing import Generator as generator
from dataclasses import dataclass
import re

@dataclass
class RouteStep():
    polyline: list[tuple[float, float]]
    calc_dist: meters
    elevation_data: list[meters]
    locdata: list[tuple[tuple[float, float], meters]]



    def __init__(self, _encoded_polyline: str, _dist: meters):
        """
        Constructor Method to initialize a RouteStep object from Google Directions API data.

        :param _encoded_polyline:   Google Polyline String (see. https://developers.google.com/maps/documentation/utilities/polylinealgorithm)
        :param _dist:               Distance of the route string.
        """

        self.dist = _dist
        self.instructions = ""
        self.polyline: list[tuple[float, float]] = polyline_decode(_encoded_polyline, 5)
        self.calc_dist = approximate_distance_from_polyline(self.polyline)
        self.elevation_data = self.approximate_elevation_series()
        self.locdata = list(zip(self.polyline, self.elevation_data))
        for n in self.locdata: print(n)



    def approximate_elevation_series(self) -> list[meters]:
        """
        This method samples elevation data at each point on a polyline using the Google Elevation API. The line is first
        chunked into sections smaller than 512 langitude, longitude pairs (limit imposed by Elevation API), before being
        passed into the API call (see https://developers.google.com/maps/documentation/elevation/).

        :return: List of altitudes (in meters) for each point in the parameterized polyline.
        """

        elevation_data: list[float] = []

        # The `chunk_list` generator converts a list of polyline points into sublists of maximum size 512.
        chunk_list: generator[list[tuple, tuple], None, None]
        chunk_list = lambda locations: (locations[index : index + 512] for index in range(0, len(locations), 512))
        for chunk in chunk_list(self.polyline):
            elevation_data.extend(get_elevation_data('|'.join([f'{lat},{lng}' for (lat, lng) in chunk])))
        return list(map(lambda d: d['elevation'], elevation_data))



def parse_step(step: dict) -> RouteStep:
    """
    This function parses a 'step' from the Google Directions API, encapsulating the data into to a RouteStep object.
    Refer to (https://developers.google.com/maps/documentation/directions/get-directions#DirectionsLeg-steps)

    :param step:    Dictionary response from Google Directions API.
    :return:        Encapsulated RouteStep Object
    """

    _temp: RouteStep = RouteStep(step['polyline']['points'], step['distance']['value'])
    _temp.instructions = re.sub('<.*?>', '', step['html_instructions'])
    return _temp


