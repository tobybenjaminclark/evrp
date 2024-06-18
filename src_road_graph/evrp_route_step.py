from evrp_route_utils import meters, haversine
from src_google_api import get_elevation_data
from polyline import decode as polyline_decode

class RouteStep():

    # Initialze the Route Step
    def __init__(self, _encoded_polyline: str, _dist: meters):
        self.dist = _dist
        self.polyline: list[tuple[float, float]] = polyline_decode(_encoded_polyline, 5)
        self.calc_dist = self.total_distance()
        self.elevation_data = self.calculate_elevation_data()
        self.locdata = zip(self.polyline, self.elevation_data)
        for n in self.locdata: print(n)


    def calculate_elevation_data(self) -> list[meters]:
        """
        This method samples elevation data at each point on a polyline using the Google Elevation API. The line is first
        chunked into sections smaller than 512 langitude, longitude pairs (limit imposed by Elevation API), before being
        passed into the API call (see https://developers.google.com/maps/documentation/elevation/).

        :return: List of altitudes (in meters) for each point in the parameterized polyline.
        """

        elevation_data: list[float] = []
        chunk_list = lambda locations: (locations[index : index + 512] for index in range(0, len(locations), 512))
        for chunk in chunk_list(self.polyline):
            elevation_data.extend(get_elevation_data('|'.join([f'{lat},{lng}' for (lat, lng) in chunk])))
        return list(map(lambda d: d['elevation'], elevation_data))



    def total_distance(self) -> meters:
        """
        This method approximates the total length of a polyline, and is used to validate the correctness of the polyline
        against the total distance the Directions API provides. It uses the haversine function to calculate the result.

        :return: Cumulative Distance between all points in the parameterized polyline.
        """

        return sum([haversine(self.polyline[i], self.polyline[i + 1]) for i in range(len(self.polyline) - 1)])

    # String Representation
    def __repr__(self):
        return f"RouteStep :: Dist: {self.dist}, Calculated Dist: {self.calc_dist}"

def parse_step(step: dict) -> RouteStep:
    return RouteStep(step['polyline']['points'], step['distance']['value'])
