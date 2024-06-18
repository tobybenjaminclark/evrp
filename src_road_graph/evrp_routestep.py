from evrp_route_utils import meters, haversine
from src_google_api import get_elevation_data
from polyline import decode as polyline_decode

class RouteStep():

    # Initialze the Route Step
    def __init__(self, _encoded_polyline: str, _dist: meters):
        self.dist = _dist
        self.polyline: list[tuple[float, float]] = polyline_decode(_encoded_polyline, 5)
        self.calc_dist = self.total_distance()
        self.elevation_data = self.get_elevation_data()
        self.locdata = zip(self.polyline, self.elevation_data)
        for n in self.locdata: print(n)

    # Gets the elevation data
    def get_elevation_data(self, elevation_data: list[float] = []) -> list[meters]:

        chunk_list = lambda locations: (locations[index : index + 512] for index in range(0, len(locations), 512))
        for chunk in chunk_list(self.polyline):
            elevation_data.extend(get_elevation_data('|'.join([f'{lat},{lng}' for (lat, lng) in chunk])))
        return list(map(lambda d: d['elevation'], elevation_data))

    # Gets a total estimated distance from the polyline
    def total_distance(self) -> meters:
        return sum([haversine(self.polyline[i], self.polyline[i + 1]) for i in range(len(self.polyline) - 1)])

    # String Representation
    def __repr__(self):
        return f"RouteStep :: Dist: {self.dist}, Calculated Dist: {self.calc_dist}"

def parse_step(step: dict) -> RouteStep:
    return RouteStep(step['polyline']['points'], step['distance']['value'])
