from math import cos, sin, sqrt, radians, atan2
from typing import Generator

meters: type = type("meters", (), {})


def chunk_list(locations: list[tuple[float, float]], chunk_size: int = 512) -> Generator[list[tuple[float, float]], None, None]:
    for index in range(0, len(locations), chunk_size): yield locations[index : index + chunk_size]


def haversine(_point_one: float, _point_two: float, earth_radius: meters = 6_387_000) -> meters:
    """
    The haversine formula determines the great-circle distance between two points on a sphere given their longitudes and
    latitudes, (See https://w.wiki/4Aj7). This is used to determine the distance between points in a polyline, when
    approximating the total distance of a route.

    :param _point_one:      Langitude & Longitude of the first point.
    :param _point_two:      Langitude & Longitude of the second point.
    :param earth_radius:    Radius of the earth in meters. (Assumed to be 6,387,000)
    :return:                Distance between the two points in meters.
    """

    lat1, lon1, lat2, lon2 = map(radians, _point_one), map(radians, _point_two)
    a = sin((lat2 - lat1) / 2) ** 2 + cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2) ** 2
    return earth_radius * (2 * atan2(sqrt(a), sqrt(1 - a)))
