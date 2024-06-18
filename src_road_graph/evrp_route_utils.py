from math import cos, sin, sqrt, radians, atan2

# Type to denote meters (avoiding unit confusion).
meters: type = type("meters", (), {})


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

    lat1, lon1 = map(radians, _point_one)
    lat2, lon2 = map(radians, _point_two)
    a = sin((lat2 - lat1) / 2) ** 2 + cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2) ** 2
    return earth_radius * (2 * atan2(sqrt(a), sqrt(1 - a)))


def approximate_distance_from_polyline(polyline = None) -> meters:
    """
    This method approximates the total length of a polyline, and is used to validate the correctness of the polyline
    against the total distance the Directions API provides. It uses the haversine function to calculate the result.

    :return:    Cumulative Distance between all points in the parameterized polyline.
    """

    if polyline == None: raise ValueError
    return sum([haversine(polyline[i], polyline[i + 1]) for i in range(len(polyline) - 1)])